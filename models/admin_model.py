from config.database import db_cursor


from models.eliminacion_model import (
    desactivar_alerta,
    desactivar_articulo,
    desactivar_avistamiento,
    desactivar_informe,
    desactivar_mascota,
    desactivar_usuario,
    reactivar_articulo,
)


def _like(value):
    return f"%{value or ''}%"


def _where_text(fields, q, params):
    if not q:
        return None
    params.extend([_like(q)] * len(fields))
    return "(" + " OR ".join(f"{field} LIKE %s" for field in fields) + ")"


def listar_usuarios_admin(q="", rol="", eliminados=False):
    where = []
    params = []
    text_where = _where_text(["u.nombre_completo", "u.correo", "u.telefono"], q, params)
    if text_where:
        where.append(text_where)
    if rol:
        where.append("u.id_rol = %s")
        params.append(rol)
    where.insert(0, "u.estado_usuario = %s")
    params.insert(0, 0 if eliminados else 1)
    sql = """
        SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo, u.estado_usuario,
               u.foto_perfil, u.fecha_registro, r.nombre_rol,
               COUNT(CASE WHEN m.estado_mascota = 1 THEN m.id_mascota END) AS total_mascotas
        FROM usuario u
        LEFT JOIN rol r ON r.id_rol = u.id_rol
        LEFT JOIN mascota m ON m.id_usuario = u.id_usuario
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += """
        GROUP BY u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo, u.foto_perfil, u.fecha_registro, r.nombre_rol
        ORDER BY u.id_usuario DESC
    """
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_usuario_admin(id_usuario):
    sql = """
        SELECT u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo, u.estado_usuario,
               u.foto_perfil, u.fecha_registro, r.nombre_rol,
               COUNT(CASE WHEN m.estado_mascota = 1 THEN m.id_mascota END) AS total_mascotas
        FROM usuario u
        LEFT JOIN rol r ON r.id_rol = u.id_rol
        LEFT JOIN mascota m ON m.id_usuario = u.id_usuario
        WHERE u.id_usuario = %s
        GROUP BY u.id_usuario, u.id_rol, u.nombre_completo, u.telefono, u.correo, u.foto_perfil, u.fecha_registro, r.nombre_rol
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchone()


def actualizar_usuario_admin(id_usuario, nombre, telefono, correo, id_rol):
    sql = """
        UPDATE usuario
        SET nombre_completo = %s, telefono = %s, correo = %s, id_rol = %s
        WHERE id_usuario = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (nombre, telefono, correo, id_rol, id_usuario))
        return cursor.rowcount


def eliminar_usuario_admin(id_usuario):
    return desactivar_usuario(id_usuario)


def listar_articulos_admin(q="", filtro="", eliminados=False):
    params = [0 if eliminados else 1]
    where = ["a.estado_articulo = %s"]
    text_where = _where_text(["a.titulo", "a.contenido", "u.nombre_completo"], q, params)
    if text_where:
        where.append(text_where)
    sql = """
        SELECT a.id_articulo, a.id_usuario, a.titulo, a.contenido, a.url_imagen, a.estado_articulo,
               a.fecha_publicacion, u.nombre_completo AS nombre_usuario
        FROM articulo a
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE """ + " AND ".join(where) + " ORDER BY a.id_articulo DESC"
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_articulo_admin(id_articulo):
    sql = """
        SELECT a.id_articulo, a.id_usuario, a.titulo, a.contenido, a.url_imagen, a.estado_articulo,
               a.fecha_publicacion, u.nombre_completo AS nombre_usuario
        FROM articulo a
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE a.id_articulo = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_articulo,))
        return cursor.fetchone()


def actualizar_articulo_admin(id_articulo, titulo, contenido, url_imagen):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE articulo SET titulo = %s, contenido = %s, url_imagen = %s WHERE id_articulo = %s",
            (titulo, contenido, url_imagen or None, id_articulo),
        )
        return cursor.rowcount


def eliminar_articulo_admin(id_articulo):
    return desactivar_articulo(id_articulo)


def reactivar_articulo_admin(id_articulo):
    return reactivar_articulo(id_articulo)


def listar_mascotas_admin(q="", estado="", eliminados=False):
    where = []
    params = []
    text_where = _where_text(["m.nombre_mascota", "m.raza", "m.color", "m.pelaje", "u.nombre_completo"], q, params)
    if text_where:
        where.append(text_where)
    if estado:
        where.append("m.estado = %s")
        params.append(estado)
    where.insert(0, "m.estado_mascota = %s")
    params.insert(0, 0 if eliminados else 1)
    sql = """
        SELECT m.id_mascota, m.id_usuario, m.nombre_mascota, m.raza, m.edad, m.estado_mascota,
               m.color, m.pelaje, m.`tamaño` AS tamano, m.descripcion, m.estado,
               m.fecha_registro, u.nombre_completo AS nombre_usuario
        FROM mascota m
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY m.id_mascota DESC"
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_mascota_admin(id_mascota):
    sql = """
        SELECT m.id_mascota, m.id_usuario, m.nombre_mascota, m.raza, m.edad, m.estado_mascota,
               m.color, m.pelaje, m.`tamaño` AS tamano, m.descripcion, m.estado,
               m.fecha_registro, u.nombre_completo AS nombre_usuario, u.correo AS correo_usuario
        FROM mascota m
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
        WHERE m.id_mascota = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_mascota,))
        return cursor.fetchone()


