from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import borrar_articulo, editar_articulo, mostrar_lista_articulos, mostrar_articulo_completo, registrar_articulo
from controllers.security import admin_required, login_required

articulo_bp = Blueprint('articulo', __name__)

# modulo articulo
@articulo_bp.route('/lista')
@login_required
def lista_articulos():
    return mostrar_lista_articulos()

@articulo_bp.route('/articulo/<int:id_articulo>')
@login_required
def articulo_completo(id_articulo):
    return mostrar_articulo_completo(id_articulo)

@articulo_bp.route('/crear', methods=['POST'])
@admin_required
def crear():
    return registrar_articulo()

@articulo_bp.route('/editar/<int:id_articulo>', methods=['POST'])
@admin_required
def editar(id_articulo):
    return editar_articulo(id_articulo)

@articulo_bp.route('/eliminar/<int:id_articulo>', methods=['POST'])
@admin_required
def eliminar(id_articulo):
    return borrar_articulo(id_articulo)
