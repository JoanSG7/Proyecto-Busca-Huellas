-- Ejecuta este archivo una sola vez si la tabla avistamiento_confirmado ya
-- existe y fue creada antes de añadir la eliminación lógica.
-- 1 = confirmación activa; 0 = eliminada lógicamente y recuperable.

ALTER TABLE avistamiento_confirmado
    ADD COLUMN estado_confirmacion TINYINT(1) NOT NULL DEFAULT 1;

CREATE INDEX idx_confirmacion_estado
    ON avistamiento_confirmado (estado_confirmacion);
