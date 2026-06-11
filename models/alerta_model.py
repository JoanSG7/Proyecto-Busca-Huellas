from config.database import db_cursor


def crear_alerta(id_usuario, id_mascota, tipo, mensaje):
    sql = """
        INSERT INTO alerta (id_usuario, id_mascota, estado_alerta, confirmacion, fecha_alerta)
        VALUES (%s, %s, %s, %s, CURDATE())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_usuario, id_mascota, tipo, "no"))
        return cursor.lastrowid


def listar_alertas_usuario(id_usuario):
    sql = """
        SELECT
            a.id_alerta,
            a.id_usuario,
            a.id_mascota,
            a.estado_alerta AS tipo,
            a.confirmacion AS mensaje,
            a.fecha_alerta,
            m.nombre_mascota,
            m.estado AS estado_mascota,
            u.nombre_completo AS nombre_usuario,
            (
                SELECT fm.url_imagen
                FROM foto_mascota fm
                WHERE fm.id_mascota = a.id_mascota
                ORDER BY fm.id_foto ASC
                LIMIT 1
            ) AS url_imagen
        FROM alerta a
        LEFT JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE a.id_usuario = %s OR a.id_usuario IS NULL
        ORDER BY a.id_alerta DESC
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchall()
