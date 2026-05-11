from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_adopcion

adopcion_bp = Blueprint('adopcion', __name__)

# modulo usuario
@adopcion_bp.route('/adopciones')
def adopcion():
    return mostrar_adopcion()