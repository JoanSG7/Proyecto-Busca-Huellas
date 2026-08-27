-- Ejecutar una sola vez en una base de datos existente.
-- Permite conservar la foto tomada como parte de un mensaje de chat.
ALTER TABLE mensaje
    ADD COLUMN url_imagen VARCHAR(255) NULL AFTER mensaje_chat;
