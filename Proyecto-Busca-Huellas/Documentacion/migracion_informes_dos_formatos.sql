-- Ejecutar después de las migraciones de informes anteriores.
-- Cada nuevo informe conservará sus dos archivos: PDF y Excel.
ALTER TABLE informe
    ADD COLUMN ruta_excel VARCHAR(255) NULL AFTER ruta_pdf;
