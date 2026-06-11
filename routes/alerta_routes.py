from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import listar_alertas_json, mostrar_lista_alertas
from controllers.security import login_required

alerta_bp = Blueprint('alerta', __name__)

# modulo alerta
@alerta_bp.route('/lista')
@login_required
def alertas():
    return mostrar_lista_alertas()


@alerta_bp.route('/api')
@login_required
def api_alertas():
    return listar_alertas_json()
