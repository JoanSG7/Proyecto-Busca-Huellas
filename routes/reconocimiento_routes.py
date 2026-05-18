from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_capturar_foto

reconocimiento_bp = Blueprint('reconocimiento', __name__)

# modulo reconocimiento
@reconocimiento_bp.route('/capturar-foto')
def capturar_foto():
    return mostrar_capturar_foto()