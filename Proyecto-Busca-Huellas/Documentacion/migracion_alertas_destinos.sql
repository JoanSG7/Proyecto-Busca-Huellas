-- Ejecutar después de migracion_alertas_con_hora.sql en una base de datos existente.
-- Conserva las notificaciones actuales y permite abrir el chat que generó cada aviso de mensaje.
ALTER TABLE alerta
    ADD COLUMN id_alerta_origen INT NULL AFTER id_mascota,
    ADD INDEX idx_alerta_origen (id_alerta_origen),
    ADD CONSTRAINT alerta_ibfk_3 FOREIGN KEY (id_alerta_origen) REFERENCES alerta (id_alerta);
