from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import (
    cerrar_sesion,
    iniciar_login_social,
    mostrar_editar_perfil,
    mostrar_inicio_sesion,
    mostrar_perfil_usuario,
    mostrar_recuperar_contrasena,
    mostrar_registro_usuario,
    recibir_login_social,
)
from controllers.security import login_required

usuario_bp = Blueprint('usuario', __name__)

# modulo usuario
@usuario_bp.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    return mostrar_inicio_sesion()

@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registro_usuario():
    return mostrar_registro_usuario()

@usuario_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    return mostrar_recuperar_contrasena()

@usuario_bp.route('/login/<provider>')
def oauth_login(provider):
    return iniciar_login_social(provider)

@usuario_bp.route('/login/<provider>/callback')
def oauth_callback(provider):
    return recibir_login_social(provider)

@usuario_bp.route('/perfil')
@login_required
def perfil_usuario():
    return mostrar_perfil_usuario()

@usuario_bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    return mostrar_editar_perfil()

@usuario_bp.route('/cerrar-sesion', methods=['POST'])
@login_required
def logout():
    return cerrar_sesion()
