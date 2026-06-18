import os
import json
import secrets
import smtplib
import time
import unicodedata
from datetime import date, datetime
from email.message import EmailMessage
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from mysql.connector import IntegrityError
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from controllers.security import (
    ADMIN_REGISTRATION_CODE,
    ADMIN_ROLE_ID,
    USER_ROLE_ID,
    VALID_PET_SIZES,
    VALID_PET_STATES,
    clean_text,
    current_user_id,
    is_valid_email,
    is_valid_phone,
    is_admin,
)
from controllers.upload_utils import guardar_imagen, guardar_imagen_base64
from models.alerta_model import crear_alerta, listar_alertas_usuario
from models.articulo_model import actualizar_articulo, crear_articulo, eliminar_articulo, listar_articulos, obtener_articulo
from models.inicio_model import obtener_estadisticas_inicio
from models.mascota_model import crear_fotos_mascota, crear_mascota, listar_fotos_mascota, listar_mascotas_por_usuario, obtener_mascota
from models.mensaje_model import (
    crear_mensaje_alerta,
    listar_chats_alerta,
    listar_mensajes_alerta,
    obtener_chat_alerta,
)
from models.usuario_model import (
    actualizar_contrasena_usuario,
    actualizar_usuario,
    crear_usuario,
    obtener_usuario_por_correo,
    obtener_usuario_por_id,
)


OAUTH_PROVIDERS = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "profile_url": "https://openidconnect.googleapis.com/v1/userinfo",
        "scope": "openid email profile",
        "client_id_env": "GOOGLE_CLIENT_ID",
        "client_secret_env": "GOOGLE_CLIENT_SECRET",
    },
    "facebook": {
        "auth_url": "https://www.facebook.com/v19.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v19.0/oauth/access_token",
        "profile_url": "https://graph.facebook.com/me",
        "scope": "email,public_profile",
        "client_id_env": "FACEBOOK_CLIENT_ID",
        "client_secret_env": "FACEBOOK_CLIENT_SECRET",
    },
}


def _es_mayor_de_edad(fecha_nacimiento_raw):
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_raw or "", "%Y-%m-%d").date()
    except ValueError:
        return False

    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )
    return edad > 18


def mostrar_inicio():
    articulos = listar_articulos()[:3]
    estadisticas = obtener_estadisticas_inicio()
    return render_template("inicio.html", articulos=articulos, estadisticas=estadisticas)


def obtener_estadisticas_inicio_json():
    return jsonify(obtener_estadisticas_inicio())


def enviar_codigo_recuperacion(correo, codigo):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    remitente = os.getenv("SMTP_FROM", smtp_user or "no-reply@buscahuellas.local")

    if not smtp_host:
        print(f"Codigo de recuperacion para {correo}: {codigo}")
        return

    mensaje = EmailMessage()
    mensaje["Subject"] = "Codigo de recuperacion - Busca Huellas"
    mensaje["From"] = remitente
    mensaje["To"] = correo
    mensaje.set_content(
        f"Tu codigo de recuperacion de Busca Huellas es: {codigo}\n\n"
        "Este codigo vence en 15 minutos."
    )

    with smtplib.SMTP(smtp_host, smtp_port) as servidor:
        servidor.starttls()
        if smtp_user and smtp_password:
            servidor.login(smtp_user, smtp_password)
        servidor.send_message(mensaje)


def enviar_codigo_registro(correo, codigo):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    print("SMTP_HOST:", smtp_host)
    print("SMTP_USER:", smtp_user)
    print("SMTP_PASSWORD:", smtp_password)
    
    remitente = os.getenv("SMTP_FROM", smtp_user or "no-reply@buscahuellas.local")

    if not smtp_host:
        print(f"Codigo de registro para {correo}: {codigo}")
        return

    mensaje = EmailMessage()
    mensaje["Subject"] = "Codigo de registro - Busca Huellas"
    mensaje["From"] = remitente
    mensaje["To"] = correo
    mensaje.set_content(
        f"Tu codigo de registro de Busca Huellas es: {codigo}\n\n"
        "Este codigo vence en 15 minutos."
    )

    with smtplib.SMTP(smtp_host, smtp_port) as servidor:
        servidor.starttls()
        if smtp_user and smtp_password:
            servidor.login(smtp_user, smtp_password)
        servidor.send_message(mensaje)


