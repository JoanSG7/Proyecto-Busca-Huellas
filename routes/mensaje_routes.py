from flask import Blueprint

from controllers.auth_controller import mostrar_chat_alerta, mostrar_chat_seguro
from controllers.security import login_required


mensaje_bp = Blueprint("mensaje", __name__)


@mensaje_bp.route("/chat")
@login_required
def chat_seguro():
    return mostrar_chat_seguro()


@mensaje_bp.route("/chat/<int:id_alerta>", methods=["GET", "POST"])
@login_required
def chat_alerta(id_alerta):
    return mostrar_chat_alerta(id_alerta)
