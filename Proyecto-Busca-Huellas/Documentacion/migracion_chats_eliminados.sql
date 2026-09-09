-- Oculta un chat únicamente para el usuario que decide eliminarlo.
CREATE TABLE chat_eliminado (
    id_chat_eliminado INT NOT NULL AUTO_INCREMENT,
    id_alerta INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_eliminacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_chat_eliminado),
    UNIQUE KEY uq_chat_eliminado_usuario (id_alerta, id_usuario),
    CONSTRAINT fk_chat_eliminado_alerta FOREIGN KEY (id_alerta) REFERENCES alerta (id_alerta),
    CONSTRAINT fk_chat_eliminado_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
