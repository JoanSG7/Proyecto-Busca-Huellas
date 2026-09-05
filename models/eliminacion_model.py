"""Operaciones de eliminación lógica (estado 0) para los registros del sistema."""

from config.database import db_cursor


def desactivar_mascota(id_mascota):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE mascota SET estado_mascota = 0 WHERE id_mascota = %s AND estado_mascota = 1",
            (id_mascota,),
        )
        return cursor.rowcount


def desactivar_alerta(id_alerta):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE alerta SET estado_alerta_registro = 0 WHERE id_alerta = %s AND estado_alerta_registro = 1",
            (id_alerta,),
        )
        return cursor.rowcount


def desactivar_avistamiento(id_avistamiento):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE avistamiento SET estado_avistamiento = 0 WHERE id_avistamiento = %s AND estado_avistamiento = 1",
            (id_avistamiento,),
        )
        return cursor.rowcount


def desactivar_articulo(id_articulo):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE articulo SET estado_articulo = 0 WHERE id_articulo = %s AND estado_articulo = 1",
            (id_articulo,),
        )
        return cursor.rowcount


def reactivar_articulo(id_articulo):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE articulo SET estado_articulo = 1 WHERE id_articulo = %s AND estado_articulo = 0",
            (id_articulo,),
        )
        return cursor.rowcount


def reactivar_usuario(id_usuario):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "SELECT id_mascota FROM mascota WHERE id_usuario = %s",
            (id_usuario,),
        )
        mascotas = [fila["id_mascota"] for fila in cursor.fetchall()]

        cursor.execute(
            "UPDATE usuario SET estado_usuario = 1 WHERE id_usuario = %s AND estado_usuario = 0",
            (id_usuario,),
        )
        usuario_actualizado = cursor.rowcount

        cursor.execute("UPDATE articulo SET estado_articulo = 1 WHERE id_usuario = %s", (id_usuario,))
        cursor.execute("UPDATE informe SET estado_informe = 1 WHERE id_usuario = %s", (id_usuario,))
        cursor.execute("UPDATE alerta SET estado_alerta_registro = 1 WHERE id_usuario = %s", (id_usuario,))

        if mascotas:
            marcadores = ", ".join(["%s"] * len(mascotas))
            cursor.execute(
                f"UPDATE alerta SET estado_alerta_registro = 1 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
            cursor.execute(
                f"UPDATE avistamiento SET estado_avistamiento = 1 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
            cursor.execute(
                f"UPDATE mascota SET estado_mascota = 1 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
        return usuario_actualizado


def reactivar_mascota(id_mascota):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE mascota SET estado_mascota = 1 WHERE id_mascota = %s AND estado_mascota = 0",
            (id_mascota,),
        )
        return cursor.rowcount


def reactivar_alerta(id_alerta):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE alerta SET estado_alerta_registro = 1 WHERE id_alerta = %s AND estado_alerta_registro = 0",
            (id_alerta,),
        )
        return cursor.rowcount


def reactivar_avistamiento(id_avistamiento):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE avistamiento SET estado_avistamiento = 1 WHERE id_avistamiento = %s AND estado_avistamiento = 0",
            (id_avistamiento,),
        )
        return cursor.rowcount


def reactivar_avistamiento_confirmado(id_avistamiento_confirmado):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE avistamiento_confirmado SET estado_confirmacion = 1 WHERE id_confirmacion = %s AND estado_confirmacion = 0",
            (id_avistamiento_confirmado,),
        )
        return cursor.rowcount


def reactivar_informe(id_informe):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE informe SET estado_informe = 1 WHERE id_informe = %s AND estado_informe = 0",
            (id_informe,),
        )
        return cursor.rowcount


def desactivar_informe(id_informe):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE informe SET estado_informe = 0 WHERE id_informe = %s AND estado_informe = 1",
            (id_informe,),
        )
        return cursor.rowcount


def desactivar_usuario(id_usuario):
    """Desactiva una cuenta y todos los registros que le pertenecen."""
    with db_cursor(commit=True) as cursor:
        cursor.execute("SELECT id_mascota FROM mascota WHERE id_usuario = %s", (id_usuario,))
        mascotas = [fila["id_mascota"] for fila in cursor.fetchall()]

        cursor.execute(
            "UPDATE usuario SET estado_usuario = 0 WHERE id_usuario = %s AND estado_usuario = 1",
            (id_usuario,),
        )
        usuario_actualizado = cursor.rowcount

        cursor.execute("UPDATE articulo SET estado_articulo = 0 WHERE id_usuario = %s", (id_usuario,))
        cursor.execute("UPDATE informe SET estado_informe = 0 WHERE id_usuario = %s", (id_usuario,))
        cursor.execute("UPDATE alerta SET estado_alerta_registro = 0 WHERE id_usuario = %s", (id_usuario,))

        if mascotas:
            marcadores = ", ".join(["%s"] * len(mascotas))
            cursor.execute(
                f"UPDATE alerta SET estado_alerta_registro = 0 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
            cursor.execute(
                f"UPDATE avistamiento SET estado_avistamiento = 0 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
            cursor.execute(
                f"UPDATE mascota SET estado_mascota = 0 WHERE id_mascota IN ({marcadores})",
                tuple(mascotas),
            )
        return usuario_actualizado
