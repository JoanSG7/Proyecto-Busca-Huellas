import os

from flask import Flask, redirect, url_for
# Importamos el Blueprint que creamos en tu carpeta de rutas
from routes.inicio_routes import inicio_bp
from routes.usuario_routes import usuario_bp
from routes.alerta_routes import alerta_bp
# from routes.ia_routes import ia_bp
# from routes.informe_routes import informe_bp
from routes.articulo_routes import articulo_bp
from routes.mascota_routes import mascota_bp
# from routes.mensaje_routes import mensaje_bp
from routes.reconocimiento_routes import reconocimiento_bp
# from routes.validacion_routes import validacion_bp

# 1. Inicializamos la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'busca-huellas-dev-secret-change-me')

# 2. Registramos las rutas (Blueprints)
app.register_blueprint(inicio_bp)
app.register_blueprint(usuario_bp, url_prefix='/autenticacion')
app.register_blueprint(articulo_bp, url_prefix='/articulos')
app.register_blueprint(alerta_bp, url_prefix='/alertas')
# app.register_blueprint(ia_bp, url_prefix='/ia')
# app.register_blueprint(informe_bp, url_prefix='/informe')
app.register_blueprint(mascota_bp, url_prefix='/mascota')
# app.register_blueprint(mensaje_bp, url_prefix='/mansaje')
app.register_blueprint(reconocimiento_bp, url_prefix='/reconocimiento')
# app.register_blueprint(validacion_bp, url_prefix='/validacion')


# 4. Si el usuario entra directo lo dirige a el inicio
@app.route('/')
def index():
    # Redirige a la función 'login' que está dentro del blueprint 'usuario'
    return redirect(url_for('usuario.inicio_sesion'))

# 5. Arrancamos el servidor
if __name__ == '__main__':
    app.run(debug=True)
