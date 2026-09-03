-- Ejecutar después de las migraciones de informes PDF y Excel.
ALTER TABLE informe
    ADD COLUMN titulo VARCHAR(120) NULL AFTER id_usuario;

-- Conserva una etiqueta útil para los informes existentes.
UPDATE informe
SET titulo = CONCAT('Informe ', id_informe)
WHERE titulo IS NULL OR titulo = '';
