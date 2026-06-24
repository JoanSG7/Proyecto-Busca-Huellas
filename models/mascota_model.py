from config.database import db_cursor


def _columna_ubicacion_mascota(cursor):
    cursor.execute("SHOW COLUMNS FROM mascota")
    columnas = {columna["Field"] for columna in cursor.fetchall()}
    if "ubicacion" in columnas:
        return "ubicacion"
    if "ubicación" in columnas:
        return "ubicación"
    return None


def crear_mascota(id_usuario, nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado, ubicacion=None):
    with db_cursor(commit=True) as cursor:
        columna_ubicacion = _columna_ubicacion_mascota(cursor)
        columnas = ["id_usuario", "nombre_mascota", "raza", "edad", "color", "pelaje", "`tamaño`", "descripcion", "estado"]
        valores = [id_usuario, nombre_mascota, raza, edad, color, pelaje, tamano, descripcion, estado]

        if columna_ubicacion:
            columnas.insert(-1, f"`{columna_ubicacion}`")
            valores.insert(-1, ubicacion)

        placeholders = ", ".join(["%s"] * len(valores))
        sql = f"""
            INSERT INTO mascota
                ({", ".join(columnas)})
            VALUES ({placeholders})
        """
        cursor.execute(sql, valores)
        return cursor.lastrowid


def crear_fotos_mascota(id_mascota, urls_fotos):
    if not urls_fotos:
        return 0

    sql = "INSERT INTO foto_mascota (id_mascota, url_imagen) VALUES (%s, %s)"
    with db_cursor(commit=True) as cursor:
        cursor.executemany(sql, [(id_mascota, url_imagen) for url_imagen in urls_fotos])
        return cursor.rowcount


def listar_fotos_mascota(id_mascota):
    sql = """
        SELECT id_foto AS id_foto_mascota, url_imagen
        FROM foto_mascota
        WHERE id_mascota = %s
        ORDER BY id_foto ASC
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_mascota,))
        return cursor.fetchall()


def listar_mascotas_con_fotos():
    sql = """
        SELECT
            m.id_mascota,
            m.id_usuario,
            m.nombre_mascota,
            m.raza,
            m.edad,
            m.color,
            m.pelaje,
            m.`tamaño` AS tamano,
            m.descripcion,
            m.estado,
            u.nombre_completo AS nombre_dueno,
            fm.id_foto,
            fm.url_imagen
        FROM mascota m
        INNER JOIN foto_mascota fm ON fm.id_mascota = m.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
        WHERE fm.url_imagen IS NOT NULL AND fm.url_imagen <> ''
        ORDER BY m.id_mascota DESC, fm.id_foto ASC
    """
    with db_cursor() as cursor:
        cursor.execute(sql)
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
