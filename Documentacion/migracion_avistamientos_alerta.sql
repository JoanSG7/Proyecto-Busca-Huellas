-- Ejecutar una sola vez en una base de datos existente.
-- Relaciona cada avistamiento con su alerta y conserva su hora exacta.
ALTER TABLE avistamiento
    ADD COLUMN id_alerta INT NULL AFTER id_avistamiento,
    MODIFY COLUMN fecha_avistamiento DATETIME NULL,
    ADD INDEX idx_avistamiento_alerta (id_alerta),
    ADD CONSTRAINT avistamiento_ibfk_2 FOREIGN KEY (id_alerta) REFERENCES alerta (id_alerta);
