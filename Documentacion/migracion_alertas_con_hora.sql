-- Ejecutar una sola vez en la base de datos busca_huellas ya existente.
-- Conserva las alertas actuales y permite guardar el texto y la hora exacta.
ALTER TABLE alerta
    ADD COLUMN mensaje TEXT NULL AFTER confirmacion,
    MODIFY COLUMN fecha_alerta DATETIME NULL;
