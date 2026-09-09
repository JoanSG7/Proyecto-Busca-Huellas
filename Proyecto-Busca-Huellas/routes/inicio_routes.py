from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_inicio, obtener_estadisticas_inicio_json
from controllers.security import login_required

inicio_bp = Blueprint('inicio', __name__)

# modulo inicio
@inicio_bp.route('/inicio')
@login_required
def inicio():
    return mostrar_inicio()


@inicio_bp.route('/inicio/estadisticas')
@login_required
def estadisticas():
    return obtener_estadisticas_inicio_json()
