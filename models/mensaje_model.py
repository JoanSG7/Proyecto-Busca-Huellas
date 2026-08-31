from config.database import db_cursor


def _columnas_mensaje(cursor):
    cursor.execute("SHOW COLUMNS FROM mensaje")
    return {columna["Field"] for columna in cursor.fetchall()}


def listar_chats_alerta(id_usuario, es_admin=False):
    sql = """
        SELECT
            a.id_alerta,
            a.id_usuario AS id_usuario_alerta,
            a.id_mascota,
            a.estado_alerta,
            a.confirmacion,
            a.fecha_alerta,
            m.nombre_mascota,
            m.id_usuario AS id_dueno,
            dueno.nombre_completo AS nombre_dueno,
            alerta_usuario.nombre_completo AS nombre_alerta_usuario,
            NULL AS ultimo_mensaje
        FROM alerta a
        INNER JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario dueno ON dueno.id_usuario = m.id_usuario
        LEFT JOIN usuario alerta_usuario ON alerta_usuario.id_usuario = a.id_usuario
        WHERE a.id_alerta IN (
            SELECT MAX(a2.id_alerta)
            FROM alerta a2
            INNER JOIN mascota m2 ON m2.id_mascota = a2.id_mascota
            WHERE a2.confirmacion = 'si'
              AND a2.estado_alerta = 'coincidencia_encontrada'
              AND (a2.id_usuario = %s OR m2.id_usuario = %s)
            GROUP BY LEAST(a2.id_usuario, m2.id_usuario), GREATEST(a2.id_usuario, m2.id_usuario)
        )
          AND NOT EXISTS (
              SELECT 1
              FROM chat_eliminado ce
              WHERE ce.id_alerta = a.id_alerta AND ce.id_usuario = %s
          )
        ORDER BY a.fecha_alerta DESC
    """
    params = (id_usuario, id_usuario, id_usuario)
    with db_cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def obtener_chat_alerta(id_alerta, id_usuario, es_admin=False):
    sql = """
        SELECT
            a.id_alerta,
            a.id_usuario AS id_usuario_alerta,
            a.id_mascota,
            a.estado_alerta,
            a.confirmacion,
            a.fecha_alerta,
            m.nombre_mascota,
            m.id_usuario AS id_dueno,
            dueno.nombre_completo AS nombre_dueno,
            alerta_usuario.nombre_completo AS nombre_alerta_usuario
        FROM alerta a
        INNER JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario dueno ON dueno.id_usuario = m.id_usuario
        LEFT JOIN usuario alerta_usuario ON alerta_usuario.id_usuario = a.id_usuario
        WHERE a.id_alerta = %s
          AND a.confirmacion = 'si'
          AND a.estado_alerta = 'coincidencia_encontrada'
          AND (a.id_usuario = %s OR m.id_usuario = %s)
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_alerta, id_usuario, id_usuario))
        return cursor.fetchone()


def listar_mensajes_alerta(usuario_uno, usuario_dos):
    sql = """
        SELECT ms.id_mensaje, ms.id_alerta, ms.usuario_emisor, ms.usuario_receptor,
               ms.mensaje_chat, ms.fecha_envio, emisor.nombre_completo AS nombre_emisor,
               receptor.nombre_completo AS nombre_receptor,
               av.id_avistamiento, av.ubicacion AS ubicacion_avistamiento,
               ac.id_confirmacion
        FROM mensaje ms
        LEFT JOIN usuario emisor ON emisor.id_usuario = ms.usuario_emisor
        LEFT JOIN usuario receptor ON receptor.id_usuario = ms.usuario_receptor
        LEFT JOIN avistamiento av ON av.id_alerta = ms.id_alerta
            AND av.estado_avistamiento = 1
        LEFT JOIN avistamiento_confirmado ac ON ac.id_avistamiento = av.id_avistamiento
        WHERE (ms.usuario_emisor = %s AND ms.usuario_receptor = %s)
           OR (ms.usuario_emisor = %s AND ms.usuario_receptor = %s)
        ORDER BY ms.fecha_envio ASC, ms.id_mensaje ASC
    """
    with db_cursor() as cursor:
        columnas = _columnas_mensaje(cursor)
        imagen_sql = "ms.url_imagen," if "url_imagen" in columnas else "NULL AS url_imagen,"
        sql = sql.replace("ms.mensaje_chat, ms.fecha_envio", f"ms.mensaje_chat, {imagen_sql} ms.fecha_envio")
        cursor.execute(sql, (usuario_uno, usuario_dos, usuario_dos, usuario_uno))
        return cursor.fetchall()


def crear_mensaje_alerta(id_alerta, usuario_emisor, usuario_receptor, mensaje, url_imagen=None):
    with db_cursor(commit=True) as cursor:
        columnas = ["id_alerta", "usuario_emisor", "usuario_receptor", "mensaje_chat", "fecha_envio"]
        valores = [id_alerta, usuario_emisor, usuario_receptor, mensaje, "NOW()"]
        if "url_imagen" in _columnas_mensaje(cursor):
            columnas.insert(4, "url_imagen")
            valores.insert(4, url_imagen)
        marcadores = ["NOW()" if valor == "NOW()" else "%s" for valor in valores]
        sql = f"INSERT INTO mensaje ({', '.join(columnas)}) VALUES ({', '.join(marcadores)})"
        cursor.execute(sql, tuple(valor for valor in valores if valor != "NOW()"))
        return cursor.lastrowid


def eliminar_chat_para_usuario(id_alerta, id_usuario):
    """Oculta el chat solo para quien lo elimina, sin afectar al otro participante."""
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """INSERT IGNORE INTO chat_eliminado (id_alerta, id_usuario, fecha_eliminacion)
               VALUES (%s, %s, NOW())""",
            (id_alerta, id_usuario),
        )
        return cursor.rowcount > 0
