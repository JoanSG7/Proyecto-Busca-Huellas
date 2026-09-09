-- Ejecutar una sola vez en una base de datos existente.
-- Conserva la fecha de registro y permite guardar la hora exacta de nuevas mascotas.
ALTER TABLE mascota
    MODIFY COLUMN fecha_registro DATETIME NULL;
