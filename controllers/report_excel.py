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
