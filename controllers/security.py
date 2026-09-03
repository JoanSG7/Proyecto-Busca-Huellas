from functools import wraps
import os
from re import fullmatch

from flask import flash, redirect, session, url_for


USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE", "BUSCAHUELLAS-ADMIN")
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_PATTERN = r"^[0-9+\-\s()]{7,20}$"
VALID_PET_STATES = {"perdida", "encontrada", "en proceso"}
VALID_PET_SIZES = {"pequeño", "mediano", "grande"}


def clean_text(value, max_length=None):
    value = (value or "").strip()
    if max_length:
        value = value[:max_length]
    return value


def is_valid_email(value):
    return bool(fullmatch(EMAIL_PATTERN, value or ""))


def is_valid_phone(value):
    return not value or bool(fullmatch(PHONE_PATTERN, value))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("usuario.inicio_sesion"))
        return view(*args, **kwargs)

    return wrapped_view


def is_admin():
    return session.get("rol_id") == ADMIN_ROLE_ID


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("usuario.inicio_sesion"))
        if not is_admin():
            flash("Solo un administrador puede realizar esta acción.", "error")
            return redirect(url_for("articulo.lista_articulos"))
        return view(*args, **kwargs)

    return wrapped_view


def current_user_id():
    return session.get("usuario_id")
