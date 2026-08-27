from config.database import db_cursor


def _columnas_alerta(cursor):
    """Mantiene las alertas operativas tanto antes como después de la migración."""
    cursor.execute("SHOW COLUMNS FROM alerta")
    return {columna["Field"] for columna in cursor.fetchall()}


def _insertar_alerta(cursor, id_usuario, id_mascota, tipo, confirmacion, mensaje, id_alerta_origen=None):
    columnas_alerta = _columnas_alerta(cursor)
    columnas = ["id_usuario", "id_mascota", "estado_alerta", "confirmacion", "fecha_alerta"]
    valores = [id_usuario, id_mascota, tipo, confirmacion, "NOW()"]
    if "mensaje" in columnas_alerta:
        columnas.insert(4, "mensaje")
        valores.insert(4, mensaje)
    if "id_alerta_origen" in columnas_alerta:
        columnas.insert(2, "id_alerta_origen")
        valores.insert(2, id_alerta_origen)
    marcadores = ["NOW()" if valor == "NOW()" else "%s" for valor in valores]
    sql = f"INSERT INTO alerta ({', '.join(columnas)}) VALUES ({', '.join(marcadores)})"
    cursor.execute(sql, tuple(valor for valor in valores if valor != "NOW()"))
    return cursor.lastrowid


def crear_alerta(id_usuario, id_mascota, tipo, mensaje, id_alerta_origen=None):
    with db_cursor(commit=True) as cursor:
        return _insertar_alerta(cursor, id_usuario, id_mascota, tipo, "no", mensaje, id_alerta_origen)


def crear_alerta_coincidencia(id_reportante, id_mascota, nombre_mascota):
    """Registra cada coincidencia para conservar todos los reportes enviados."""
    with db_cursor(commit=True) as cursor:
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
        alerta_origen_sql = "a.id_alerta_origen" if "id_alerta_origen" in columnas_alerta else "NULL"
        sql = f"""
            SELECT
                a.id_alerta,
                a.id_usuario,
                a.id_mascota,
                a.estado_alerta AS tipo,
                a.confirmacion,
                {mensaje_sql} AS mensaje,
                {alerta_origen_sql} AS id_alerta_origen,
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
              AND (m.id_mascota IS NULL OR m.estado_mascota = 1)
              AND (a.id_usuario = %s OR m.id_usuario = %s OR a.id_usuario IS NULL)
            ORDER BY a.id_alerta DESC
        """
        cursor.execute(sql, (id_usuario, id_usuario))
        return cursor.fetchall()
