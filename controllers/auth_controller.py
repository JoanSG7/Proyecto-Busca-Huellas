from flask import render_template, request

# inicio
def mostrar_inicio():
    return render_template('inicio.html') 

# Modulo usuario
def mostrar_inicio_sesion():
    if request.method == 'POST':
        # Aquí capturas los datos: email = request.form.get('email')
        return "Procesando el inicio de sesión..."
    
    # Si es GET, solo renderizas el HTML
    return render_template('modulo_usuario/inicio_sesion.html')

def mostrar_registro_usuario():
    return render_template('modulo_usuario/registro_usuario.html')

def mostrar_recuperar_contrasena():
    return render_template('modulo_usuario/recuperar_contraseña.html')

def mostrar_perfil_usuario():
    return render_template('modulo_usuario/perfil_usuario.html')

#Modulo alertas

def mostrar_lista_alertas():
    return render_template('modulo_alerta/lista_alertas.html')

# modulo articulo
def mostrar_lista_articulos():
    return render_template('modulo_articulo/lista_articulos.html')

# modulo mascota
def mostrar_registro_mascota():
    return render_template('modulo_mascota/registro_mascota.html')
