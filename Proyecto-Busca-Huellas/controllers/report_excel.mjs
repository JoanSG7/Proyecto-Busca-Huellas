import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) throw new Error("Se requiere el archivo de datos y la ruta de salida.");
const preview = JSON.parse(await fs.readFile(inputPath, "utf8"));
const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Informe");
const rows = preview.datos || [];
const columns = rows.length ? Object.keys(rows[0]) : ["Resultado"];
const lastColumn = String.fromCharCode(64 + Math.min(columns.length, 26));

sheet.showGridLines = false;
sheet.mergeCells(`A1:${lastColumn}1`);
sheet.getRange("A1").values = [["BUSCA HUELLAS"]];
sheet.getRange("A1").format = { fill: "#0F5238", font: { bold: true, color: "#FFFFFF", size: 16 }, horizontalAlignment: "center", verticalAlignment: "center" };
sheet.getRange("A1").format.rowHeight = 30;
sheet.mergeCells(`A2:${lastColumn}2`);
sheet.getRange("A2").values = [[preview.titulo]];
sheet.getRange("A2").format = { font: { bold: true, color: "#0F5238", size: 14 }, horizontalAlignment: "center" };
sheet.mergeCells(`A3:${lastColumn}3`);
const dates = preview.fecha_inicio || preview.fecha_fin ? `Periodo: ${preview.fecha_inicio || "Inicio"} a ${preview.fecha_fin || "Hoy"}` : "Sin filtro de fechas";
sheet.getRange("A3").values = [[`${preview.tipo.replaceAll("_", " ")} - ${dates}`]];
sheet.getRange("A3").format = { font: { color: "#56615A", italic: true }, horizontalAlignment: "center" };

sheet.getRange(`A5:${lastColumn}5`).values = [columns.map((column) => column.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase()))];
sheet.getRange(`A5:${lastColumn}5`).format = { fill: "#0F5238", font: { bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", wrapText: true };
if (rows.length) {
  sheet.getRangeByIndexes(5, 0, rows.length, columns.length).values = rows.map((row) => columns.map((column) => row[column] ?? ""));
  const dataRange = sheet.getRangeByIndexes(4, 0, rows.length + 1, columns.length);
  dataRange.format.borders = { preset: "all", style: "thin", color: "#D8DED7" };
  sheet.tables.add(`A5:${lastColumn}${rows.length + 5}`, true, "InformeDatos");
} else {
  sheet.mergeCells(`A6:${lastColumn}6`);
  sheet.getRange("A6").values = [["No se encontraron resultados con los filtros seleccionados."]];
  sheet.getRange("A6").format = { horizontalAlignment: "center", font: { color: "#56615A", italic: true } };
}
sheet.getRange(`A1:${lastColumn}${Math.max(6, rows.length + 5)}`).format.autofitColumns();
for (let index = 0; index < columns.length; index += 1) {
  const column = sheet.getRangeByIndexes(0, index, Math.max(6, rows.length + 5), 1);
  if (column.format.columnWidth > 28) column.format.columnWidth = 28;
  if (column.format.columnWidth < 13) column.format.columnWidth = 13;
}
sheet.freezePanes.freezeRows(5);

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
