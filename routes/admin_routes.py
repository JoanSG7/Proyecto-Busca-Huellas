from flask import Blueprint

from controllers.admin_controller import (
    exportar_informe_admin,
    eliminar_item_admin,
    generar_informe_admin,
    guardar_detalle_admin,
    mostrar_admin,
    mostrar_detalle_admin,
)
from controllers.security import admin_required


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_bp.route("/<seccion>")
@admin_required
def panel(seccion="usuarios"):
    return mostrar_admin(seccion)


@admin_bp.route("/<seccion>/<int:item_id>")
@admin_required
def detalle(seccion, item_id):
    return mostrar_detalle_admin(seccion, item_id)


@admin_bp.route("/<seccion>/<int:item_id>/guardar", methods=["POST"])
@admin_required
def guardar(seccion, item_id):
    return guardar_detalle_admin(seccion, item_id)


@admin_bp.route("/<seccion>/<int:item_id>/eliminar", methods=["POST"])
@admin_required
def eliminar(seccion, item_id):
    return eliminar_item_admin(seccion, item_id)


@admin_bp.route("/informes/generar", methods=["POST"])
@admin_required
def generar_informe():
    return generar_informe_admin()


@admin_bp.route("/informes/exportar/<formato>")
@admin_required
def exportar_informe(formato):
    return exportar_informe_admin(formato)
