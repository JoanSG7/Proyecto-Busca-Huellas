from config.database import db_cursor


def crear_avistamiento(id_alerta, id_mascota, ubicacion, descripcion, url_imagen):
    sql = """
        INSERT INTO avistamiento
            (id_alerta, id_mascota, ubicacion, descripcion_avistamiento, url_imagen, fecha_avistamiento)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_alerta, id_mascota, ubicacion, descripcion, url_imagen))
        return cursor.lastrowid


def obtener_imagen_avistamiento(id_alerta):
    sql = """
        SELECT url_imagen
        FROM avistamiento
        WHERE id_alerta = %s AND estado_avistamiento = 1
        ORDER BY id_avistamiento DESC
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_alerta,))
        avistamiento = cursor.fetchone()
        return avistamiento["url_imagen"] if avistamiento else None
