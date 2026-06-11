from config.database import db_cursor


def obtener_estadisticas_inicio():
    consultas = {
        "mascotas_reencontradas": """
            SELECT COUNT(*) AS total
            FROM mascota
            WHERE LOWER(estado) = 'encontrada'
        """,
        "voluntarios_activos": """
            SELECT COUNT(*) AS total
            FROM usuario
            WHERE id_rol = 1
        """,
        "hogares_felices": """
            SELECT COUNT(*) AS total
            FROM mascota
            WHERE LOWER(estado) = 'adoptada'
        """,
        "reportes_activos_hoy": """
            SELECT COUNT(*) AS total
            FROM mascota
            WHERE LOWER(estado) = 'perdida'
        """,
    }

    estadisticas = {}
    with db_cursor() as cursor:
        for clave, sql in consultas.items():
            cursor.execute(sql)
            fila = cursor.fetchone() or {}
            estadisticas[clave] = fila.get("total", 0)

    return estadisticas
