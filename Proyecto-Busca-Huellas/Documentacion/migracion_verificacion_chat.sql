-- Ejecutar una sola vez para persistir la verificación de correo requerida por el chat.
ALTER TABLE usuario
    ADD COLUMN correo_verificado TINYINT(1) NOT NULL DEFAULT 0;

-- Las cuentas existentes se mantienen habilitadas para no bloquear usuarios ya registrados.
UPDATE usuario SET correo_verificado = 1;
