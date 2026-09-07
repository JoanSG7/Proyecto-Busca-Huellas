-- Ejecuta este archivo una sola vez en bases de datos creadas antes de los
-- indicadores de notificaciones y mensajes no leídos.

ALTER TABLE alerta
    ADD COLUMN leida TINYINT(1) NOT NULL DEFAULT 0;

CREATE INDEX idx_alerta_leida ON alerta (leida);

ALTER TABLE mensaje
    ADD COLUMN leido TINYINT(1) NOT NULL DEFAULT 0;

CREATE INDEX idx_mensaje_receptor_leido ON mensaje (usuario_receptor, leido);
