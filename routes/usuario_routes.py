from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import (
    cerrar_sesion,
    eliminar_mi_cuenta,
    iniciar_login_social,
    mostrar_editar_perfil,
    mostrar_configuracion_usuario,
    guardar_configuracion_usuario,
    mostrar_inicio_sesion,
    mostrar_perfil_usuario,
    mostrar_recuperar_contrasena,
    mostrar_registro_usuario,
    recibir_login_social,
)
from controllers.security import login_required
from controllers.legal_controller import mostrar_contacto, mostrar_documento_legal

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


@usuario_bp.route('/privacidad')
def politica_privacidad():
    return mostrar_documento_legal('privacidad')


@usuario_bp.route('/terminos')
def terminos_condiciones():
    return mostrar_documento_legal('terminos')


@usuario_bp.route('/acuerdo-de-uso')
def acuerdo_uso():
    return mostrar_documento_legal('acuerdo')


@usuario_bp.route('/contacto')
def contacto():
    return mostrar_contacto()

@usuario_bp.route('/perfil')
@login_required
def perfil_usuario():
    return mostrar_perfil_usuario()

@usuario_bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    return mostrar_editar_perfil()

@usuario_bp.route('/configuracion')
@login_required
def configuracion_usuario():
    return mostrar_configuracion_usuario()

@usuario_bp.route('/configuracion', methods=['POST'])
@login_required
def guardar_configuracion():
    return guardar_configuracion_usuario()

@usuario_bp.route('/eliminar-cuenta', methods=['POST'])
@login_required
def eliminar_cuenta():
    return eliminar_mi_cuenta()

@usuario_bp.route('/cerrar-sesion', methods=['POST'])
@login_required
def logout():
    return cerrar_sesion()
