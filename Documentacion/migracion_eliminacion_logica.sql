-- Ejecuta este archivo una sola vez sobre la base de datos busca_huellas.
-- 1 = registro activo; 0 = eliminado lógicamente y conservado para auditoría.

ALTER TABLE usuario
    ADD COLUMN estado_usuario TINYINT(1) NOT NULL DEFAULT 1;

ALTER TABLE mascota
    ADD COLUMN estado_mascota TINYINT(1) NOT NULL DEFAULT 1;

-- estado_alerta ya representa el avance de la alerta; esta columna indica si existe.
ALTER TABLE alerta
    ADD COLUMN estado_alerta_registro TINYINT(1) NOT NULL DEFAULT 1;

ALTER TABLE avistamiento
    ADD COLUMN estado_avistamiento TINYINT(1) NOT NULL DEFAULT 1;

ALTER TABLE articulo
    ADD COLUMN estado_articulo TINYINT(1) NOT NULL DEFAULT 1;

ALTER TABLE informe
    ADD COLUMN estado_informe TINYINT(1) NOT NULL DEFAULT 1;

CREATE INDEX idx_usuario_estado ON usuario (estado_usuario);
CREATE INDEX idx_mascota_estado ON mascota (estado_mascota);
CREATE INDEX idx_alerta_estado_registro ON alerta (estado_alerta_registro);
CREATE INDEX idx_avistamiento_estado ON avistamiento (estado_avistamiento);
CREATE INDEX idx_articulo_estado ON articulo (estado_articulo);
CREATE INDEX idx_informe_estado ON informe (estado_informe);
