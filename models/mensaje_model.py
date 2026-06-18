from config.database import db_cursor


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
            MAX(ms.fecha_envio) AS ultimo_mensaje
        FROM alerta a
        INNER JOIN mascota m ON m.id_mascota = a.id_mascota
        LEFT JOIN usuario dueno ON dueno.id_usuario = m.id_usuario
        LEFT JOIN usuario alerta_usuario ON alerta_usuario.id_usuario = a.id_usuario
        LEFT JOIN mensaje ms ON ms.id_alerta = a.id_alerta
        WHERE a.confirmacion = 'si'
          AND (%s = TRUE OR a.id_usuario = %s OR m.id_usuario = %s
               OR ms.usuario_emisor = %s OR ms.usuario_receptor = %s)
        GROUP BY a.id_alerta, a.id_usuario, a.id_mascota, a.estado_alerta, a.confirmacion,
                 a.fecha_alerta, m.nombre_mascota, m.id_usuario, dueno.nombre_completo,
                 alerta_usuario.nombre_completo
        ORDER BY COALESCE(MAX(ms.fecha_envio), a.fecha_alerta) DESC
    """
    params = (es_admin, id_usuario, id_usuario, id_usuario, id_usuario)
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
          AND (%s = TRUE OR a.id_usuario = %s OR m.id_usuario = %s)
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_alerta, es_admin, id_usuario, id_usuario))
        return cursor.fetchone()


def listar_mensajes_alerta(id_alerta):
    sql = """
        SELECT ms.id_mensaje, ms.id_alerta, ms.usuario_emisor, ms.usuario_receptor,
               ms.mensaje_chat, ms.fecha_envio, emisor.nombre_completo AS nombre_emisor,
               receptor.nombre_completo AS nombre_receptor
        FROM mensaje ms
        LEFT JOIN usuario emisor ON emisor.id_usuario = ms.usuario_emisor
        LEFT JOIN usuario receptor ON receptor.id_usuario = ms.usuario_receptor
        WHERE ms.id_alerta = %s
        ORDER BY ms.fecha_envio ASC, ms.id_mensaje ASC
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_alerta,))
        return cursor.fetchall()


def crear_mensaje_alerta(id_alerta, usuario_emisor, usuario_receptor, mensaje):
    sql = """
        INSERT INTO mensaje (id_alerta, usuario_emisor, usuario_receptor, mensaje_chat, fecha_envio)
        VALUES (%s, %s, %s, %s, NOW())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_alerta, usuario_emisor, usuario_receptor, mensaje))
        return cursor.lastrowid