def mostrar_inicio_sesion():
    estadisticas = obtener_estadisticas_inicio()
    if request.method == "POST":
        correo = clean_text(request.form.get("email"), 100).lower()
        contrasena = request.form.get("password") or ""

        if not is_valid_email(correo) or not contrasena:
            flash("Correo o contraseña inválidos.", "error")
            return render_template("modulo_usuario/inicio_sesion.html", estadisticas=estadisticas), 400

        usuario = obtener_usuario_por_correo(correo)
        if not usuario or not check_password_hash(usuario["contraseña"], contrasena):
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("modulo_usuario/inicio_sesion.html", estadisticas=estadisticas), 401

        session.clear()
        session["usuario_id"] = usuario["id_usuario"]
        session["usuario_nombre"] = usuario["nombre_completo"]
        session["rol_id"] = usuario["id_rol"]
        session["correo_verificado"] = True
        flash("Inicio de sesión exitoso.", "success")
        return redirect(url_for("inicio.inicio"))

    return render_template("modulo_usuario/inicio_sesion.html", estadisticas=estadisticas)


def _oauth_config(provider):
    config = OAUTH_PROVIDERS.get(provider)
    if not config:
        return None

    client_id = os.getenv(config["client_id_env"])
    client_secret = os.getenv(config["client_secret_env"])
    if not client_id or not client_secret:
        return None

    return {**config, "client_id": client_id, "client_secret": client_secret}


def _json_request(url, data=None, headers=None):
    body = None
    request_headers = headers or {}
    if data is not None:
        body = urlencode(data).encode("utf-8")
        request_headers = {"Content-Type": "application/x-www-form-urlencoded", **request_headers}

    request_obj = Request(url, data=body, headers=request_headers)
    with urlopen(request_obj, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def _iniciar_sesion_oauth(perfil):
    correo = clean_text(perfil.get("email"), 100).lower()
    nombre = clean_text(perfil.get("name"), 100) or correo.split("@")[0]
    foto_perfil = clean_text(perfil.get("picture"), 255) or None

    if not is_valid_email(correo):
        flash("No pudimos obtener un correo valido desde esa cuenta.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    usuario = obtener_usuario_por_correo(correo)
    if not usuario:
        contrasena_temporal = generate_password_hash(secrets.token_urlsafe(32))
        crear_usuario(nombre, None, correo, contrasena_temporal, id_rol=USER_ROLE_ID, foto_perfil=foto_perfil)
        usuario = obtener_usuario_por_correo(correo)

    session.clear()
    session["usuario_id"] = usuario["id_usuario"]
    session["usuario_nombre"] = usuario["nombre_completo"]
    session["rol_id"] = usuario["id_rol"]
    session["rol_nombre"] = usuario.get("nombre_rol")
    session["correo_verificado"] = False
    flash("Inicio de sesion exitoso.", "success")
    return redirect(url_for("inicio.inicio"))


def iniciar_login_social(provider):
    config = _oauth_config(provider)
    if not config:
        flash(f"Configura {provider.upper()}_CLIENT_ID y {provider.upper()}_CLIENT_SECRET para usar este inicio de sesion.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    state = secrets.token_urlsafe(24)
    session["oauth_state"] = state
    session["oauth_provider"] = provider
    redirect_uri = url_for("usuario.oauth_callback", provider=provider, _external=True)

    params = {
        "client_id": config["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": config["scope"],
        "state": state,
    }
    if provider == "google":
        params["prompt"] = "select_account"

    return redirect(f"{config['auth_url']}?{urlencode(params)}")


def recibir_login_social(provider):
    config = _oauth_config(provider)
    state = request.args.get("state")
    code = request.args.get("code")

    if not config or provider != session.get("oauth_provider") or state != session.get("oauth_state") or not code:
        flash("No se pudo validar el inicio de sesion social.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    redirect_uri = url_for("usuario.oauth_callback", provider=provider, _external=True)
    try:
        if provider == "google":
            token_data = _json_request(
                config["token_url"],
                {
                    "client_id": config["client_id"],
                    "client_secret": config["client_secret"],
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                },
            )
            perfil = _json_request(
                config["profile_url"],
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
        else:
            token_url = f"{config['token_url']}?{urlencode({
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'code': code,
                'redirect_uri': redirect_uri,
            })}"
            token_data = _json_request(token_url)
            profile_url = f"{config['profile_url']}?{urlencode({
                'fields': 'id,name,email,picture.type(large)',
                'access_token': token_data['access_token'],
            })}"
            facebook_profile = _json_request(profile_url)
            perfil = {
                "email": facebook_profile.get("email"),
                "name": facebook_profile.get("name"),
                "picture": ((facebook_profile.get("picture") or {}).get("data") or {}).get("url"),
            }
    except (KeyError, URLError, TimeoutError, ValueError):
        flash("No se pudo completar el inicio de sesion social. Intenta de nuevo.", "error")
        return redirect(url_for("usuario.inicio_sesion"))
    finally:
        session.pop("oauth_state", None)
        session.pop("oauth_provider", None)

    return _iniciar_sesion_oauth(perfil)


