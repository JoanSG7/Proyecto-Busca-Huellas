from io import BytesIO

from flask import flash, make_response, redirect, render_template, request, session, url_for

from controllers.security import clean_text, is_valid_email, is_valid_phone
from models.admin_model import (
    actualizar_alerta_admin,
    actualizar_avistamiento_admin,
    actualizar_informe_admin,
    actualizar_mascota_admin,
    actualizar_usuario_admin,
    crear_informe_admin,
    eliminar_alerta_admin,
    eliminar_avistamiento_admin,
    eliminar_informe_admin,
    eliminar_mascota_admin,
    eliminar_usuario_admin,
    generar_datos_informe,
    listar_alertas_admin,
    listar_avistamientos_admin,
    listar_informes_admin,
    listar_mascotas_admin,
    listar_usuarios_admin,
    obtener_alerta_admin,
    obtener_avistamiento_admin,
    obtener_informe_admin,
    obtener_mascota_admin,
    obtener_resumen_admin,
    obtener_usuario_admin,
)


ADMIN_SECTIONS = {
    "usuarios": {"titulo": "Usuarios", "filtro": ("rol", [("", "Todos"), ("1", "Usuarios"), ("2", "Administradores")])},
    "mascotas": {"titulo": "Mascotas", "filtro": ("estado", [("", "Todos"), ("perdida", "Perdida"), ("encontrada", "Encontrada"), ("en proceso", "En proceso")])},
    "alertas": {"titulo": "Alertas", "filtro": ("estado", [("", "Todos"), ("pendiente", "Pendiente"), ("enviada", "Enviada"), ("vista", "Vista")])},
    "avistamientos": {"titulo": "Avistamientos", "filtro": ("estado", [("", "Todos"), ("confirmados", "Confirmados"), ("sin_confirmar", "Sin confirmar")])},
    "informes": {"titulo": "Informes", "filtro": ("tipo", [("", "Todos"), ("mascotas_por_fecha", "Mascotas"), ("alertas_por_fecha", "Alertas"), ("top_usuarios_avistamientos", "Top usuarios")])},
}


def _list_items(seccion, q, filtro):
    if seccion == "usuarios":
        return listar_usuarios_admin(q, filtro)
    if seccion == "mascotas":
        return listar_mascotas_admin(q, filtro)
    if seccion == "alertas":
        return listar_alertas_admin(q, filtro)
    if seccion == "avistamientos":
        return listar_avistamientos_admin(q, filtro)
    return listar_informes_admin(q, filtro)


def _get_item(seccion, item_id):
    getters = {
        "usuarios": obtener_usuario_admin,
        "mascotas": obtener_mascota_admin,
        "alertas": obtener_alerta_admin,
        "avistamientos": obtener_avistamiento_admin,
        "informes": obtener_informe_admin,
    }
    return getters[seccion](item_id)


def mostrar_admin(seccion="usuarios"):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    filtro_nombre = ADMIN_SECTIONS[seccion]["filtro"][0]
    q = clean_text(request.args.get("q"), 100)
    filtro = clean_text(request.args.get(filtro_nombre), 80)
    preview = session.pop("informe_preview", None) if seccion == "informes" else None
    return render_template(
        "modulo_admin/panel.html",
        seccion=seccion,
        secciones=ADMIN_SECTIONS,
        config=ADMIN_SECTIONS[seccion],
        filtro_nombre=filtro_nombre,
        q=q,
        filtro=filtro,
        items=_list_items(seccion, q, filtro),
        resumen=obtener_resumen_admin(),
        preview=preview,
    )


def mostrar_detalle_admin(seccion, item_id):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    item = _get_item(seccion, item_id)
    if not item:
        flash("No se encontro el registro solicitado.", "error")
        return redirect(url_for("admin.panel", seccion=seccion))
    return render_template(
        "modulo_admin/detalle.html",
        seccion=seccion,
        config=ADMIN_SECTIONS[seccion],
        item=item,
        item_id=item_id,
        modo=clean_text(request.args.get("modo"), 20) or "ver",
    )


def eliminar_item_admin(seccion, item_id):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    _delete_item(seccion, item_id)
    flash("Registro eliminado.", "success")
    return redirect(url_for("admin.panel", seccion=seccion))


