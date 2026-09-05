import os
from datetime import date, datetime
from io import BytesIO

from flask import flash, make_response, redirect, render_template, request, send_file, session, url_for


from controllers.report_pdf import crear_pdf_informe, ruta_archivo_informe

from controllers.report_excel import crear_excel_informe
from controllers.security import VALID_PET_STATES, clean_text, is_valid_email, is_valid_phone
from models.admin_model import (
    actualizar_alerta_admin,
    actualizar_articulo_admin,
    actualizar_avistamiento_admin,
    actualizar_archivos_informe,
    actualizar_informe_admin,
    actualizar_mascota_admin,
    actualizar_usuario_admin,
    crear_informe_admin,
    eliminar_alerta_admin,
    eliminar_articulo_admin,
    eliminar_avistamiento_admin,
    eliminar_informe_admin,
    eliminar_mascota_admin,
    eliminar_usuario_admin,
    reactivar_articulo_admin,
    reactivar_usuario_admin,
    reactivar_mascota_admin,
    reactivar_alerta_admin,
    reactivar_avistamiento_admin,
    reactivar_avistamiento_confirmado_admin,
    reactivar_informe_admin,
    generar_datos_informe,
    listar_alertas_admin,
    listar_articulos_admin,
    listar_avistamientos_admin,
    listar_avistamientos_confirmados_admin,
    listar_informes_admin,
    listar_mascotas_admin,
    listar_usuarios_admin,
    obtener_alerta_admin,
    obtener_articulo_admin,
    obtener_avistamiento_admin,
    obtener_avistamiento_confirmado_admin,
    obtener_informe_admin,
    obtener_mascota_admin,
    obtener_resumen_admin,
    obtener_usuario_admin,
)


ADMIN_SECTIONS = {
    "usuarios": {"titulo": "Usuarios", "filtro": ("rol", [("", "Todos"), ("1", "Usuarios"), ("2", "Administradores")])},
    "articulos": {"titulo": "Artículos", "filtro": ("filtro", [("", "Todos")])},
    "mascotas": {"titulo": "Mascotas", "filtro": ("estado", [("", "Todos"), ("perdida", "Perdida"), ("encontrada", "Encontrada"), ("en proceso", "En proceso")])},
    "alertas": {"titulo": "Alertas", "filtro": ("estado", [("", "Todos"), ("pendiente", "Pendiente"), ("enviada", "Enviada"), ("vista", "Vista")])},
    "avistamientos": {"titulo": "Avistamientos", "filtro": ("estado", [("", "Todos"), ("confirmados", "Confirmados"), ("sin_confirmar", "Sin confirmar")])},
    "avistamientos_confirmados": {"titulo": "Avistamientos confirmados", "filtro": ("filtro", [("", "Todos")])},
    "informes": {"titulo": "Informes", "filtro": ("tipo", [("", "Todos"), ("mascotas_por_fecha", "Mascotas"), ("alertas_por_fecha", "Alertas"), ("top_usuarios_avistamientos", "Top usuarios")])},
}


def _list_items(seccion, q, filtro, eliminados=False):
    if seccion == "usuarios":
        return listar_usuarios_admin(q, filtro, eliminados)
    if seccion == "articulos":
        return listar_articulos_admin(q, filtro, eliminados)
    if seccion == "mascotas":
        return listar_mascotas_admin(q, filtro, eliminados)
    if seccion == "alertas":
        return listar_alertas_admin(q, filtro, eliminados)
    if seccion == "avistamientos":
        return listar_avistamientos_admin(q, filtro, eliminados)
    if seccion == "avistamientos_confirmados":
        return listar_avistamientos_confirmados_admin(q, filtro, eliminados)
    return listar_informes_admin(q, filtro, eliminados)


def _get_item(seccion, item_id):
    getters = {
        "usuarios": obtener_usuario_admin,
        "articulos": obtener_articulo_admin,
        "mascotas": obtener_mascota_admin,
        "alertas": obtener_alerta_admin,
        "avistamientos": obtener_avistamiento_admin,
        "avistamientos_confirmados": obtener_avistamiento_confirmado_admin,
        "informes": obtener_informe_admin,
    }
    return getters[seccion](item_id)


