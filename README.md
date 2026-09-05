# Busca Huellas

Plataforma web para reportar mascotas perdidas, encontradas y realizar su reconocimiento mediante inteligencia artificial. Desarrollada con **Flask** y **MySQL, incluye sistema de usuarios con roles, alertas, chat seguro, artículos informativos y un módulo de reconocimiento visual de mascotas usando redes neuronales (TensorFlow).

---

## Requisitos previos

Asegúrate de tener instalado en tu sistema:

| Software          | Versión recomendada          |
|-------------------|------------------------------|
| Python            | 3.10 o superior              |
| MySQL / MariaDB   | 8.0+ o 10.5+                 |
| Navegador web     | Cualquiera moderno (Chrome, Edge, Firefox, etc.) |

> **Nota**: El módulo de IA usa TensorFlow, por lo que se recomiendan al menos 4 GB de RAM libres.

---

## Pasos para ejecutar el proyecto

### 1. Clonar / ubicar el proyecto

Si acabas de clonar el repositorio, abre una terminal y sitúate dentro de la carpeta raíz:

```bash
cd Proyecto-Busca-Huellas-main
```

### 2. Crear un entorno virtual de Python

```bash
# Windows (PowerShell / CMD)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux (Bash / Zsh)
python3 -m venv .venv
source .venv/bin/activate
```

Deberías ver `(.venv)` al inicio de tu prompt, confirmando que el entorno está activado.

### 3. Instalar dependencias

Con el entorno activado:

```bash
pip install -r requirements.txt
```

> Si `pip` da problemas, prueba con `python -m pip install -r requirements.txt`.

### 4. Crear el archivo `.env`

El proyecto lee configuraciones desde un archivo `.env` en la raíz. Copia el de ejemplo:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Abre `.env` con un editor y ajusta los valores según tu máquina. Los más importantes:

- `SECRET_KEY`: una cadena aleatoria usada por Flask para sesiones seguras.
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`: credenciales de tu MySQL.
- `DB_NAME`: nombre de la base de datos (por defecto `busca_huellas`).
- `ADMIN_REGISTRATION_CODE`: código necesario para crear una cuenta de tipo administrador.

Las variables de SMTP y OAuth son **opcionales**. Si no se configuran:
- Los códigos de verificación / recuperación de contraseña se imprimirán en la consola de Flask.
- El botón de login con Google mostrará un aviso indicando que no está configurado.

### 5. Crear la base de datos en MySQL

Conéctate a tu servidor MySQL (por consola, Workbench, phpMyAdmin, etc.) y ejecuta el script principal que incluye la estructura y los catálogos:

```sql
source busca_huellas.sql;
```

O desde la línea de comandos:

```bash
# Ajusta el usuario y ruta según tu equipo
mysql -u root -p < busca_huellas.sql
```

El script crea automáticamente la base `busca_huellas`, todas las tablas, índices y el catálogo de roles (`Usuario` y `Administrador`).

#### Migraciones adicionales (opcionales)

Dentro de `Documentacion/` hay varios scripts `migracion_*.sql`. Son actualizaciones que se aplicaron sobre el esquema inicial. Si ejecutaste `busca_huellas.sql` reciente **no son necesarios**, pero si estás actualizando una instalación anterior revisa y aplica cada uno en orden alfabético.

### 6. Ejecutar la aplicación Flask

Con el entorno virtual activado y la base de datos lista:

```bash
python app.py
```

Verás una salida similar a:

```
[INFO] Intentando arrancar Flask en localhost:5000 ...
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://localhost:5000
Press CTRL+C to quit
```

Abre en tu navegador la URL que muestre la terminal — normalmente **<http://localhost:5000>**.

> 🔧 **Puerto y host son configurables via `.env`** (variables `PORT` y `FLASK_HOST`, ver sección siguiente).
> La raíz redirige automáticamente al inicio de sesión.

#### ⚠️ Si el puerto 5000 está ocupado (muy común en PCs del SENA)

En laboratorios del SENA es normal que el puerto 5000 ya lo use otro programa
(Skype, Windows servicios, Docker, IIS Express, etc.). En ese caso no tienes
que hacer nada manualmente — el script **ya intenta automáticamente** los
puertos en este orden:

1. El que hayas puesto en `PORT` del `.env` (por defecto `5000`)
2. `5001`
3. `8000`
4. `8080`
5. `3000`

En la consola verás algo como:

```
[INFO] Intentando arrancar Flask en localhost:5000 ...
[WARNING] Puerto 5000 OCUPADO o denegado (...). Proximo puerto...
[INFO] Intentando arrancar Flask en localhost:5001 ...
 * Running on http://localhost:5001
```

Simplemente abre la URL nueva (en el ejemplo `http://localhost:5001`). Si
prefieres forzar un puerto concreto antes de arrancar, edita el `.env`:

```ini
PORT=8080
```

#### 🖧 Quieren ver la app desde otro PC del salón del SENA

Por defecto Flask solo escucha en `localhost` (solo el mismo equipo). Si
en la sustentación quieren que **otros PCs de la red local** abran la app:

