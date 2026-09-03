from config.database import db_cursor


def obtener_estadisticas_inicio():
    consultas = {
        "mascotas_reencontradas": """
            SELECT COUNT(*) AS total
            FROM mascota
            WHERE LOWER(estado) = 'encontrada'
              AND estado_mascota = 1
        """,
        "voluntarios_activos": """
            SELECT COUNT(*) AS total
            FROM usuario
            WHERE id_rol = 1
              AND estado_usuario = 1
        """,
        "colaboradores_activos": """
            SELECT COUNT(*) AS total
            FROM usuario
            WHERE id_rol = 1
              AND estado_usuario = 1
        """,
        "reportes_activos_hoy": """
            SELECT COUNT(*) AS total
            FROM mascota
            WHERE LOWER(estado) = 'perdida'
              AND estado_mascota = 1
              AND DATE(fecha_registro) = CURDATE()
        """,
    }

    estadisticas = {}
    with db_cursor() as cursor:
        for clave, sql in consultas.items():
            cursor.execute(sql)
            fila = cursor.fetchone() or {}
            estadisticas[clave] = fila.get("total", 0)

    return estadisticas
