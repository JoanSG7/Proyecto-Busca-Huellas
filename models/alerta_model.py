from config.database import db_cursor


def _columnas_alerta(cursor):
    """Mantiene las alertas operativas tanto antes como después de la migración."""
    cursor.execute("SHOW COLUMNS FROM alerta")
    return {columna["Field"] for columna in cursor.fetchall()}


def _insertar_alerta(cursor, id_usuario, id_mascota, tipo, confirmacion, mensaje):
    columnas_alerta = _columnas_alerta(cursor)
    columnas = ["id_usuario", "id_mascota", "estado_alerta", "confirmacion", "fecha_alerta"]
    valores = [id_usuario, id_mascota, tipo, confirmacion, "NOW()"]
    if "mensaje" in columnas_alerta:
        columnas.insert(4, "mensaje")
        valores.insert(4, mensaje)
    marcadores = ["NOW()" if valor == "NOW()" else "%s" for valor in valores]
    sql = f"INSERT INTO alerta ({', '.join(columnas)}) VALUES ({', '.join(marcadores)})"
    cursor.execute(sql, tuple(valor for valor in valores if valor != "NOW()"))
    return cursor.lastrowid


def crear_alerta(id_usuario, id_mascota, tipo, mensaje):
    with db_cursor(commit=True) as cursor:
        return _insertar_alerta(cursor, id_usuario, id_mascota, tipo, "no", mensaje)


def crear_alerta_coincidencia(id_reportante, id_mascota, nombre_mascota):
    """Crea una alerta confirmada que habilita el chat entre reportante y dueño."""
    sql_existente = """
        SELECT id_alerta
        FROM alerta
        WHERE id_usuario = %s AND id_mascota = %s AND estado_alerta = 'coincidencia_encontrada'
          AND estado_alerta_registro = 1
        ORDER BY id_alerta DESC
        LIMIT 1
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql_existente, (id_reportante, id_mascota))
        existente = cursor.fetchone()
        if existente:
            return existente["id_alerta"]
        return _insertar_alerta(
            cursor,
            id_reportante,
            id_mascota,
            "coincidencia_encontrada",
            "si",
            f"Nueva coincidencia encontrada: posible coincidencia con {nombre_mascota}.",
        )


def listar_alertas_usuario(id_usuario):
    with db_cursor() as cursor:
        columnas_alerta = _columnas_alerta(cursor)
        mensaje_sql = "a.mensaje" if "mensaje" in columnas_alerta else "NULL"
        sql = f"""
            SELECT
                a.id_alerta,
                a.id_usuario,
                a.id_mascota,
                a.estado_alerta AS tipo,
                a.confirmacion,
                {mensaje_sql} AS mensaje,
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
            WHERE a.estado_alerta_registro = 1
              AND m.estado_mascota = 1
              AND (a.id_usuario = %s OR m.id_usuario = %s OR a.id_usuario IS NULL)
            ORDER BY a.id_alerta DESC
        """
        cursor.execute(sql, (id_usuario, id_usuario))
        return cursor.fetchall()