def actualizar_mascota_admin(id_mascota, id_usuario, nombre, raza, edad, color, pelaje, tamano, descripcion, estado):
    sql = """
        UPDATE mascota
        SET id_usuario = %s, nombre_mascota = %s, raza = %s, edad = %s, color = %s,
            pelaje = %s, `tamaño` = %s, descripcion = %s, estado = %s
        WHERE id_mascota = %s
    """
    params = (id_usuario, nombre, raza, edad, color, pelaje, tamano, descripcion, estado, id_mascota)
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, params)
        return cursor.rowcount


def eliminar_mascota_admin(id_mascota):
    return desactivar_mascota(id_mascota)


def listar_alertas_admin(q="", estado="", eliminados=False):
    where = []
    params = []
    text_where = _where_text(["a.estado_alerta", "a.confirmacion", "m.nombre_mascota", "u.nombre_completo"], q, params)
    if text_where:
        where.append(text_where)
    if estado:
        where.append("a.estado_alerta = %s")
        params.append(estado)
    where.insert(0, "a.estado_alerta_registro = %s")
    params.insert(0, 0 if eliminados else 1)
    sql = """
        SELECT a.id_alerta, a.id_usuario, a.id_mascota, a.estado_alerta, a.estado_alerta_registro,
               a.confirmacion, a.fecha_alerta,
               m.nombre_mascota, u.nombre_completo AS nombre_usuario
        FROM alerta a
        LEFT JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY a.id_alerta DESC"
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_alerta_admin(id_alerta):
    sql = """
        SELECT a.id_alerta, a.id_usuario, a.id_mascota, a.estado_alerta, a.estado_alerta_registro,
               a.confirmacion, a.fecha_alerta,
               m.nombre_mascota, u.nombre_completo AS nombre_usuario
        FROM alerta a
        LEFT JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
        WHERE a.id_alerta = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_alerta,))
        return cursor.fetchone()


def actualizar_alerta_admin(id_alerta, id_usuario, id_mascota, estado_alerta, confirmacion):
    sql = """
        UPDATE alerta
        SET id_usuario = %s, id_mascota = %s, estado_alerta = %s, confirmacion = %s
        WHERE id_alerta = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_usuario or None, id_mascota or None, estado_alerta, confirmacion, id_alerta))
        return cursor.rowcount


def eliminar_alerta_admin(id_alerta):
    return desactivar_alerta(id_alerta)


def listar_avistamientos_admin(q="", estado="", eliminados=False):
    where = []
    params = []
    text_where = _where_text(["av.ubicacion", "av.descripcion_avistamiento", "m.nombre_mascota"], q, params)
    if text_where:
        where.append(text_where)
    if estado == "confirmados":
        where.append("av.id_mascota IS NOT NULL")
    elif estado == "sin_confirmar":
        where.append("av.id_mascota IS NULL")
    where.insert(0, "av.estado_avistamiento = %s")
    params.insert(0, 0 if eliminados else 1)
    sql = """
        SELECT av.id_avistamiento, av.id_mascota, av.ubicacion, av.descripcion_avistamiento, av.estado_avistamiento,
               av.url_imagen, av.fecha_avistamiento, m.nombre_mascota,
               u.id_usuario AS id_dueno, u.nombre_completo AS nombre_dueno
        FROM avistamiento av
        LEFT JOIN mascota m ON m.id_mascota = av.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY av.id_avistamiento DESC"
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_avistamiento_admin(id_avistamiento):
    sql = """
        SELECT av.id_avistamiento, av.id_mascota, av.ubicacion, av.descripcion_avistamiento, av.estado_avistamiento,
               av.url_imagen, av.fecha_avistamiento, m.nombre_mascota,
               u.id_usuario AS id_dueno, u.nombre_completo AS nombre_dueno
        FROM avistamiento av
        LEFT JOIN mascota m ON m.id_mascota = av.id_mascota
        LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
        WHERE av.id_avistamiento = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_avistamiento,))
        return cursor.fetchone()


def actualizar_avistamiento_admin(id_avistamiento, id_mascota, ubicacion, descripcion, url_imagen, fecha):
    sql = """
        UPDATE avistamiento
        SET id_mascota = %s, ubicacion = %s, descripcion_avistamiento = %s,
            url_imagen = %s, fecha_avistamiento = %s
        WHERE id_avistamiento = %s
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_mascota or None, ubicacion, descripcion, url_imagen, fecha or None, id_avistamiento))
        return cursor.rowcount


def eliminar_avistamiento_admin(id_avistamiento):
    return desactivar_avistamiento(id_avistamiento)


