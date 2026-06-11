from flask import Blueprint

from controllers.auth_controller import mostrar_chat_seguro
from controllers.security import login_required


mensaje_bp = Blueprint("mensaje", __name__)


@mensaje_bp.route("/chat")
@login_required
def chat_seguro():
    return mostrar_chat_seguro()
