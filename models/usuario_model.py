import json

from config.database import db_cursor


def _tiene_columna_verificacion(cursor):
    cursor.execute("SHOW COLUMNS FROM usuario")
    return any(columna["Field"] == "correo_verificado" for columna in cursor.fetchall())


def _tiene_columna_preferencias(cursor):
    cursor.execute("SHOW COLUMNS FROM usuario")
    columnas = {columna["Field"] for columna in cursor.fetchall()}
    return "preferencias" in columnas


def obtener_preferencias_usuario(id_usuario):
    preferencias_originales = {"tema": "claro", "reducir_movimiento": False}
    with db_cursor() as cursor:
        if not _tiene_columna_preferencias(cursor):
            return preferencias_originales
        cursor.execute("SELECT preferencias FROM usuario WHERE id_usuario = %s", (id_usuario,))
        fila = cursor.fetchone() or {}
        preferencias = fila.get("preferencias")
        if isinstance(preferencias, str):
            try:
                preferencias = json.loads(preferencias)
            except json.JSONDecodeError:
                preferencias = {}
        if not isinstance(preferencias, dict):
            preferencias = {}
        return {
            "tema": preferencias.get("tema") if preferencias.get("tema") in {"claro", "oscuro", "sepia"} else "claro",
            "reducir_movimiento": bool(preferencias.get("reducir_movimiento", False)),
        }


def actualizar_preferencias_usuario(id_usuario, tema_preferido, reducir_movimiento):
    with db_cursor(commit=True) as cursor:
        if not _tiene_columna_preferencias(cursor):
            return False
        cursor.execute(
            "UPDATE usuario SET preferencias = %s WHERE id_usuario = %s",
            (json.dumps({"tema": tema_preferido, "reducir_movimiento": reducir_movimiento}), id_usuario),
        )
        return True


def marcar_correo_verificado(id_usuario):
    with db_cursor(commit=True) as cursor:
        if not _tiene_columna_verificacion(cursor):
            return True
        cursor.execute("UPDATE usuario SET correo_verificado = TRUE WHERE id_usuario = %s", (id_usuario,))
        return cursor.rowcount > 0


def correo_usuario_verificado(id_usuario):
    """Las bases antiguas se consideran verificadas para conservar acceso hasta migrarlas."""
    with db_cursor() as cursor:
        if not _tiene_columna_verificacion(cursor):
            return True
        cursor.execute("SELECT correo_verificado FROM usuario WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        return bool(usuario and usuario["correo_verificado"])


def asegurar_roles_basicos():
    sql = """
        INSERT INTO rol (id_rol, nombre_rol)
        VALUES (1, 'Usuario'), (2, 'Administrador')
        ON DUPLICATE KEY UPDATE nombre_rol = VALUES(nombre_rol)
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql)


def crear_usuario(nombre_completo, telefono, correo, contrasena_hash, id_rol=1, foto_perfil=None):
    asegurar_roles_basicos()
    sql = """
        INSERT INTO usuario (id_rol, nombre_completo, telefono, correo, `contraseña`, foto_perfil, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_rol, nombre_completo, telefono, correo, contrasena_hash, foto_perfil))
        return cursor.lastrowid


def obtener_usuario_por_correo(correo):
    sql = """
       SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo,
        u.`contraseña`, u.foto_perfil,
        u.google_id, u.facebook_id, u.fecha_registro,
        r.nombre_rol
        FROM usuario u
        LEFT JOIN rol r ON r.id_rol = u.id_rol
        WHERE u.correo = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (correo,))
        return cursor.fetchone()


def obtener_usuario_por_id(id_usuario):
    sql = """
        SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo,
        u.foto_perfil,
        u.google_id, u.facebook_id, u.fecha_registro,
        r.nombre_rol
        FROM usuario u
        LEFT JOIN rol r ON r.id_rol = u.id_rol
        WHERE u.id_usuario = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchone()


def actualizar_usuario(id_usuario, nombre_completo, telefono, correo, foto_perfil=None):
    sql = """
        UPDATE usuario
        SET nombre_completo = %s,
            telefono = %s,
            correo = %s,
            foto_perfil = COALESCE(%s, foto_perfil)
        WHERE id_usuario = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (nombre_completo, telefono, correo, foto_perfil, id_usuario))
        return cursor.rowcount


def actualizar_contrasena_usuario(id_usuario, contrasena_hash):
    sql = """
        UPDATE usuario
        SET `contraseña` = %s
        WHERE id_usuario = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (contrasena_hash, id_usuario))
        return cursor.rowcount

def obtener_usuario_por_google_id(google_id):
    sql = """
        SELECT *
        FROM usuario
        WHERE google_id = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (google_id,))
        return cursor.fetchone()


def obtener_usuario_por_facebook_id(facebook_id):
    sql = """
        SELECT *
        FROM usuario
        WHERE facebook_id = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (facebook_id,))
        return cursor.fetchone()


def actualizar_google_id(id_usuario, google_id):
    sql = """
        UPDATE usuario
        SET google_id = %s
        WHERE id_usuario = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (google_id, id_usuario))


def actualizar_facebook_id(id_usuario, facebook_id):
    sql = """
        UPDATE usuario
        SET facebook_id = %s
        WHERE id_usuario = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (facebook_id, id_usuario))


def eliminar_cuenta_usuario(id_usuario):
    """Elimina la cuenta y todos los registros que dependen de ella."""
    with db_cursor(commit=True) as cursor:
        cursor.execute("SELECT id_mascota FROM mascota WHERE id_usuario = %s", (id_usuario,))
        mascotas = [fila["id_mascota"] for fila in cursor.fetchall()]

        condiciones_alerta = ["id_usuario = %s"]
        parametros_alerta = [id_usuario]
        if mascotas:
            marcadores = ", ".join(["%s"] * len(mascotas))
            condiciones_alerta.append(f"id_mascota IN ({marcadores})")
            parametros_alerta.extend(mascotas)

        where_alerta = " OR ".join(condiciones_alerta)
        cursor.execute(f"SELECT id_alerta FROM alerta WHERE {where_alerta}", tuple(parametros_alerta))
        alertas = [fila["id_alerta"] for fila in cursor.fetchall()]

        condiciones_mensaje = ["usuario_emisor = %s", "usuario_receptor = %s"]
        parametros_mensaje = [id_usuario, id_usuario]
        if alertas:
            marcadores = ", ".join(["%s"] * len(alertas))
            condiciones_mensaje.append(f"id_alerta IN ({marcadores})")
            parametros_mensaje.extend(alertas)
        cursor.execute(
            f"DELETE FROM mensaje WHERE {' OR '.join(condiciones_mensaje)}",
            tuple(parametros_mensaje),
        )

        cursor.execute(f"DELETE FROM alerta WHERE {where_alerta}", tuple(parametros_alerta))
        cursor.execute("DELETE FROM articulo WHERE id_usuario = %s", (id_usuario,))
        cursor.execute("DELETE FROM informe WHERE id_usuario = %s", (id_usuario,))

        if mascotas:
            marcadores = ", ".join(["%s"] * len(mascotas))
            cursor.execute(f"DELETE FROM foto_mascota WHERE id_mascota IN ({marcadores})", tuple(mascotas))
            cursor.execute(f"DELETE FROM avistamiento WHERE id_mascota IN ({marcadores})", tuple(mascotas))
            cursor.execute(f"DELETE FROM mascota WHERE id_mascota IN ({marcadores})", tuple(mascotas))

        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        return cursor.rowcount > 0
