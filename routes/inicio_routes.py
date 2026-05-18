from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_inicio

inicio_bp = Blueprint('inicio', __name__)

# modulo inicio
@inicio_bp.route('/inicio')
def inicio():
    return mostrar_inicio()