def mostrar_registro_usuario():
    if request.method == "POST":
        accion = request.form.get("accion") or "enviar_codigo"

        if accion == "verificar_codigo":
            codigo = clean_text(request.form.get("codigo"), 6)
            registro = session.get("registro_pendiente") or {}
            datos = registro.get("datos") or {}
            codigo_valido = (
                registro.get("codigo") == codigo
                and registro.get("expira", 0) >= int(time.time())
            )

            if not codigo_valido:
                flash("El codigo de registro no es valido o ya vencio.", "error")
                return render_template(
                    "modulo_usuario/registro_usuario.html",
                    codigo_enviado=True,
                    correo=datos.get("correo"),
                ), 400

            if obtener_usuario_por_correo(datos.get("correo")):
                session.pop("registro_pendiente", None)
                flash("Ya existe una cuenta registrada con ese correo.", "error")
                return render_template("modulo_usuario/registro_usuario.html"), 409

            try:
                crear_usuario(
                    datos["nombre"],
                    datos["telefono"],
                    datos["correo"],
                    datos["contrasena_hash"],
                    id_rol=datos["id_rol"],
                )
            except IntegrityError as exc:
                session.pop("registro_pendiente", None)
                if getattr(exc, "errno", None) == 1062:
                    flash("Ya existe una cuenta registrada con ese correo.", "error")
                    return render_template("modulo_usuario/registro_usuario.html"), 409
                flash("No se pudo crear la cuenta. Revisa los datos e intenta de nuevo.", "error")
                return render_template("modulo_usuario/registro_usuario.html"), 400

            session.pop("registro_pendiente", None)
            flash("Cuenta creada y correo verificado. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("usuario.inicio_sesion"))

        nombre = clean_text(request.form.get("name"), 100)
        telefono = clean_text(request.form.get("phone"), 20)
        correo = clean_text(request.form.get("email"), 100).lower()
        fecha_nacimiento = clean_text(request.form.get("dob"), 20)
        contrasena = request.form.get("password") or ""
        confirmar = request.form.get("confirm_password") or ""
        rol_solicitado = clean_text(request.form.get("role"), 20).lower() or "usuario"
        codigo_admin = clean_text(request.form.get("admin_code"), 100)
        id_rol = USER_ROLE_ID

        errores = []
        if len(nombre) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres.")
        if not is_valid_phone(telefono):
            errores.append("El teléfono no tiene un formato válido.")
        if not is_valid_email(correo):
            errores.append("El correo no tiene un formato válido.")
        if not _es_mayor_de_edad(fecha_nacimiento):
            errores.append("Debes ser mayor de 18 años para registrarte.")
        if len(contrasena) < 8:
            errores.append("La contraseña debe tener mínimo 8 caracteres.")
        if contrasena != confirmar:
            errores.append("Las contraseñas no coinciden.")
        if rol_solicitado not in {"usuario", "admin"}:
            errores.append("Selecciona un tipo de cuenta válido.")
        if rol_solicitado == "admin":
            if codigo_admin != ADMIN_REGISTRATION_CODE:
                errores.append("El código de administrador no es válido.")
            else:
                id_rol = ADMIN_ROLE_ID
        if request.form.get("terms") != "on":
            errores.append("Debes aceptar los términos para crear la cuenta.")
        if obtener_usuario_por_correo(correo):
            errores.append("Ya existe una cuenta registrada con ese correo.")

        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("modulo_usuario/registro_usuario.html"), 400

        codigo = f"{secrets.randbelow(1000000):06d}"
        session["registro_pendiente"] = {
            "codigo": codigo,
            "expira": int(time.time()) + 900,
            "datos": {
                "nombre": nombre,
                "telefono": telefono,
                "correo": correo,
                "contrasena_hash": generate_password_hash(contrasena),
                "id_rol": id_rol,
            },
        }
        enviar_codigo_registro(correo, codigo)
        flash("Te enviamos un código de 6 dígitos al correo para terminar el registro.", "success")
        return render_template(
            "modulo_usuario/registro_usuario.html",
            codigo_enviado=True,
            correo=correo,
        )

    return render_template("modulo_usuario/registro_usuario.html")


def cerrar_sesion():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("usuario.inicio_sesion"))