def guardar_detalle_admin(seccion, item_id):
    accion = request.form.get("accion")
    if accion == "eliminar":
        _delete_item(seccion, item_id)
        flash("Registro eliminado.", "success")
        return redirect(url_for("admin.panel", seccion=seccion))

    if seccion == "usuarios":
        nombre = clean_text(request.form.get("nombre_completo"), 100)
        telefono = clean_text(request.form.get("telefono"), 20)
        correo = clean_text(request.form.get("correo"), 100).lower()
        id_rol = clean_text(request.form.get("id_rol"), 5)
        if len(nombre) < 3 or not is_valid_email(correo) or not is_valid_phone(telefono) or id_rol not in {"1", "2"}:
            flash("Revisa los datos del usuario.", "error")
        else:
            actualizar_usuario_admin(item_id, nombre, telefono, correo, id_rol)
            flash("Usuario actualizado.", "success")
    elif seccion == "mascotas":
        try:
            edad = int(request.form.get("edad") or 0)
        except ValueError:
            edad = 0
        actualizar_mascota_admin(
            item_id,
            clean_text(request.form.get("id_usuario"), 20) or None,
            clean_text(request.form.get("nombre_mascota"), 100),
            clean_text(request.form.get("raza"), 100),
            edad,
            clean_text(request.form.get("color"), 50),
            clean_text(request.form.get("pelaje"), 50),
            clean_text(request.form.get("tamano"), 50),
            clean_text(request.form.get("descripcion"), 1000),
            clean_text(request.form.get("estado"), 50),
        )
        flash("Mascota actualizada.", "success")
    elif seccion == "alertas":
        actualizar_alerta_admin(
            item_id,
            clean_text(request.form.get("id_usuario"), 20),
            clean_text(request.form.get("id_mascota"), 20),
            clean_text(request.form.get("estado_alerta"), 80),
            clean_text(request.form.get("confirmacion"), 80),
        )
        flash("Alerta actualizada.", "success")
    elif seccion == "avistamientos":
        actualizar_avistamiento_admin(
            item_id,
            clean_text(request.form.get("id_mascota"), 20),
            clean_text(request.form.get("ubicacion"), 150),
            clean_text(request.form.get("descripcion_avistamiento"), 1000),
            clean_text(request.form.get("url_imagen"), 255),
            clean_text(request.form.get("fecha_avistamiento"), 30),
        )
        flash("Avistamiento actualizado.", "success")
    elif seccion == "informes":
        actualizar_informe_admin(
            item_id,
            clean_text(request.form.get("tipo_informe"), 80),
            clean_text(request.form.get("descripcion"), 3000),
        )
        flash("Informe actualizado.", "success")
    return redirect(url_for("admin.detalle", seccion=seccion, item_id=item_id))


def _delete_item(seccion, item_id):
    deletes = {
        "usuarios": eliminar_usuario_admin,
        "mascotas": eliminar_mascota_admin,
        "alertas": eliminar_alerta_admin,
        "avistamientos": eliminar_avistamiento_admin,
        "informes": eliminar_informe_admin,
    }
    deletes[seccion](item_id)


def generar_informe_admin():
    tipo = clean_text(request.form.get("tipo_informe"), 80)
    fecha_inicio = clean_text(request.form.get("fecha_inicio"), 20)
    fecha_fin = clean_text(request.form.get("fecha_fin"), 20)
    limite = clean_text(request.form.get("limite"), 3) or "10"
    titulo = clean_text(request.form.get("titulo"), 120) or "Informe personalizado"
    datos = [_serializar_fila(row) for row in generar_datos_informe(tipo, fecha_inicio, fecha_fin, limite)]
    preview = {
        "titulo": titulo,
        "tipo": tipo,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "limite": limite,
        "datos": datos,
    }
    accion = request.form.get("accion")
    if accion == "guardar":
        descripcion = _render_text_report(preview)
        crear_informe_admin(session.get("usuario_id"), tipo, descripcion)
        flash("Informe guardado.", "success")
    else:
        session["informe_preview"] = preview
    return redirect(url_for("admin.panel", seccion="informes"))


def exportar_informe_admin(formato):
    preview = session.get("informe_preview")
    if not preview:
        flash("Primero genera una vista previa del informe.", "error")
        return redirect(url_for("admin.panel", seccion="informes"))
    contenido = _render_text_report(preview)
    if formato == "word":
        html = "<html><body><pre>" + contenido.replace("&", "&amp;").replace("<", "&lt;") + "</pre></body></html>"
        response = make_response(html)
        response.headers["Content-Type"] = "application/msword"
        response.headers["Content-Disposition"] = "attachment; filename=informe_busca_huellas.doc"
        return response
    pdf = _simple_pdf(contenido)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=informe_busca_huellas.pdf"
    return response


def _render_text_report(preview):
    lines = [preview["titulo"], f"Tipo: {preview['tipo']}", ""]
    if preview.get("fecha_inicio") or preview.get("fecha_fin"):
        lines.append(f"Rango: {preview.get('fecha_inicio') or 'inicio'} a {preview.get('fecha_fin') or 'hoy'}")
        lines.append("")
    for index, row in enumerate(preview.get("datos") or [], start=1):
        detail = " | ".join(f"{key}: {value}" for key, value in row.items())
        lines.append(f"{index}. {detail}")
    if not preview.get("datos"):
        lines.append("Sin resultados para los filtros seleccionados.")
    return "\n".join(lines)


def _serializar_fila(row):
    return {key: "" if value is None else str(value) for key, value in row.items()}


def _simple_pdf(text):
    stream = BytesIO()
    lines = text.splitlines()[:45]
    content = "BT /F1 11 Tf 50 780 Td 14 TL " + " T* ".join(f"({line[:90].replace('(', '[').replace(')', ']')}) Tj" for line in lines) + " ET"
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        b"3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >> endobj\n",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        f"5 0 obj << /Length {len(content.encode('latin-1', 'replace'))} >> stream\n{content}\nendstream endobj\n".encode("latin-1", "replace"),
    ]
    stream.write(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(stream.tell())
        stream.write(obj)
    xref = stream.tell()
    stream.write(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        stream.write(f"{offset:010d} 00000 n \n".encode())
    stream.write(f"trailer << /Root 1 0 R /Size {len(objects) + 1} >>\nstartxref\n{xref}\n%%EOF".encode())
    return stream.getvalue()