def mostrar_admin(seccion="usuarios"):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    filtro_nombre = ADMIN_SECTIONS[seccion]["filtro"][0]
    q = clean_text(request.args.get("q"), 100)
    filtro = clean_text(request.args.get(filtro_nombre), 80)
    eliminados = request.args.get("vista") == "eliminados"
    preview = session.pop("informe_preview", None) if seccion == "informes" else None
    return render_template(
        "modulo_admin/panel.html",
        seccion=seccion,
        secciones=ADMIN_SECTIONS,
        config=ADMIN_SECTIONS[seccion],
        filtro_nombre=filtro_nombre,
        q=q,
        filtro=filtro,
        items=_list_items(seccion, q, filtro, eliminados),
        resumen=obtener_resumen_admin(eliminados),
        preview=preview,
        eliminados=eliminados,
    )


def mostrar_detalle_admin(seccion, item_id):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    item = _get_item(seccion, item_id)
    if not item:
        flash("No se encontro el registro solicitado.", "error")
        return redirect(url_for("admin.panel", seccion=seccion))
    campo_estado = {
        "usuarios": "estado_usuario",
        "articulos": "estado_articulo",
        "mascotas": "estado_mascota",
        "alertas": "estado_alerta_registro",
        "avistamientos": "estado_avistamiento",
        "avistamientos_confirmados": "estado_confirmacion",
        "informes": "estado_informe",
    }[seccion]
    eliminado = not bool(item.get(campo_estado, 1))
    return render_template(
        "modulo_admin/detalle.html",
        seccion=seccion,
        config=ADMIN_SECTIONS[seccion],
        item=item,
        item_id=item_id,
        modo="ver" if eliminado else (clean_text(request.args.get("modo"), 20) or "ver"),
        eliminado=eliminado,
    )


def eliminar_item_admin(seccion, item_id):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))
    _delete_item(seccion, item_id)
    flash("Registro eliminado.", "success")
    return redirect(url_for("admin.panel", seccion=seccion))


def reactivar_item_admin(seccion, item_id):
    if seccion not in ADMIN_SECTIONS:
        return redirect(url_for("admin.panel", seccion="usuarios"))

    reactivadores = {
        "usuarios": (reactivar_usuario_admin, "Usuario"),
        "articulos": (reactivar_articulo_admin, "Artículo"),
        "mascotas": (reactivar_mascota_admin, "Mascota"),
        "alertas": (reactivar_alerta_admin, "Alerta"),
        "avistamientos": (reactivar_avistamiento_admin, "Avistamiento"),
        "avistamientos_confirmados": (reactivar_avistamiento_confirmado_admin, "Confirmación de avistamiento"),
        "informes": (reactivar_informe_admin, "Informe"),
    }

    reactivar_fn, nombre = reactivadores.get(seccion, (None, "Registro"))
    if not reactivar_fn:
        flash(f"No se puede reactivar esta sección.", "error")
        return redirect(url_for("admin.panel", seccion=seccion, vista="eliminados"))

    if reactivar_fn(item_id):
        flash(f"{nombre} reactivado.", "success")
    else:
        flash(f"No fue posible reactivar el {nombre.lower()}.", "error")
    return redirect(url_for("admin.panel", seccion=seccion, vista="eliminados"))


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
        estado_mascota = clean_text(request.form.get("estado"), 50).lower()
        if estado_mascota not in VALID_PET_STATES:
            flash("Selecciona un estado v\u00e1lido para la mascota.", "error")
        else:
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
                estado_mascota,
            )
            flash("Mascota actualizada.", "success")
    elif seccion == "articulos":
        actualizar_articulo_admin(
            item_id,
            clean_text(request.form.get("titulo"), 255),
            clean_text(request.form.get("contenido"), 10000),
            clean_text(request.form.get("url_imagen"), 255),
        )
        flash("Artículo actualizado.", "success")
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
            clean_text(request.form.get("titulo"), 120),
            clean_text(request.form.get("tipo_informe"), 80),
            clean_text(request.form.get("descripcion"), 3000),
        )
        flash("Informe actualizado.", "success")
    return redirect(url_for("admin.detalle", seccion=seccion, item_id=item_id))


def _delete_item(seccion, item_id):
    deletes = {
        "usuarios": eliminar_usuario_admin,
        "articulos": eliminar_articulo_admin,
        "mascotas": eliminar_mascota_admin,
        "alertas": eliminar_alerta_admin,
        "avistamientos": eliminar_avistamiento_admin,
        "informes": eliminar_informe_admin,
    }
    if seccion != "informes":
        return deletes[seccion](item_id)

    informe = obtener_informe_admin(item_id)
    eliminado = deletes[seccion](item_id)
    if eliminado and informe:
        _eliminar_archivos_informe(informe)
    return eliminado


