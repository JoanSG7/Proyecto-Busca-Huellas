import json

from models.eliminacion_model import desactivar_usuario

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


def reactivar_usuario(id_usuario, nombre=None, telefono=None, correo=None, contrasena_hash=None, id_rol=None, foto_perfil=None, google_id=None, facebook_id=None):
    """Reactiva una cuenta conservada por eliminación lógica."""
    sql = """
        UPDATE usuario
        SET estado_usuario = 1,
            nombre_completo = COALESCE(%s, nombre_completo),
            telefono = COALESCE(%s, telefono),
            correo = COALESCE(%s, correo),
            `contraseña` = COALESCE(%s, `contraseña`),
            id_rol = COALESCE(%s, id_rol),
            foto_perfil = COALESCE(%s, foto_perfil),
            google_id = COALESCE(%s, google_id),
            facebook_id = COALESCE(%s, facebook_id)
        WHERE id_usuario = %s AND estado_usuario = 0
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            sql,
            (nombre, telefono, correo, contrasena_hash, id_rol, foto_perfil, google_id, facebook_id, id_usuario),
        )
        return cursor.rowcount


def obtener_usuario_por_correo(correo):
    sql = """
       SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo, u.estado_usuario,
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
        WHERE u.id_usuario = %s AND u.estado_usuario = 1
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
        WHERE google_id = %s AND estado_usuario = 1
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (google_id,))
        return cursor.fetchone()


def obtener_usuario_por_facebook_id(facebook_id):
    sql = """
        SELECT *
        FROM usuario
        WHERE facebook_id = %s AND estado_usuario = 1
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
    return desactivar_usuario(id_usuario) > 0