def listar_informes_admin(q="", tipo="", eliminados=False):
    where = []
    params = []
    text_where = _where_text(["i.tipo_informe", "i.descripcion", "u.nombre_completo"], q, params)
    if text_where:
        where.append(text_where)
    if tipo:
        where.append("i.tipo_informe = %s")
        params.append(tipo)
    where.insert(0, "i.estado_informe = %s")
    params.insert(0, 0 if eliminados else 1)
    sql = """
        SELECT i.id_informe, i.id_usuario, i.tipo_informe, i.descripcion, i.fecha_generacion, i.estado_informe,
               u.nombre_completo AS nombre_usuario
        FROM informe i
        LEFT JOIN usuario u ON u.id_usuario = i.id_usuario
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY i.id_informe DESC"
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def obtener_informe_admin(id_informe):
    sql = """
        SELECT i.id_informe, i.id_usuario, i.tipo_informe, i.descripcion, i.fecha_generacion, i.estado_informe,
               u.nombre_completo AS nombre_usuario
        FROM informe i
        LEFT JOIN usuario u ON u.id_usuario = i.id_usuario
        WHERE i.id_informe = %s
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_informe,))
        return cursor.fetchone()


def crear_informe_admin(id_usuario, tipo_informe, descripcion):
    sql = """
        INSERT INTO informe (id_usuario, tipo_informe, descripcion, fecha_generacion)
        VALUES (%s, %s, %s, NOW())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_usuario, tipo_informe, descripcion))
        return cursor.lastrowid


def actualizar_informe_admin(id_informe, tipo_informe, descripcion):
    sql = "UPDATE informe SET tipo_informe = %s, descripcion = %s WHERE id_informe = %s"
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (tipo_informe, descripcion, id_informe))
        return cursor.rowcount


def eliminar_informe_admin(id_informe):
    return desactivar_informe(id_informe)


def obtener_resumen_admin():
    consultas = {
        "usuarios": "SELECT COUNT(*) AS total FROM usuario",
        "mascotas": "SELECT COUNT(*) AS total FROM mascota",
        "alertas": "SELECT COUNT(*) AS total FROM alerta",
        "avistamientos": "SELECT COUNT(*) AS total FROM avistamiento",
        "informes": "SELECT COUNT(*) AS total FROM informe",
        "avistamientos_confirmados": "SELECT COUNT(*) AS total FROM avistamiento WHERE id_mascota IS NOT NULL",
    }
    resumen = {}
    with db_cursor() as cursor:
        for clave, sql in consultas.items():
            cursor.execute(sql)
            resumen[clave] = (cursor.fetchone() or {}).get("total", 0)
    return resumen


def generar_datos_informe(tipo, fecha_inicio=None, fecha_fin=None, limite=5):
    limite = max(1, min(int(limite or 5), 100))
    params = []
    if tipo == "mascotas_por_fecha":
        sql = """
            SELECT m.id_mascota, m.nombre_mascota, m.estado, m.raza, m.fecha_registro,
                   u.nombre_completo AS usuario
            FROM mascota m
            LEFT JOIN usuario u ON u.id_usuario = m.id_usuario
            WHERE (%s IS NULL OR m.fecha_registro >= %s)
              AND (%s IS NULL OR m.fecha_registro <= %s)
            ORDER BY m.fecha_registro DESC, m.id_mascota DESC
            LIMIT %s
        """
        params.extend([fecha_inicio or None, fecha_inicio or None, fecha_fin or None, fecha_fin or None, limite])
    elif tipo == "alertas_por_fecha":
        sql = """
            SELECT a.id_alerta, a.estado_alerta, a.confirmacion, a.fecha_alerta,
                   m.nombre_mascota, u.nombre_completo AS usuario
            FROM alerta a
            LEFT JOIN mascota m ON m.id_mascota = a.id_mascota
            LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
            WHERE (%s IS NULL OR DATE(a.fecha_alerta) >= %s)
              AND (%s IS NULL OR DATE(a.fecha_alerta) <= %s)
            ORDER BY a.fecha_alerta DESC
            LIMIT %s
        """
        params.extend([fecha_inicio or None, fecha_inicio or None, fecha_fin or None, fecha_fin or None, limite])
    elif tipo == "top_usuarios_avistamientos":
        sql = """
            SELECT u.id_usuario, u.nombre_completo, u.correo, COUNT(av.id_avistamiento) AS total_avistamientos
            FROM usuario u
            INNER JOIN mascota m ON m.id_usuario = u.id_usuario
            INNER JOIN avistamiento av ON av.id_mascota = m.id_mascota
            WHERE av.id_mascota IS NOT NULL
            GROUP BY u.id_usuario, u.nombre_completo, u.correo
            ORDER BY total_avistamientos DESC
            LIMIT %s
        """
        params.append(limite)
    else:
        sql = """
            SELECT id_usuario, nombre_completo, correo, telefono, fecha_registro
            FROM usuario
            WHERE (%s IS NULL OR fecha_registro >= %s)
              AND (%s IS NULL OR fecha_registro <= %s)
            ORDER BY fecha_registro DESC, id_usuario DESC
            LIMIT %s
        """
        params.extend([fecha_inicio or None, fecha_inicio or None, fecha_fin or None, fecha_fin or None, limite])
    with db_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

