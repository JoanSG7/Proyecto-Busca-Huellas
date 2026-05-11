from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import mostrar_inicio_sesion, mostrar_registro_usuario, mostrar_recuperar_contrasena, mostrar_noticias

usuario_bp = Blueprint('usuario', __name__)

# modulo usuario
@usuario_bp.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    return mostrar_inicio_sesion()

@usuario_bp.route('/registro')
def registro_usuario():
    return mostrar_registro_usuario()

@usuario_bp.route('/recuperar-contrasena')
def recuperar_contrasena():
    return mostrar_recuperar_contrasena()

@usuario_bp.route('/noticias')
def noticia():
    return mostrar_noticias()