def mostrar_recuperar_contrasena():
    correo_inicial = clean_text(request.args.get("email"), 100).lower()
    if request.method == "POST":
        accion = request.form.get("accion")
        correo = clean_text(request.form.get("email"), 100).lower()

        if accion == "enviar_codigo":
            if not is_valid_email(correo):
                flash("El correo no tiene un formato válido.", "error")
                return render_template("modulo_usuario/recuperar_contraseña.html"), 400

            usuario = obtener_usuario_por_correo(correo)
            if not usuario:
                flash("Este correo no esta vinculado a ninguna cuenta", "error")
                return render_template("modulo_usuario/recuperar_contraseña.html"), 404

            codigo = f"{secrets.randbelow(1000000):06d}"
            session["recuperacion_contrasena"] = {
                "correo": correo,
                "codigo": codigo,
                "expira": int(time.time()) + 900,
            }
            enviar_codigo_recuperacion(correo, codigo)
            flash("Te enviamos un código de 6 dígitos al correo.", "success")
            return render_template(
                "modulo_usuario/recuperar_contraseña.html",
                codigo_enviado=True,
                correo=correo,
            )

        if accion == "cambiar_contrasena":
            codigo = clean_text(request.form.get("codigo"), 6)
            contrasena = request.form.get("password") or ""
            recuperacion = session.get("recuperacion_contrasena") or {}

            codigo_valido = (
                recuperacion.get("correo") == correo
                and recuperacion.get("codigo") == codigo
                and recuperacion.get("expira", 0) >= int(time.time())
            )
            if not codigo_valido:
                flash(" El codigo no es valido", "error")
                return render_template(
                    "modulo_usuario/recuperar_contraseña.html",
                    codigo_enviado=True,
                    correo=correo,
                ), 400

            if len(contrasena) < 8:
                flash("La contraseña debe tener mínimo 8 caracteres.", "error")
                return render_template(
                    "modulo_usuario/recuperar_contraseña.html",
                    codigo_enviado=True,
                    correo=correo,
                ), 400

            usuario = obtener_usuario_por_correo(correo)
            if not usuario:
                flash("Este correo no esta vinculado a ninguna cuenta", "error")
                return render_template("modulo_usuario/recuperar_contraseña.html"), 404

            actualizar_contrasena_usuario(usuario["id_usuario"], generate_password_hash(contrasena))
            session.pop("recuperacion_contrasena", None)
            flash("Contraseña actualizada correctamente. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("usuario.inicio_sesion"))

    return render_template("modulo_usuario/recuperar_contraseña.html", correo=correo_inicial)


def mostrar_perfil_usuario():
    usuario = obtener_usuario_por_id(current_user_id())
    mascotas = listar_mascotas_por_usuario(current_user_id())
    return render_template("modulo_usuario/perfil_usuario.html", usuario=usuario, mascotas=mascotas)


def mostrar_editar_perfil():
    usuario = obtener_usuario_por_id(current_user_id())
    if request.method == "POST":
        nombre = clean_text(request.form.get("fullname"), 100)
        telefono = clean_text(request.form.get("phone"), 20)
        correo = clean_text(request.form.get("email"), 100).lower()
        foto_perfil = guardar_imagen(request.files.get("foto_perfil"), "perfiles")

        if len(nombre) < 3 or not is_valid_email(correo) or not is_valid_phone(telefono):
            flash("Revisa nombre, correo y teléfono antes de guardar.", "error")
            return render_template("modulo_usuario/editar_perfil.html", usuario=usuario), 400

        try:
            actualizar_usuario(current_user_id(), nombre, telefono, correo, foto_perfil)
        except IntegrityError:
            flash("Ese correo ya está en uso por otra cuenta.", "error")
            return render_template("modulo_usuario/editar_perfil.html", usuario=usuario), 409

        session["usuario_nombre"] = nombre
        if foto_perfil:
            crear_alerta(
                current_user_id(),
                None,
                "perfil_actualizado",
                "Se ha actualizado tu foto de perfil correctamente.",
            )
        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for("usuario.perfil_usuario"))

    return render_template("modulo_usuario/editar_perfil.html", usuario=usuario)


def mostrar_lista_alertas():
    alertas = listar_alertas_usuario(current_user_id())
    return render_template("modulo_alerta/lista_alertas.html", alertas=alertas)


