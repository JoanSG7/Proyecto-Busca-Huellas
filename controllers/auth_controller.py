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
    clean_text,
    current_user_id,
    is_valid_email,
    is_valid_phone,
    is_admin,
)
from controllers.reconocimiento_service import buscar_mascotas_similares, ruta_local_desde_url
from controllers.upload_utils import guardar_imagen, guardar_imagen_base64
from models.alerta_model import crear_alerta, crear_alerta_coincidencia, listar_alertas_usuario
from models.articulo_model import actualizar_articulo, crear_articulo, eliminar_articulo, listar_articulos, obtener_articulo
from models.inicio_model import obtener_estadisticas_inicio
from models.avistamiento_model import crear_avistamiento, obtener_imagen_avistamiento
from models.avistamiento_confirmado_model import confirmar_avistamiento, obtener_avistamiento_confirmable
from models.mascota_model import actualizar_mascota, crear_fotos_mascota, crear_mascota, eliminar_mascota, listar_fotos_mascota, listar_mascotas_con_fotos, listar_mascotas_por_usuario, marcar_mascota_encontrada, obtener_mascota
from models.mensaje_model import (
    crear_mensaje_alerta,
    eliminar_chat_para_usuario,
    listar_chats_alerta,
    listar_mensajes_alerta,
    obtener_chat_alerta,
)
from models.usuario_model import (
    actualizar_contrasena_usuario,
    actualizar_usuario,
    actualizar_preferencias_usuario,
    crear_usuario,
    eliminar_cuenta_usuario,
    obtener_usuario_por_correo,
    obtener_usuario_por_id,
    obtener_preferencias_usuario,
    obtener_usuario_por_google_id,
    obtener_usuario_por_facebook_id,
    actualizar_google_id,
    actualizar_facebook_id,
    correo_usuario_verificado,
    marcar_correo_verificado,
    reactivar_usuario,
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
    return edad >= 18


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
        if not usuario or not usuario.get("estado_usuario", 1) or not check_password_hash(usuario["contraseña"], contrasena):
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("modulo_usuario/inicio_sesion.html", estadisticas=estadisticas), 401

        session.clear()
        session["usuario_id"] = usuario["id_usuario"]
        session["usuario_nombre"] = usuario["nombre_completo"]
        session["rol_id"] = usuario["id_rol"]
        session["correo_verificado"] = correo_usuario_verificado(usuario["id_usuario"])
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


def _build_redirect_uri(provider):
    """Construye el redirect_uri de OAuth evitando el error redirect_uri_mismatch.

    Google trata `localhost` y `127.0.0.1` como URLs distintas. Si el usuario
    entro por 127.0.0.1 pero en Google Cloud registro localhost, falla.

    Solucion:
      1) Si la variable APP_PUBLIC_URL esta definida en .env
         (p. ej. "http://localhost:5000"), la usamos como base. Asi el
         redirect_uri es el MISMO siempre, sin importar por cual URL
         acceda el usuario.
      2) Si no, usamos url_for(..., _external=True) PERO normalizamos:
         sustituimos `127.0.0.1` por `localhost` (es el caso mas comun
         en los entornos del SENA).
    """
    from urllib.parse import urlparse, urlunparse

    path = f"/autenticacion/login/{provider}/callback"
    public_url = os.getenv("APP_PUBLIC_URL", "").strip()

    if public_url:
        # Quitamos barra final si la tiene para no duplicar.
        return public_url.rstrip("/") + path

    redirect_uri = url_for("usuario.oauth_callback", provider=provider, _external=True)

    # Normalizacion automatica: 127.0.0.1 => localhost (mas frecuente en Google Console)
    try:
        parsed = urlparse(redirect_uri)
        if parsed.hostname == "127.0.0.1":
            new_netloc = "localhost"
            if parsed.port:
                new_netloc += f":{parsed.port}"
            parsed = parsed._replace(netloc=new_netloc)
            redirect_uri = urlunparse(parsed)
    except Exception:
        pass

    return redirect_uri


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

    provider = perfil.get("provider")
    if provider == "google":
        social_id = perfil.get("sub")
    else:
        social_id = perfil.get("id")

    if not is_valid_email(correo):
        flash("No pudimos obtener un correo valido desde esa cuenta.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    usuario = None

    if provider == "google":
     usuario = obtener_usuario_por_google_id(social_id)

    elif provider == "facebook":
     usuario = obtener_usuario_por_facebook_id(social_id)

    if not usuario:
     usuario = obtener_usuario_por_correo(correo)

    if usuario and not usuario.get("estado_usuario", 1):
        reactivar_usuario(
            usuario["id_usuario"],
            nombre=nombre,
            correo=correo,
            foto_perfil=foto_perfil,
            google_id=social_id if provider == "google" else None,
            facebook_id=social_id if provider == "facebook" else None,
        )
        usuario = obtener_usuario_por_correo(correo)

    if usuario:
      if provider == "google" and not usuario.get("google_id"):
        actualizar_google_id(usuario["id_usuario"], social_id)
        usuario = obtener_usuario_por_id(usuario["id_usuario"])

      elif provider == "facebook" and not usuario.get("facebook_id"):
        actualizar_facebook_id(usuario["id_usuario"], social_id)
        usuario = obtener_usuario_por_id(usuario["id_usuario"])


    if not usuario:
        codigo = f"{secrets.randbelow(1000000):06d}"
        session["registro_pendiente"] = {
            "codigo": codigo,
            "expira": int(time.time()) + 900,
            "datos": {
                "nombre": nombre,
                "telefono": None,
                "correo": correo,
                "contrasena_hash": generate_password_hash(secrets.token_urlsafe(32)),
                "id_rol": USER_ROLE_ID,
                "google_id": social_id if provider == "google" else None,
                "facebook_id": social_id if provider == "facebook" else None,
                "foto_perfil": foto_perfil,
            },
        }
        enviar_codigo_registro(correo, codigo)
        flash("Te enviamos un código para verificar tu correo y crear la cuenta social.", "success")
        return redirect(url_for("usuario.registro_usuario"))

    session.clear()
    session["usuario_id"] = usuario["id_usuario"]
    session["usuario_nombre"] = usuario["nombre_completo"]
    session["rol_id"] = usuario["id_rol"]
    session["rol_nombre"] = usuario.get("nombre_rol")
    session["correo_verificado"] = correo_usuario_verificado(usuario["id_usuario"])

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
    redirect_uri = _build_redirect_uri(provider)
    print(f"[DEBUG OAuth] Iniciando flujo {provider}")
    print(f"[DEBUG OAuth]   redirect_uri enviado a Google: {redirect_uri}")
    print(f"[DEBUG OAuth]   state guardado en sesion: {state[:8]}...")
    print(f"[DEBUG OAuth]   Host actual: {request.host}")
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

    session_provider = session.get("oauth_provider")
    session_state = session.get("oauth_state")

    # --- Diagnostico detallado por consola para depurar ---
    print(f"[DEBUG OAuth] Callback recibido para provider={provider}")
    print(f"[DEBUG OAuth]   code presente: {bool(code)} | state recibido: {bool(state)}")
    print(f"[DEBUG OAuth]   session[oauth_provider]={session_provider!r}")
    print(f"[DEBUG OAuth]   session[oauth_state]={session_state!r}")
    if not session_state:
        print("[DEBUG OAuth]   AVISO: La sesion esta VACIA. Problema de cookies?")
        print(f"[DEBUG OAuth]   Host: {request.host} | URL: {request.url_root}")

    if not config:
        print(f"[DEBUG OAuth]   FALLO: No hay config para {provider} (revisa CLIENT_ID/SECRET)")
        flash("Las credenciales de inicio de sesión social no están configuradas.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    if provider != session_provider:
        print(f"[DEBUG OAuth]   FALLO: provider mismatch {provider!r} vs sesion {session_provider!r}")
        flash("El proveedor de inicio de sesión no coincide. Inténtalo de nuevo.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    if state != session_state:
        print(f"[DEBUG OAuth]   FALLO: state OAuth no coincide (probablemente sesión perdida)")
        flash("La sesión se perdió durante el inicio de sesión. Asegúrate de usar siempre 'localhost' y no '127.0.0.1'. Inténtalo de nuevo.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    if not code:
        print("[DEBUG OAuth]   FALLO: No se recibio el parametro 'code' de Google")
        flash("Google no devolvió el código de autorización. Inténtalo de nuevo.", "error")
        return redirect(url_for("usuario.inicio_sesion"))

    redirect_uri = _build_redirect_uri(provider)
    print(f"[DEBUG OAuth]   redirect_uri usado en token exchange: {redirect_uri}")
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

            perfil["provider"] = "google"

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
                "id": facebook_profile.get("id"),
                "provider": "facebook",
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

            usuario_existente = obtener_usuario_por_correo(datos.get("correo"))
            if usuario_existente and usuario_existente.get("estado_usuario", 1):
                session.pop("registro_pendiente", None)
                flash("Ya existe una cuenta registrada con ese correo.", "error")
                return render_template("modulo_usuario/registro_usuario.html"), 409

            try:
                if usuario_existente:
                    reactivar_usuario(
                        usuario_existente["id_usuario"],
                        nombre=datos["nombre"],
                        telefono=datos["telefono"],
                        correo=datos["correo"],
                        contrasena_hash=datos["contrasena_hash"],
                        id_rol=datos["id_rol"],
                        foto_perfil=datos.get("foto_perfil"),
                        google_id=datos.get("google_id"),
                        facebook_id=datos.get("facebook_id"),
                    )
                else:
                    crear_usuario(
                        datos["nombre"],
                        datos["telefono"],
                        datos["correo"],
                        datos["contrasena_hash"],
                        id_rol=datos["id_rol"],
                        foto_perfil=datos.get("foto_perfil"),
                    )
            except IntegrityError as exc:
                session.pop("registro_pendiente", None)
                if getattr(exc, "errno", None) == 1062:
                    flash("Ya existe una cuenta registrada con ese correo.", "error")
                    return render_template("modulo_usuario/registro_usuario.html"), 409
                flash("No se pudo crear la cuenta. Revisa los datos e intenta de nuevo.", "error")
                return render_template("modulo_usuario/registro_usuario.html"), 400

            usuario_creado = obtener_usuario_por_correo(datos["correo"])
            if usuario_creado:
                if datos.get("google_id"):
                    actualizar_google_id(usuario_creado["id_usuario"], datos["google_id"])
                if datos.get("facebook_id"):
                    actualizar_facebook_id(usuario_creado["id_usuario"], datos["facebook_id"])
                marcar_correo_verificado(usuario_creado["id_usuario"])
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
            errores.append("Debes tener al menos 18 años para registrarte.")
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
        usuario_existente = obtener_usuario_por_correo(correo)
        if usuario_existente and usuario_existente.get("estado_usuario", 1):
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

    registro = session.get("registro_pendiente") or {}
    if registro.get("datos"):
        return render_template(
            "modulo_usuario/registro_usuario.html",
            codigo_enviado=True,
            correo=registro["datos"].get("correo"),
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
            crear_alerta(
                usuario["id_usuario"],
                None,
                "contrasena_actualizada",
                "Nueva contraseña actualizada correctamente.",
            )
            session.pop("recuperacion_contrasena", None)
            flash("Contraseña actualizada correctamente. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("usuario.inicio_sesion"))

    return render_template("modulo_usuario/recuperar_contraseña.html", correo=correo_inicial)


def mostrar_perfil_usuario():
    usuario = obtener_usuario_por_id(current_user_id())
    mascotas = listar_mascotas_por_usuario(current_user_id())
    return render_template("modulo_usuario/perfil_usuario.html", usuario=usuario, mascotas=mascotas)


def mostrar_configuracion_usuario():
    preferencias = obtener_preferencias_usuario(current_user_id())
    return render_template("modulo_usuario/configuracion.html", preferencias=preferencias)


def guardar_configuracion_usuario():
    tema = clean_text(request.form.get("tema"), 20)
    reducir_movimiento = request.form.get("reducir_movimiento") == "on"
    if tema not in {"claro", "oscuro", "sepia"}:
        flash("Selecciona un tema válido.", "error")
    elif actualizar_preferencias_usuario(current_user_id(), tema, reducir_movimiento):
        flash("Preferencias guardadas para tu cuenta.", "success")
    else:
        flash("Primero ejecuta la migración JSON de preferencias en la base de datos.", "error")
    return redirect(url_for("usuario.configuracion_usuario"))


def eliminar_mi_cuenta():
    id_usuario = current_user_id()
    if not eliminar_cuenta_usuario(id_usuario):
        flash("No fue posible eliminar la cuenta.", "error")
        return redirect(url_for("usuario.configuracion_usuario"))

    session.clear()
    flash("Tu cuenta y los registros asociados fueron desactivados.", "success")
    return redirect(url_for("usuario.inicio_sesion"))


def mostrar_editar_perfil():
    usuario = obtener_usuario_por_id(current_user_id())
    if request.method == "POST":
        nombre = clean_text(request.form.get("fullname"), 100)
        telefono = clean_text(request.form.get("phone"), 20)
        correo = clean_text(request.form.get("email"), 100).lower()
        # La versión recortada se crea en el navegador a partir de la foto elegida.
        # Si JavaScript no está disponible, conservamos la carga de archivo normal.
        foto_recortada = request.form.get("foto_perfil_recortada")
        foto_perfil = (
            guardar_imagen_base64(foto_recortada, "perfiles")
            if foto_recortada
            else guardar_imagen(request.files.get("foto_perfil"), "perfiles")
        )

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
                "Foto de perfil actualizada correctamente.",
            )
        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for("usuario.perfil_usuario"))

    return render_template("modulo_usuario/editar_perfil.html", usuario=usuario)


def mostrar_lista_alertas():
    alertas = listar_alertas_usuario(current_user_id())
    return render_template("modulo_alerta/lista_alertas.html", alertas=alertas)


def listar_alertas_json():
    return jsonify(listar_alertas_usuario(current_user_id()))


def crear_alerta_coincidencia_desde_resultado():
    id_mascota_raw = clean_text(request.form.get("id_mascota"), 20)
    try:
        id_mascota = int(id_mascota_raw)
    except (TypeError, ValueError):
        flash("No se pudo identificar la mascota de la coincidencia.", "error")
        return redirect(url_for("reconocimiento.capturar_foto"))

    mascota = obtener_mascota(id_mascota)
    if not mascota:
        flash("La mascota de la coincidencia ya no está disponible.", "error")
        return redirect(url_for("reconocimiento.capturar_foto"))
    if mascota["id_usuario"] == current_user_id():
        flash("No puedes abrir una alerta de coincidencia para tu propia mascota.", "warning")
        return redirect(url_for("mascota.info_mascota", id_mascota=id_mascota))

    enviar_chat = request.form.get("accion") == "chat"
    foto_alerta = request.form.get("foto_alerta") or ""
    foto_capturada = session.get("ultima_foto_captura")
    if foto_alerta != foto_capturada or not ruta_local_desde_url(foto_alerta):
        flash("La foto de la alerta ya no está disponible. Realiza una nueva búsqueda.", "error")
        return redirect(url_for("reconocimiento.capturar_foto"))

    id_alerta = crear_alerta_coincidencia(current_user_id(), id_mascota, mascota["nombre_mascota"])
    ubicacion = clean_text(request.form.get("ubicacion_avistamiento"), 255) or "Ubicación no disponible"
    crear_avistamiento(
        id_alerta,
        id_mascota,
        ubicacion,
        f"Avistamiento reportado por {session.get('usuario_nombre') or 'un usuario'}.",
        foto_alerta,
    )
    flash("Alerta de coincidencia enviada. Ya puedes comunicarte con el dueño.", "success")
    if enviar_chat:
        imagen_avistamiento = obtener_imagen_avistamiento(id_alerta)
        crear_mensaje_alerta(
            id_alerta,
            current_user_id(),
            mascota["id_usuario"],
            f"Compartió una foto tomada para la alerta sobre {mascota['nombre_mascota']}.",
            url_imagen=imagen_avistamiento,
        )
        return redirect(url_for("mensaje.chat_alerta", id_alerta=id_alerta))
    return redirect(url_for("alerta.alertas"))


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
    if not session.get("correo_verificado") or not correo_usuario_verificado(current_user_id()):
        flash("Debes tener tu correo verificado con código para usar el chat seguro.", "error")
        return redirect(url_for("inicio.inicio"))

    chats = listar_chats_alerta(current_user_id(), is_admin())
    return render_template("modulo_mensaje/chat_seguro.html", chats=chats)


def mostrar_chat_alerta(id_alerta):
    if not session.get("correo_verificado") or not correo_usuario_verificado(current_user_id()):
        flash("Debes tener tu correo verificado con código para usar el chat seguro.", "error")
        return redirect(url_for("inicio.inicio"))

    chat = obtener_chat_alerta(id_alerta, current_user_id(), is_admin())
    if not chat:
        flash("Este chat solo se activa para una coincidencia entre el dueño y quien encontró la mascota.", "error")
        return redirect(url_for("mensaje.chat_seguro"))

    if not correo_usuario_verificado(chat["id_dueno"]) or not correo_usuario_verificado(chat["id_usuario_alerta"]):
        flash("El chat se habilitará cuando ambas cuentas hayan verificado su correo.", "error")
        return redirect(url_for("mensaje.chat_seguro"))

    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "confirmar_avistamiento":
            try:
                id_avistamiento = int(request.form.get("id_avistamiento") or 0)
            except (TypeError, ValueError):
                id_avistamiento = 0
            if current_user_id() != chat["id_dueno"]:
                flash("Solo el dueño de la mascota puede confirmar este avistamiento.", "error")
            elif not obtener_avistamiento_confirmable(
                id_avistamiento,
                id_alerta,
                chat["id_mascota"],
                chat["id_usuario_alerta"],
                chat["id_dueno"],
            ):
                flash("El avistamiento seleccionado no está disponible para confirmar.", "error")
            elif confirmar_avistamiento(id_avistamiento, chat["id_usuario_alerta"], chat["id_dueno"], chat["id_mascota"]):
                marcar_mascota_encontrada(chat["id_mascota"], chat["id_dueno"])
                flash("Avistamiento confirmado. La mascota ahora figura como encontrada.", "success")
            else:
                marcar_mascota_encontrada(chat["id_mascota"], chat["id_dueno"])
                flash("Este avistamiento ya había sido confirmado.", "warning")
            return redirect(url_for("mensaje.chat_alerta", id_alerta=id_alerta))

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
            crear_alerta(
                receptor,
                chat["id_mascota"],
                "mensaje_recibido",
                f"Nuevo mensaje recibido de {session.get('usuario_nombre') or 'un usuario'} sobre {chat['nombre_mascota']}.",
                id_alerta_origen=id_alerta,
            )
            return redirect(url_for("mensaje.chat_alerta", id_alerta=id_alerta))

    mensajes = listar_mensajes_alerta(chat["id_usuario_alerta"], chat["id_dueno"])
    return render_template(
        "modulo_mensaje/chat_avistamiento.html",
        chat=chat,
        mensajes=mensajes,
    )


def eliminar_mi_chat(id_alerta):
    chat = obtener_chat_alerta(id_alerta, current_user_id(), is_admin())
    if not chat:
        flash("No puedes eliminar un chat al que no perteneces.", "error")
    elif eliminar_chat_para_usuario(id_alerta, current_user_id()):
        flash("Chat eliminado de tu lista.", "success")
    else:
        flash("Este chat ya no estaba en tu lista.", "warning")
    return redirect(url_for("mensaje.chat_seguro"))


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
        ubicacion = clean_text(request.form.get("ubicacion"), 150) or None
        estado = "perdida"

        try:
            edad = int(edad_raw) if edad_raw else None
        except ValueError:
            edad = -1

        if len(nombre) < 2 or edad is not None and (edad < 0 or edad > 30):
            flash("El nombre de la mascota y la edad deben ser válidos. La edad máxima es 30 años.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400
        if tamano not in VALID_PET_SIZES:
            flash("Selecciona un tamaño válido.", "error")
            return render_template("modulo_mascota/registro_mascota.html"), 400
        if not ubicacion:
            flash("Selecciona y confirma en el mapa el último lugar donde se vio la mascota.", "error")
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
            current_user_id(), nombre, raza, edad, color, pelaje, tamano, descripcion, estado, ubicacion
        )
        crear_fotos_mascota(id_mascota, fotos)
        crear_alerta(
            current_user_id(),
            id_mascota,
            "mascota_registrada",
            f"Última mascota registrada: {nombre}.",
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
    return render_template(
        "modulo_mascota/info_mascota.html",
        mascota=mascota,
        fotos=fotos,
        es_dueno=mascota.get("id_usuario") == current_user_id(),
    )


def editar_mi_mascota(id_mascota):
    mascota = obtener_mascota(id_mascota)
    if not mascota or mascota.get("id_usuario") != current_user_id():
        flash("No puedes editar esta mascota.", "error")
        return redirect(url_for("usuario.perfil_usuario"))

    if request.method == "POST":
        nombre = clean_text(request.form.get("nombre_mascota"), 100)
        raza = clean_text(request.form.get("raza"), 100) or None
        color = clean_text(request.form.get("color"), 50) or None
        pelaje = clean_text(request.form.get("pelaje"), 50) or None
        tamano = clean_text(request.form.get("tamano"), 50).lower()
        descripcion = clean_text(request.form.get("descripcion"), 1000) or None
        estado = clean_text(request.form.get("estado"), 50).lower() or "perdida"
        try:
            edad = int(clean_text(request.form.get("edad"), 3))
        except ValueError:
            edad = -1

        if len(nombre) < 2 or edad < 0 or edad > 30 or tamano not in VALID_PET_SIZES:
            flash("Revisa el nombre, edad y tamaño de la mascota.", "error")
            return render_template("modulo_mascota/editar_mascota.html", mascota=mascota), 400
        if estado not in VALID_PET_STATES:
            flash("Selecciona un estado válido para la mascota.", "error")
            return render_template("modulo_mascota/editar_mascota.html", mascota=mascota), 400

        actualizar_mascota(
            id_mascota, current_user_id(), nombre, raza, edad, color, pelaje, tamano, descripcion, estado
        )
        flash("Datos de la mascota actualizados.", "success")
        return redirect(url_for("mascota.info_mascota", id_mascota=id_mascota))

    return render_template("modulo_mascota/editar_mascota.html", mascota=mascota)


def eliminar_mi_mascota(id_mascota):
    if eliminar_mascota(id_mascota, current_user_id()):
        flash("La mascota fue desactivada.", "success")
    else:
        flash("No fue posible eliminar esa mascota.", "error")
    return redirect(url_for("usuario.perfil_usuario"))


def mostrar_capturar_foto():
    if request.method == "POST":
        foto_capturada = request.form.get("foto_capturada")
        latitud = clean_text(request.form.get("latitud"), 40)
        longitud = clean_text(request.form.get("longitud"), 40)
        ubicacion_texto = clean_text(request.form.get("ubicacion_texto"), 255)

        if not foto_capturada or not latitud or not longitud:
            flash("Debes tomar una foto y registrar la ubicación antes de buscar.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 400

        foto_url = guardar_imagen_base64(foto_capturada, "capturas")
        if not foto_url:
            flash("No se pudo guardar la foto tomada. Intenta de nuevo.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 400

        session["ultima_foto_captura"] = foto_url

        ruta_foto_usuario = ruta_local_desde_url(foto_url)
        if not ruta_foto_usuario:
            flash("No se pudo preparar la foto para el reconocimiento.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 400

        mascotas_con_fotos = listar_mascotas_con_fotos()
        try:
            resultados = buscar_mascotas_similares(ruta_foto_usuario, mascotas_con_fotos, limite=10)
        except Exception:
            flash("No se pudo completar la comparacion de imagenes. Intenta de nuevo.", "error")
            return render_template("modulo_reconocimiento/capturar_foto.html"), 500

        return render_template(
            "modulo_reconocimiento/resultados.html",
            id_usuario=current_user_id(),
            nombre_usuario=session.get("usuario_nombre") or "Usuario",
            foto_guardada=foto_url,
            ubicacion=ubicacion_texto or "Ubicacion detectada",
            ubicacion_coordenadas=f"{latitud}, {longitud}",
            resultados=resultados,
        )

    return render_template("modulo_reconocimiento/capturar_foto.html")