def _eliminar_archivos_informe(informe):
    """Elimina los dos adjuntos privados de un informe ya desactivado."""
    for nombre_archivo in (informe.get("ruta_pdf"), informe.get("ruta_excel")):
        ruta_archivo = ruta_archivo_informe(nombre_archivo)
        if ruta_archivo:
            try:
                os.remove(ruta_archivo)
            except OSError:
                # El registro ya está desactivado; no bloqueamos la operación si
                # el archivo fue retirado manualmente o está siendo usado.
                pass


def _eliminar_archivo(nombre_archivo):
    ruta_archivo = ruta_archivo_informe(nombre_archivo)
    if ruta_archivo:
        try:
            os.remove(ruta_archivo)
        except OSError:
            pass


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
        # La tabla conserva metadatos; los contenidos completos viven en PDF y Excel.
        descripcion = f"Archivos PDF y Excel generados: {preview['titulo']}"
        nombre_pdf = crear_pdf_informe(preview)
        try:
            nombre_excel = crear_excel_informe(preview)
        except Exception:
            _eliminar_archivo(nombre_pdf)
            raise
        try:
            crear_informe_admin(session.get("usuario_id"), titulo, tipo, descripcion, nombre_pdf, nombre_excel)
        except RuntimeError as exc:
            _eliminar_archivo(nombre_pdf)
            _eliminar_archivo(nombre_excel)
            flash(f"{exc} Ejecuta Documentacion/migracion_informes_dos_formatos.sql.", "error")
            return redirect(url_for("admin.panel", seccion="informes"))
        except Exception:
            _eliminar_archivo(nombre_pdf)
            _eliminar_archivo(nombre_excel)
            raise
        flash("Informe en PDF y Excel generado y guardado correctamente.", "success")
    else:
        session["informe_preview"] = preview
    return redirect(url_for("admin.panel", seccion="informes"))


def entregar_pdf_informe(id_informe, formato="pdf", descargar=False):
    if formato not in {"pdf", "excel"}:
        flash("Formato de informe no válido.", "error")
        return redirect(url_for("admin.panel", seccion="informes"))

    informe = obtener_informe_admin(id_informe)
    if not informe:
        flash("El archivo solicitado no está disponible.", "error")
        return redirect(url_for("admin.panel", seccion="informes"))

    nombre_archivo = informe.get("ruta_pdf") if formato == "pdf" else informe.get("ruta_excel")
    extension = ".pdf" if formato == "pdf" else ".xlsx"
    ruta_archivo = ruta_archivo_informe(nombre_archivo) if str(nombre_archivo or "").lower().endswith(extension) else None
    if not ruta_archivo:
        try:
            preview = {
                "titulo": informe.get("titulo") or f"Informe {id_informe}",
                "tipo": informe.get("tipo_informe") or "informe",
                "fecha_inicio": None,
                "fecha_fin": None,
                "datos": [_serializar_fila(fila) for fila in generar_datos_informe(informe.get("tipo_informe"), limite=10)],
            }
            nombre_pdf = crear_pdf_informe(preview)
            try:
                nombre_excel = crear_excel_informe(preview)
            except Exception:
                _eliminar_archivo(nombre_pdf)
                raise
            actualizar_archivos_informe(id_informe, nombre_pdf, nombre_excel)
            _eliminar_archivo(informe.get("ruta_pdf"))
            _eliminar_archivo(informe.get("ruta_excel"))
            nombre_archivo = nombre_pdf if formato == "pdf" else nombre_excel
            ruta_archivo = ruta_archivo_informe(nombre_archivo)
        except Exception:
            flash("No fue posible regenerar el archivo solicitado.", "error")
            return redirect(url_for("admin.panel", seccion="informes"))
    if not ruta_archivo:
        flash("No se encontró el archivo solicitado de este informe.", "error")
        return redirect(url_for("admin.panel", seccion="informes"))
    mimetype = "application/pdf" if formato == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    extension = "pdf" if formato == "pdf" else "xlsx"
    return send_file(ruta_archivo, mimetype=mimetype, as_attachment=descargar, download_name=f"informe_busca_huellas_{id_informe}.{extension}")



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
    """Convierte valores de BD a texto seguro y consistente para ambos formatos."""
    resultado = {}
    for key, value in row.items():
        if value is None and key.startswith("fecha"):
            resultado[key] = "Sin fecha registrada"
        elif value is None:
            resultado[key] = ""
        elif isinstance(value, datetime):
            resultado[key] = value.strftime("%d/%m/%Y %H:%M")
        elif isinstance(value, date):
            resultado[key] = value.strftime("%d/%m/%Y")
        else:
            resultado[key] = str(value)
    return resultado


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