1. En el `.env` cambia:
   ```ini
   FLASK_HOST=0.0.0.0
   ```
2. Reinicia `python app.py`.
3. Averigua la IP del PC donde corre Flask (`ipconfig` en Windows →
   "Dirección IPv4" de Ethernet / Wi‑Fi, por ejemplo `192.168.0.20`).
4. Desde otro PC de la misma red abren `http://192.168.0.20:5000`
   (o el puerto que haya arrancado — en tu propio PC sigue funcionando
   **también** con `http://localhost:5000`).

> 🔒 En Windows puede saltar el Firewall al poner `0.0.0.0`. Acepta la
> ventanita de "Permitir acceso" marcando redes **Privadas** y **Públicas**.

---

## Primer uso: crear cuentas

### Cuenta de usuario normal

1. Entra a **Registrarse** desde la pantalla de login.
2. Rellena tus datos y elige el tipo de cuenta **"Usuario"**.
3. Se enviará un código de 6 dígitos al correo (si SMTP está configurado) o aparecerá en la consola del servidor.
4. Ingresa el código para confirmar tu correo.

### Cuenta de administrador

1. En el formulario de registro selecciona tipo **"Administrador"**.
2. Aparecerá un campo extra: **Código de administrador**.
3. Ingresa el mismo valor que configuraste en `ADMIN_REGISTRATION_CODE` dentro de `.env` (por defecto `BUSCAHUELLAS-ADMIN`).
4. Completa el registro y verificación como cualquier otro usuario.

Con una cuenta de administrador podrás:
- Publicar, editar y eliminar artículos informativos.
- Ver el panel de administración.
- Revisar chats y métricas del sistema.

---

## Estructura del proyecto

```
Proyecto-Busca-Huellas-main/
├── app.py                     # Punto de entrada de Flask (blueprints, configuración)
├── requirements.txt           # Dependencias de Python
├── .env.example               # Plantilla de variables de entorno
├── busca_huellas.sql          # Script principal de la BD
├── config/
│   └── database.py            # Conexión y cursor para MySQL
├── controllers/               # Lógica de negocio (auth, admin, IA, reportes, etc.)
├── models/                    # Consultas a la base de datos
├── routes/                    # Blueprints de Flask (rutas HTTP)
├── templates/                 # Plantillas HTML (Jinja2)
├── static/
│   ├── css/                   # Estilos
│   ├── js/                    # Scripts de front-end
│   ├── img/                   # Imágenes del sitio
│   └── uploads/               # Fotos subidas por los usuarios (mascotas, perfiles, capturas)
└── Documentacion/
    ├── ER.png / Mer.jpg       # Diagramas de la BD
    └── migracion_*.sql        # Scripts de actualización
```

---

## Características principales

- **Autenticación**: registro con verificación de correo, inicio de sesión, recuperación de contraseña, login social con Google (OAuth).
- **Gestión de mascotas**: registrar, editar, eliminar y listar mascotas perdidas con múltiples fotos, ubicación y descripción.
- **Reconocimiento por IA**: toma o sube una foto de una mascota y el sistema la compara con todas las registradas usando TensorFlow y similitud de embeddings.
- **Alertas y avistamientos**: cuando se reporta un posible avistamiento se crea una alerta y un chat privado entre el dueño y quien reportó.
- **Chat seguro**: mensajes privados con filtro de palabras y confirmación de avistamiento por parte del dueño.
- **Panel de administrador**: métricas, gestión de artículos informativos y supervisión general.
- **Preferencias de usuario**: tema claro / oscuro / sepia, reducción de movimiento.

---

## Parar el servidor

Pulsa `Ctrl + C` en la terminal donde se está ejecutando `python app.py`.

---

## Solución de problemas frecuentes

| Síntoma | Causa probable | Solución |
|---------|---------------|----------|
| `No se pudo conectar con la base de datos` | MySQL no está corriendo, o credenciales en `.env` erróneas | Verifica que MySQL esté activo y revisa `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` |
| `Table 'busca_huellas.XXX' doesn't exist` | No ejecutaste `busca_huellas.sql` o te faltó alguna migración | Importa el script principal y, si aplica, las migraciones de `Documentacion/` |
| Los códigos de registro no llegan al correo | SMTP no configurado en `.env` | Revisa los valores de SMTP. Mientras tanto, los códigos se imprimen en la consola de Flask |
| Error al instalar `mysqlclient` en Windows | Faltan compiladores / librerías C | Instala primero un paquete precompilado con `pip install mysqlclient` desde un wheel oficial, o usa Visual Studio Build Tools |
| TensorFlow tarda mucho en cargar o se cierra | Falta de memoria o arquitectura no compatible | Asegúrate de usar Python 3.10-3.12 y tener al menos 4 GB de RAM libre |

---

## Desarrollo y entorno

- El servidor se ejecuta con `debug=True`, así que cualquier cambio en archivos `.py` recarga la app automáticamente.
- Las carpetas `static/uploads/` contienen imágenes de usuarios; se recomienda **no** versionarlas en Git.
- El archivo `.env` ya está excluido en `.gitignore` para no subir secretos al repositorio.
