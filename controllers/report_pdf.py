"""Generación y entrega de los informes PDF del panel administrativo."""

import os
import uuid
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle


REPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "private_reports"))


def _texto_pdf(valor):
    return escape(str(valor or "-"))


def ruta_archivo_informe(nombre_archivo):
    """Devuelve la ruta de un archivo de informe dentro del almacenamiento privado."""
    if not nombre_archivo:
        return None
    ruta = os.path.abspath(os.path.join(REPORTS_FOLDER, os.path.basename(nombre_archivo)))
    return ruta if ruta.startswith(REPORTS_FOLDER + os.sep) and os.path.isfile(ruta) else None


# Se conserva para no romper usos existentes del módulo.
def ruta_pdf_informe(nombre_archivo):
    return ruta_archivo_informe(nombre_archivo)


def crear_pdf_informe(preview):
    """Crea un PDF profesional y devuelve el nombre seguro que se guarda en la BD."""
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    nombre_archivo = f"informe_{uuid.uuid4().hex}.pdf"
    ruta_salida = os.path.join(REPORTS_FOLDER, nombre_archivo)
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("InformeTitulo", parent=estilos["Title"], fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=colors.HexColor("#0F5238"), alignment=TA_CENTER, spaceAfter=8)
    subtitulo = ParagraphStyle("InformeSubtitulo", parent=estilos["Normal"], fontSize=9, leading=13, textColor=colors.HexColor("#56615A"), alignment=TA_CENTER, spaceAfter=16)
    normal = ParagraphStyle("InformeNormal", parent=estilos["BodyText"], fontSize=8, leading=11)
    documento = SimpleDocTemplate(ruta_salida, pagesize=A4, rightMargin=1.5 * cm, leftMargin=1.5 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm, title=preview["titulo"], author="Busca Huellas")
    rango = "Sin filtro de fechas"
    if preview.get("fecha_inicio") or preview.get("fecha_fin"):
        rango = f"Periodo: {preview.get('fecha_inicio') or 'Inicio'} a {preview.get('fecha_fin') or 'Hoy'}"
    historia = [
        Paragraph("BUSCA HUELLAS", subtitulo),
        Paragraph(_texto_pdf(preview["titulo"]), titulo),
        Paragraph(f"Informe: {_texto_pdf(preview['tipo'].replace('_', ' ').title())}<br/>{_texto_pdf(rango)}<br/>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitulo),
    ]
    datos = preview.get("datos") or []
    if not datos:
        historia.append(Paragraph("No se encontraron resultados con los filtros seleccionados.", normal))
    else:
        columnas = list(datos[0].keys())
        filas = [[Paragraph(_texto_pdf(str(columna).replace("_", " ").title()), normal) for columna in columnas]]
        for registro in datos:
            filas.append([Paragraph(_texto_pdf(registro.get(columna)), normal) for columna in columnas])
        ancho = (A4[0] - documento.leftMargin - documento.rightMargin) / len(columnas)
        tabla = LongTable(filas, colWidths=[ancho] * len(columnas), repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F5238")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D8DED7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8F5")]),
        ]))
        historia.extend([Spacer(1, 0.15 * cm), tabla])
    documento.build(historia, onFirstPage=_pie_de_pagina, onLaterPages=_pie_de_pagina)
    return nombre_archivo


def _pie_de_pagina(canvas, documento):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8DED7"))
    canvas.line(documento.leftMargin, 1.15 * cm, A4[0] - documento.rightMargin, 1.15 * cm)
    canvas.setFillColor(colors.HexColor("#56615A"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(documento.leftMargin, 0.75 * cm, "Busca Huellas - Informe administrativo")
    canvas.drawRightString(A4[0] - documento.rightMargin, 0.75 * cm, f"Página {documento.page}")
    canvas.restoreState()
