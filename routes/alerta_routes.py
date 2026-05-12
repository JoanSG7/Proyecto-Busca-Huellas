from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_lista_alertas

alerta_bp = Blueprint('alerta', __name__)

@alerta_bp.route('/lista')
def alertas():
    return mostrar_lista_alertas()