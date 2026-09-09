from config.database import db_cursor


def confirmar_avistamiento(id_avistamiento, id_usuario_alerto, id_usuario_dueno, id_mascota):
    """Registra una sola confirmación por avistamiento y devuelve True si fue nueva."""
    sql = """
        INSERT IGNORE INTO avistamiento_confirmado
            (id_avistamiento, id_usuario_alerto, id_usuario_dueno, id_mascota, fecha_confirmacion)
        VALUES (%s, %s, %s, %s, NOW())
    """
    with db_cursor(commit=True) as cursor:
        cursor.execute(sql, (id_avistamiento, id_usuario_alerto, id_usuario_dueno, id_mascota))
        return cursor.rowcount > 0


def obtener_avistamiento_confirmable(id_avistamiento, id_alerta, id_mascota, id_usuario_alerto, id_usuario_dueno):
    sql = """
        SELECT id_avistamiento
        FROM avistamiento
        WHERE id_avistamiento = %s
          AND id_alerta = %s
          AND id_mascota = %s
          AND estado_avistamiento = 1
        LIMIT 1
    """
    with db_cursor() as cursor:
        cursor.execute(sql, (id_avistamiento, id_alerta, id_mascota))
        return cursor.fetchone()
