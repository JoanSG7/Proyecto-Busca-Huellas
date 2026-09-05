from flask import Blueprint, flash, redirect, url_for

from controllers.auth_controller import mostrar_capturar_foto
from controllers.security import login_required

reconocimiento_bp = Blueprint('reconocimiento', __name__)


@reconocimiento_bp.route('/capturar-foto', methods=['GET', 'POST'])
@login_required
def capturar_foto():
    return mostrar_capturar_foto()


@reconocimiento_bp.route('/resultados')
@login_required
def resultados():
    flash('Los resultados de busqueda solo estan disponibles inmediatamente despues de tomar la foto. Realiza una nueva busqueda para ver coincidencias.', 'warning')
    return redirect(url_for('reconocimiento.capturar_foto'))