def listar_alertas_json():
    return jsonify(listar_alertas_usuario(current_user_id()))


PALABRAS_BLOQUEADAS_CHAT = {
    "idiota",
    "imbecil",
    "estupido",
    "maldito",
    "mierda",
    "puta",
    "puto",
    "gonorrea",
    "marica",
    "pendejo",
}


def _normalizar_mensaje_chat(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")


def _mensaje_tiene_palabras_bloqueadas(texto):
    normalizado = _normalizar_mensaje_chat(texto)
    return any(palabra in normalizado.split() for palabra in PALABRAS_BLOQUEADAS_CHAT)


def mostrar_chat_seguro():
    if not session.get("correo_verificado"):
        flash("Debes tener tu correo verificado con código para usar el chat seguro.", "error")
        return redirect(url_for("inicio.inicio"))

    chats = listar_chats_alerta(current_user_id(), is_admin())
    return render_template("modulo_mensaje/chat_seguro.html", chats=chats)


def mostrar_chat_alerta(id_alerta):
    if not session.get("correo_verificado"):
        flash("Debes tener tu correo verificado con código para usar el chat seguro.", "error")
        return redirect(url_for("inicio.inicio"))

    chat = obtener_chat_alerta(id_alerta, current_user_id(), is_admin())
    if not chat:
        flash("Este chat solo se activa cuando la alerta esta confirmada.", "error")
        return redirect(url_for("mensaje.chat_seguro"))

    if request.method == "POST":
        mensaje = clean_text(request.form.get("mensaje"), 700)
        receptor = chat["id_dueno"] if current_user_id() != chat["id_dueno"] else chat["id_usuario_alerta"]
        if len(mensaje) < 2:
            flash("Escribe un mensaje antes de enviarlo.", "error")
        elif _mensaje_tiene_palabras_bloqueadas(mensaje):
            flash("Tu mensaje contiene palabras fuertes o indebidas. Reescribelo con respeto.", "error")
        elif not receptor:
            flash("No hay un usuario receptor para este chat.", "error")
        else:
            crear_mensaje_alerta(id_alerta, current_user_id(), receptor, mensaje)
            return redirect(url_for("mensaje.chat_alerta", id_alerta=id_alerta))

    mensajes = listar_mensajes_alerta(id_alerta)
    return render_template(
        "modulo_mensaje/chat_avistamiento.html",
        chat=chat,
        mensajes=mensajes,
    )


def mostrar_lista_articulos():
    articulos = listar_articulos()
    return render_template("modulo_articulo/lista_articulos.html", articulos=articulos)


def mostrar_articulo_completo(id_articulo):
    articulo = obtener_articulo(id_articulo)
    if not articulo:
        flash("El artículo solicitado no existe.", "error")
        return redirect(url_for("articulo.lista_articulos"))
    relacionados = [item for item in listar_articulos() if item["id_articulo"] != articulo["id_articulo"]][:3]
    return render_template("modulo_articulo/articulo_completo.html", articulo=articulo, relacionados=relacionados)


def registrar_articulo():
    if not is_admin():
        flash("Solo un administrador puede publicar artículos.", "error")
        return redirect(url_for("articulo.lista_articulos"))

    titulo = clean_text(request.form.get("titulo"), 255)
    contenido = clean_text(request.form.get("contenido"), 5000)
    url_imagen = guardar_imagen(request.files.get("imagen_articulo"), "articulos")

    if len(titulo) < 5 or len(contenido) < 20:
        flash("El artículo necesita un título y contenido más completos.", "error")
        return redirect(url_for("articulo.lista_articulos"))

    id_articulo = crear_articulo(current_user_id(), titulo, contenido, url_imagen)
    flash("Artículo publicado correctamente.", "success")
    return redirect(url_for("articulo.articulo_completo", id_articulo=id_articulo))


def editar_articulo(id_articulo):
    articulo = obtener_articulo(id_articulo)
    if not articulo or not is_admin():
        flash("No tienes permiso para modificar este artículo.", "error")
        return redirect(url_for("articulo.lista_articulos"))

    titulo = clean_text(request.form.get("titulo"), 255)
    contenido = clean_text(request.form.get("contenido"), 5000)
    url_imagen = guardar_imagen(request.files.get("imagen_articulo"), "articulos") or articulo.get("url_imagen")

    if len(titulo) < 5 or len(contenido) < 20:
        flash("El artículo necesita un título y contenido más completos.", "error")
        return redirect(url_for("articulo.articulo_completo", id_articulo=id_articulo))

    actualizar_articulo(id_articulo, titulo, contenido, url_imagen)
    flash("Artículo actualizado correctamente.", "success")
    return redirect(url_for("articulo.articulo_completo", id_articulo=id_articulo))


def borrar_articulo(id_articulo):
    articulo = obtener_articulo(id_articulo)
    if not articulo or not is_admin():
        flash("No tienes permiso para eliminar este artículo.", "error")
        return redirect(url_for("articulo.lista_articulos"))

    eliminar_articulo(id_articulo)
    flash("Artículo eliminado correctamente.", "success")
    return redirect(url_for("articulo.lista_articulos"))


def mostrar_registro_mascota():
    if request.method == "POST":
        nombre = clean_text(request.form.get("nombre_mascota"), 100)
        raza = clean_text(request.form.get("raza"), 100) or None
        edad_raw = clean_text(request.form.get("edad"))
        color = clean_text(request.form.get("color"), 50) or None
        pelaje = clean_text(request.form.get("pelaje"), 50) or None
        tamano = clean_text(request.form.get("tamano"), 50).lower()
        descripcion = clean_text(request.form.get("descripcion"), 1000) or None
        estado = clean_text(request.form.get("estado"), 50).lower() or "perdida"

        try:
            edad = int(edad_raw) if edad_raw else None
        except ValueError:
            edad = -1

        if len(nombre) < 2 or edad is not None and edad < 0:
            flash("El nombre de la mascota y la edad deben ser válidos.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400
        if tamano not in VALID_PET_SIZES:
            flash("Selecciona un tamaño válido.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400
        if estado not in VALID_PET_STATES:
            flash("Selecciona un estado válido.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400

        fotos = [
            guardar_imagen(foto, "mascotas")
            for foto in request.files.getlist("fotos_mascota")
            if foto and foto.filename
        ]
        fotos = [foto for foto in fotos if foto]
        if len(fotos) < 2:
            flash("Debes subir mínimo 2 fotos recientes de la mascota.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400

        id_mascota = crear_mascota(
            current_user_id(), nombre, raza, edad, color, pelaje, tamano, descripcion, estado
        )
        crear_fotos_mascota(id_mascota, fotos)
        if estado == "perdida":
            crear_alerta(
                current_user_id(),
                id_mascota,
                "mascota_perdida",
                f"Tu reporte de {nombre} quedo activo y la comunidad podra verlo.",
            )
            crear_alerta(
                current_user_id(),
                id_mascota,
                "mascota_cercana",
                f"Se genero una alerta de mascota cercana para {nombre}.",
            )
        elif estado == "encontrada":
            crear_alerta(
                current_user_id(),
                id_mascota,
                "mascota_encontrada",
                f"Se registro a {nombre} como mascota encontrada. Puedes iniciar chat desde esta alerta.",
            )
        flash("Mascota registrada correctamente.", "success")
        return redirect(url_for("mascota.info_mascota", id_mascota=id_mascota))

    return render_template("modulo_mascota/registro_mascota.html")


def mostrar_info_mascota(id_mascota):
    mascota = obtener_mascota(id_mascota)
    if not mascota:
        flash("La mascota solicitada no existe.", "error")
        return redirect(url_for("usuario.perfil_usuario"))
    fotos = listar_fotos_mascota(id_mascota)
    return render_template("modulo_mascota/info_mascota.html", mascota=mascota, fotos=fotos)


def mostrar_capturar_foto():
    if request.method == "POST":
        foto_capturada = request.form.get("foto_capturada")
        latitud = clean_text(request.form.get("latitud"), 40)
        longitud = clean_text(request.form.get("longitud"), 40)

        if not foto_capturada or not latitud or not longitud:
            flash("Debes tomar una foto y registrar la ubicación antes de buscar.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 400

        foto_url = guardar_imagen_base64(foto_capturada, "capturas")
        if not foto_url:
            flash("No se pudo guardar la foto tomada. Intenta de nuevo.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 400

        flash("Foto y ubicación registradas. Búsqueda iniciada.", "success")
        crear_alerta(
            current_user_id(),
            None,
            "hallazgo_reportado",
            f"Se reporto un hallazgo con foto y ubicacion en tiempo real: {latitud}, {longitud}.",
        )
        return render_template(
            "modulo_reconocimiento/capturar_foto.html",
            foto_guardada=foto_url,
            ubicacion=f"{latitud}, {longitud}",
        )

    return render_template("modulo_reconocimiento/capturar_foto.html")
