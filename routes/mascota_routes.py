from flask import Blueprint
# Importamos las funciones del controlador
from controllers.auth_controller import editar_mi_mascota, eliminar_mi_mascota, mostrar_registro_mascota, mostrar_info_mascota
from controllers.security import login_required

mascota_bp = Blueprint('mascota', __name__)

# modulo mascota
@mascota_bp.route('/registro-mascota', methods=['GET', 'POST'])
@login_required
def registro_mascota():
    return mostrar_registro_mascota()

@mascota_bp.route('/info-mascota/<int:id_mascota>')
@login_required
def info_mascota(id_mascota):
    return mostrar_info_mascota(id_mascota)


@mascota_bp.route('/<int:id_mascota>/editar', methods=['GET', 'POST'])
@login_required
def editar(id_mascota):
    return editar_mi_mascota(id_mascota)


@mascota_bp.route('/<int:id_mascota>/eliminar', methods=['POST'])
@login_required
def eliminar(id_mascota):
    return eliminar_mi_mascota(id_mascota)
