from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_lista_articulos

articulo_bp = Blueprint('articulo', __name__)

# modulo usuario
@articulo_bp.route('/lista')
def lista_articulos():
    return mostrar_lista_articulos()