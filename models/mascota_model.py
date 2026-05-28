from config.database import db_cursor


def crear_mascota(id_usuario, nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado):
    sql = """
        INSERT INTO mascota
            (id_usuario, nombre_mascota, raza, edad, color, pelaje, `tamaño`, descripcion, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_usuario, nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado))
        return cursor.lastrowid


def crear_fotos_mascota(id_mascota, urls_fotos):
    if not urls_fotos:
        return 0

    sql = "INSERT INTO foto_mascota (id_mascota, url_imagen) VALUES (%s, %s)"
    with db_cursor(commit=True) as cursor:
        cursor.executemany(sql, [(id_mascota, url_foto) for url_foto in urls_fotos])
        return cursor.rowcount


def listar_fotos_mascota(id_mascota):
    sql = """

        SELECT id_foto, url_imagen
        FROM foto_mascota
        WHERE id_mascota = %s
        ORDER BY id_foto ASC

    with db_cursor() as cursor:
        cursor.execute(sql, (id_mascota,))
        return cursor.fetchall()


def listar_mascotas_por_usuario(id_usuario):
    sql = """
        SELECT id_mascota, nombre_mascota, raza, edad, color, pelaje, `tamaño` AS tamano,
               descripcion, estado
        FROM mascota
        WHERE id_usuario = %s
        ORDER BY id_mascota DESC
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchall()


def obtener_mascota(id_mascota):
    sql = """
        SELECT m.id_mascota, m.id_usuario, m.nombre_mascota, m.raza, m.edad, m.color,
               m.pelaje, m.`tamaño` AS tamano, m.descripcion, m.estado,
               u.nombre_completo, u.telefono, u.correo
        FROM mascota m
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
        WHERE m.id_mascota = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_mascota,))
        return cursor.fetchone()


def actualizar_mascota(id_mascota, id_usuario, nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado):
    sql = """
        UPDATE mascota
        SET nombre_mascota = %s, raza = %s, edad = %s, color = %s, pelaje = %s,
            `tamaño` = %s, descripcion = %s, estado = %s
        WHERE id_mascota = %s AND id_usuario = %s
    """
    params = (nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado, id_mascota, id_usuario)
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, params)
        return cursor.rowcount


def eliminar_mascota(id_mascota, id_usuario):
    sql = "DELETE FROM mascota WHERE id_mascota = %s AND id_usuario = %s"
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_mascota, id_usuario))
        return cursor.rowcount
