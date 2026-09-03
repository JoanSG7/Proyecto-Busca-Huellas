
"""Generación de libros Excel para los informes administrativos.

No depende de Node ni de paquetes instalados fuera del proyecto.  Esto es
importante porque los informes se generan en el servidor de la aplicación,
no en el entorno de desarrollo de Codex.
"""

import os
import uuid
import zipfile
from xml.sax.saxutils import escape

from controllers.report_pdf import REPORTS_FOLDER


def crear_excel_informe(preview):
    """Crea un .xlsx válido y devuelve el nombre seguro para almacenar en BD."""
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    nombre_archivo = f"informe_{uuid.uuid4().hex}.xlsx"
    ruta_salida = os.path.join(REPORTS_FOLDER, nombre_archivo)
    filas = preview.get("datos") or []
    columnas = list(filas[0].keys()) if filas else ["Resultado"]
    periodo = (
        f"Periodo: {preview.get('fecha_inicio') or 'Inicio'} a {preview.get('fecha_fin') or 'Hoy'}"
        if preview.get("fecha_inicio") or preview.get("fecha_fin")
        else "Sin filtro de fechas"
    )
    contenido = [
        ["BUSCA HUELLAS"],
        [preview.get("titulo") or "Informe personalizado"],
        [f"{str(preview.get('tipo') or '').replace('_', ' ')} - {periodo}"],
        [],
        [str(columna).replace("_", " ").title() for columna in columnas],
    ]
    if filas:
        contenido.extend([[fila.get(columna, "") for columna in columnas] for fila in filas])
    else:
        contenido.append(["No se encontraron resultados con los filtros seleccionados."])

    try:
        with zipfile.ZipFile(ruta_salida, "w", zipfile.ZIP_DEFLATED) as libro:
            libro.writestr("[Content_Types].xml", _CONTENT_TYPES)
            libro.writestr("_rels/.rels", _RELS)
            libro.writestr("xl/workbook.xml", _WORKBOOK)
            libro.writestr("xl/_rels/workbook.xml.rels", _WORKBOOK_RELS)
            libro.writestr("xl/styles.xml", _STYLES)
            libro.writestr("xl/worksheets/sheet1.xml", _hoja_xml(contenido, len(columnas), bool(filas)))
    except Exception:
        if os.path.isfile(ruta_salida):
            os.remove(ruta_salida)
        raise
    return nombre_archivo


def _celda(valor, fila, columna, estilo=0):
    referencia = f"{_columna_excel(columna)}{fila}"
    texto = "" if valor is None else str(valor)
    return f'<c r="{referencia}" s="{estilo}" t="inlineStr"><is><t>{escape(texto)}</t></is></c>'


def _columna_excel(numero):
    resultado = ""
    while numero:
        numero, resto = divmod(numero - 1, 26)
        resultado = chr(65 + resto) + resultado
    return resultado


def _hoja_xml(contenido, total_columnas, tiene_datos):
    ultima_columna = _columna_excel(total_columnas)
    filas_xml = []
    for numero_fila, valores in enumerate(contenido, start=1):
        if numero_fila in (1, 2, 3):
            filas_xml.append(f'<row r="{numero_fila}"><c r="A{numero_fila}" s="{numero_fila - 1}" t="inlineStr"><is><t>{escape(str(valores[0]))}</t></is></c></row>')
        elif numero_fila == 5:
            filas_xml.append(f'<row r="5">{"".join(_celda(valor, numero_fila, indice, 3) for indice, valor in enumerate(valores, 1))}</row>')
        else:
            filas_xml.append(f'<row r="{numero_fila}">{"".join(_celda(valor, numero_fila, indice, 4 if tiene_datos else 5) for indice, valor in enumerate(valores, 1))}</row>')
    columnas = "".join(f'<col min="{indice}" max="{indice}" width="22" customWidth="1"/>' for indice in range(1, total_columnas + 1))
    merges = f'<mergeCells count="3"><mergeCell ref="A1:{ultima_columna}1"/><mergeCell ref="A2:{ultima_columna}2"/><mergeCell ref="A3:{ultima_columna}3"/></mergeCells>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>{columnas}</cols><sheetData>{''.join(filas_xml)}</sheetData>{merges}</worksheet>'''


_CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>'''
_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'''
_WORKBOOK = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Informe" sheetId="1" r:id="rId1"/></sheets></workbook>'''
_WORKBOOK_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
_STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="5"><font><sz val="11"/><name val="Calibri"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="16"/><name val="Calibri"/></font><font><b/><color rgb="FF0F5238"/><sz val="14"/><name val="Calibri"/></font><font><b/><color rgb="FFFFFFFF"/><name val="Calibri"/></font><font><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F5238"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="2"><border/><border><left style="thin"><color rgb="FFD8DED7"/></left><right style="thin"><color rgb="FFD8DED7"/></right><top style="thin"><color rgb="FFD8DED7"/></top><bottom style="thin"><color rgb="FFD8DED7"/></bottom></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="6"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf><xf numFmtId="0" fontId="2" fillId="0" borderId="0" applyFont="1" applyAlignment="1"><alignment horizontal="center"/></xf><xf numFmtId="0" fontId="3" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" wrapText="1"/></xf><xf numFmtId="0" fontId="4" fillId="0" borderId="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="4" fillId="0" borderId="0" applyAlignment="1"><alignment horizontal="center"/></xf></cellXfs></styleSheet>'''

"""Generación de libros Excel para los informes administrativos."""

import json
import os
import subprocess
import sys
import uuid

from controllers.report_pdf import REPORTS_FOLDER, ruta_pdf_informe


def crear_excel_informe(preview):
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    nombre_archivo = f"informe_{uuid.uuid4().hex}.xlsx"
    ruta_salida = os.path.join(REPORTS_FOLDER, nombre_archivo)
    ruta_entrada = os.path.join(REPORTS_FOLDER, f".informe_{uuid.uuid4().hex}.json")
    try:
        with open(ruta_entrada, "w", encoding="utf-8") as archivo:
            json.dump(preview, archivo, ensure_ascii=False)
        resultado = subprocess.run(
            ["node", os.path.join(os.path.dirname(__file__), "report_excel.mjs"), ruta_entrada, ruta_salida],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if resultado.returncode != 0 or not os.path.isfile(ruta_salida):
            raise RuntimeError(resultado.stderr.strip() or "No se pudo crear el archivo Excel.")
        return nombre_archivo
    finally:
        if os.path.isfile(ruta_entrada):
            os.remove(ruta_entrada)
