from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_registro_mascota, mostrar_info_mascota

mascota_bp = Blueprint('mascota', __name__)

# modulo mascota
@mascota_bp.route('/registro-mascota')
def registro_mascota():
    return mostrar_registro_mascota()

@mascota_bp.route('/info-mascota')
def info_mascota():
    return mostrar_info_mascota()