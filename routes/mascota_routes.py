from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_registro_mascota

mascota_bp = Blueprint('mascota', __name__)

# modulo usuario
@mascota_bp.route('/registro-mascota')
def registro_mascota():
    return mostrar_registro_mascota()