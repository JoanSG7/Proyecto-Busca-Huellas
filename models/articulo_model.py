from config.database import db_cursor
from models.eliminacion_model import desactivar_articulo


def listar_articulos():
    sql = """
        SELECT a.id_articulo, a.id_usuario, a.titulo, a.contenido, a.url_imagen,
               a.fecha_publicacion, u.nombre_completo AS autor
        FROM articulo a
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE a.estado_articulo = 1
        ORDER BY a.fecha_publicacion DESC, a.id_articulo DESC
    """
    with db_cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def obtener_articulo(id_articulo):
    sql = """
        SELECT a.id_articulo, a.id_usuario, a.titulo, a.contenido, a.url_imagen,
               a.fecha_publicacion, u.nombre_completo AS autor
        FROM articulo a
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE a.id_articulo = %s AND a.estado_articulo = 1
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_articulo,))
        return cursor.fetchone()


def crear_articulo(id_usuario, titulo, contenido, url_imagen=None):
    sql = """
        INSERT INTO articulo (id_usuario, titulo, contenido, url_imagen, fecha_publicacion)
        VALUES (%s, %s, %s, %s, CURDATE())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_usuario, titulo, contenido, url_imagen))
        return cursor.lastrowid


def actualizar_articulo(id_articulo, titulo, contenido, url_imagen=None):
    sql = """
        UPDATE articulo
        SET titulo = %s, contenido = %s, url_imagen = %s
        WHERE id_articulo = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (titulo, contenido, url_imagen, id_articulo))
        return cursor.rowcount


def eliminar_articulo(id_articulo):
    return desactivar_articulo(id_articulo)
