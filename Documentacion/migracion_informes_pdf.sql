-- Ejecutar una sola vez en la base de datos busca_huellas.
-- El PDF se conserva como archivo privado; la tabla almacena sus metadatos y su nombre seguro.
ALTER TABLE informe
    ADD COLUMN ruta_pdf VARCHAR(255) NULL AFTER descripcion;
