import os
import re
from flask import Flask, redirect, send_file, send_from_directory, url_for
from dotenv import load_dotenv


# Importamos el Blueprint que creamos en tu carpeta de rutas
from routes.inicio_routes import inicio_bp
from routes.usuario_routes import usuario_bp
from routes.alerta_routes import alerta_bp
from routes.admin_routes import admin_bp

load_dotenv()

# from routes.ia_routes import ia_bp
# from routes.informe_routes import informe_bp
from routes.articulo_routes import articulo_bp
from routes.mascota_routes import mascota_bp

from routes.mensaje_routes import mensaje_bp
from routes.reconocimiento_routes import reconocimiento_bp
# from routes.validacion_routes import validacion_bp
from controllers.security import current_user_id
from models.usuario_model import obtener_preferencias_usuario, obtener_usuario_por_id

# 1. Inicializamos la aplicación
app = Flask(__name__)
# SERVER_NAME activado puede romper el routing cuando accedes por IP
# distinta (p. ej. 127.0.0.1 en vez de localhost). Por eso solo lo activamos
# cuando explícitamente lo configuren via .env.
_SERVER_NAME = os.getenv("SERVER_NAME", "").strip()
if _SERVER_NAME:
    app.config["SERVER_NAME"] = _SERVER_NAME
    app.config["PREFERRED_URL_SCHEME"] = os.getenv("PREFERRED_URL_SCHEME", "http")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "busca-huellas-dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 14 * 1024 * 1024

# 2. Registramos las rutas (Blueprints)
app.register_blueprint(inicio_bp)
app.register_blueprint(usuario_bp, url_prefix="/autenticacion")
app.register_blueprint(articulo_bp, url_prefix="/articulos")
app.register_blueprint(alerta_bp, url_prefix="/alertas")
app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(ia_bp, url_prefix='/ia')
# app.register_blueprint(informe_bp, url_prefix='/informe')
app.register_blueprint(mascota_bp, url_prefix="/mascota")
app.register_blueprint(mensaje_bp, url_prefix="/mensaje")
app.register_blueprint(reconocimiento_bp, url_prefix="/reconocimiento")
# app.register_blueprint(validacion_bp, url_prefix='/validacion')


@app.context_processor
def inject_usuario_actual():
    usuario_id = current_user_id()
    if not usuario_id:
        return {"usuario_actual": None, "preferencias_actual": None}
    return {
        "usuario_actual": obtener_usuario_por_id(usuario_id),
        "preferencias_actual": obtener_preferencias_usuario(usuario_id),
    }


@app.after_request
def evitar_cache_sesion(response):
    # Bloquear cache HTML para que no se guarden datos de sesión.
    if response.mimetype == "text/html":
        html = response.get_data(as_text=True)

        # Etiquetas del favicon que insertamos en TODAS las páginas.
        # V13 se incrementa cada vez que cambiamos el favicon para vencer
        # la cache agresiva de los navegadores con este recurso.
        iconos = (
            '<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png?v=13">'
            '<link rel="icon" type="image/png" sizes="48x48" href="/static/img/favicon.png?v=13">'
            '<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico?v=13">'
            '<link rel="apple-touch-icon" type="image/png" href="/favicon.png?v=13">'
        )

        # 1) Si la página ya tenía un favicon anterior (cualquier variante
        #    de rel="icon", rel="shortcut icon" o favicon.png/.ico antiguo)
        #    lo borramos primero para evitar duplicados y rutas rotas.
        patron_link_icon = re.compile(
            r'<link\b[^>]*\brel\s*=\s*"[^"]*(?:icon|apple-touch-icon)[^"]*"[^>]*>',
            re.IGNORECASE,
        )
        html_limpio = patron_link_icon.sub("", html)

        # 2) Insertar los favicons actualizados inmediatamente antes de </head>.
        html_limpio = html_limpio.replace("</head>", f"{iconos}</head>")
        response.set_data(html_limpio)

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# 4. Si el usuario entra directo lo dirige a el inicio
@app.route("/")
def index():
    # Redirige a la función 'login' que está dentro del blueprint 'usuario'
    return redirect(url_for("usuario.inicio_sesion"))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _servir_favicon(archivo, mime):
    """Sirve un favicon con cache corta y fallback a varias rutas.

    Primero busca en la raíz del proyecto (BASE_DIR), si no existe cae
    a static/img. Así hay una copia en dos sitios y evitamos 404 al
    mover/cambiar el proyecto de máquina.
    """
    ruta_raiz = os.path.join(BASE_DIR, archivo)
    ruta_static = os.path.join(BASE_DIR, "static", "img", archivo)
    ruta_final = ruta_raiz if os.path.exists(ruta_raiz) else ruta_static
    response = send_file(ruta_final, mimetype=mime, max_age=60)
    response.headers["Cache-Control"] = "public, max-age=60, must-revalidate"
    response.headers["Vary"] = "Accept"
    return response


@app.route("/favicon.png")
def favicon_png():
    """Sirve el favicon PNG desde la raíz (con fallback a static/img)."""
    return _servir_favicon("favicon.png", "image/png")


@app.route("/favicon.ico")
def favicon_ico():
    """Sirve el favicon que el navegador pide por defecto (fallback)."""
    return _servir_favicon("favicon.ico", "image/x-icon")


@app.route("/static/img/favicon.png")
def static_favicon_png():
    """Ruta amigable para plantillas que siguen apuntando a static/img."""
    return _servir_favicon("favicon.png", "image/png")


@app.route("/static/img/favicon.ico")
def static_favicon_ico():
    """Favicon .ico bajo la ruta classic de static/img (fallback extra)."""
    return _servir_favicon("favicon.ico", "image/x-icon")


# 5. Arrancamos el servidor
if __name__ == "__main__":
    app.run(debug=True)
