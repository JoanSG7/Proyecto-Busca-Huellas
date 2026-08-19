from flask import render_template


EQUIPO = (
    "Joan Sebastian Guerrero Cristancho, Jose Daniel Londono Sanchez, "
    "Efrain Santiago Paez Rodriguez y Juan David Rivera Grillo"
)
CONTACTO = "buscahuellasteam@gmail.com"


DOCUMENTOS = {
    "privacidad": {
        "titulo": "Politica de privacidad",
        "descripcion": "Como tratamos la informacion en Busca Huellas.",
        "secciones": [
            ("Caracter academico", [
                "Busca Huellas es un proyecto academico desarrollado por aprendices ADSO del SENA. Se usa con fines de aprendizaje y demostracion; no es un servicio comercial ni una plataforma oficial de una entidad publica.",
                f"Los responsables del proyecto son: {EQUIPO}. Para consultas escribe a {CONTACTO}.",
            ]),
            ("Datos que podemos solicitar", [
                "Para crear y administrar una cuenta podemos solicitar nombre, correo electronico, telefono, fecha de nacimiento, foto de perfil y credenciales de acceso. Tambien se almacenan las fotos y datos de mascotas, publicaciones, alertas y mensajes que decidas compartir en la plataforma.",
                "Si eliges iniciar sesion con Google, recibimos los datos basicos autorizados por ti, como nombre, correo y foto de perfil. No solicitamos tu contrasena de Google.",
            ]),
            ("Finalidades", [
                "Usamos los datos para crear la cuenta, permitir la publicacion y busqueda de mascotas, generar alertas, facilitar la comunicacion entre usuarios y mantener la seguridad basica de la plataforma.",
                "No usamos la informacion para venderla ni para enviar publicidad comercial.",
            ]),
            ("Informacion visible para otros usuarios", [
                "Las publicaciones, fotos de mascotas, alertas y mensajes pueden ser vistos por las personas que usan Busca Huellas segun la funcion utilizada. No publiques documentos de identidad, contrasenas, ubicaciones privadas u otra informacion sensible.",
            ]),
            ("Tus derechos y contacto", [
                f"Puedes solicitar conocer, actualizar, corregir o eliminar tus datos, o revocar la autorizacion, escribiendo a {CONTACTO}. Incluye el correo de tu cuenta y explica tu solicitud.",
                "Esta politica se inspira en los principios de la Ley 1581 de 2012 de Colombia. Por tratarse de un proyecto academico, el equipo atendera las solicitudes dentro de las posibilidades de la etapa de demostracion.",
            ]),
            ("Conservacion y seguridad", [
                "Los datos se conservan mientras la demostracion del proyecto este activa o hasta que solicites su eliminacion. Aplicamos medidas basicas de acceso y contrasenas, pero ningun sistema en internet puede garantizar seguridad absoluta.",
            ]),
        ],
    },
    "terminos": {
        "titulo": "Terminos y condiciones",
        "descripcion": "Reglas de uso de la plataforma academica Busca Huellas.",
        "secciones": [
            ("Objeto de la plataforma", ["Busca Huellas permite registrar mascotas, publicar alertas y facilitar el contacto entre personas que reportan una mascota perdida, encontrada o avistada. Es una demostracion academica creada por aprendices ADSO del SENA."]),
            ("Requisitos de uso", ["Debes proporcionar datos veraces, proteger tu contrasena y tener al menos 18 anos para registrarte. Eres responsable de la informacion, fotos, publicaciones y mensajes asociados a tu cuenta."]),
            ("Uso responsable", ["No esta permitido suplantar a otras personas, publicar contenido falso, ofensivo, ilegal o que vulnere derechos de terceros, ni usar la plataforma para estafas, acoso o spam.", "No compartas informacion personal sensible en publicaciones o chats. Antes de entregar o recibir una mascota, verifica la informacion y actua con precaucion."]),
            ("Alcance y limitaciones", ["Busca Huellas no garantiza que una mascota sea encontrada, que una publicacion sea exacta ni que las personas usuarias sean quienes dicen ser. No reemplaza a autoridades, servicios veterinarios ni servicios de emergencia.", "El equipo academico puede modificar, suspender o finalizar la demostracion y retirar contenido que incumpla estas reglas."]),
            ("Contacto", [f"Para reportar contenido o solicitar ayuda relacionada con el proyecto, escribe a {CONTACTO}."]),
        ],
    },
    "acuerdo": {
        "titulo": "Acuerdo de uso",
        "descripcion": "Consentimiento para crear y utilizar una cuenta en Busca Huellas.",
        "secciones": [
            ("Aceptacion", ["Al marcar la casilla de aceptacion y crear una cuenta, confirmas que leiste y aceptas los Terminos y condiciones y la Politica de privacidad de Busca Huellas."]),
            ("Autorizacion de datos", ["Autorizas al equipo academico de Busca Huellas a tratar los datos que proporcionas exclusivamente para las finalidades descritas en la Politica de privacidad: administracion de la cuenta, publicaciones, alertas, mensajes y funcionamiento de la demostracion."]),
            ("Compromiso de la persona usuaria", ["Confirmas que eres mayor de edad, que la informacion entregada es verdadera y que usaras la plataforma de forma responsable. Puedes pedir la actualizacion o eliminacion de tus datos escribiendo al correo de contacto."]),
            ("Contacto", [f"Correo del equipo responsable: {CONTACTO}."]),
        ],
    },
}


def mostrar_documento_legal(tipo):
    documento = DOCUMENTOS.get(tipo)
    if not documento:
        return "Documento no encontrado", 404
    return render_template("documento_legal.html", documento=documento)


def mostrar_contacto():
    return render_template("contacto.html", correo=CONTACTO)
