from config.database import db_cursor


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
        INSERT INTO usuario (id_rol, nombre_completo, telefono, correo, `contraseña`, foto_perfil)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_rol, nombre_completo, telefono, correo, contrasena_hash, foto_perfil))
        return cursor.lastrowid


def obtener_usuario_por_correo(correo):
    sql = """
       SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo,
        u.`contraseña`, u.foto_perfil,
        u.google_id, u.facebook_id,
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
        u.google_id, u.facebook_id,
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