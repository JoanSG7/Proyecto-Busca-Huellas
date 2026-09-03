-- Ejecutar una sola vez en la base de datos busca_huellas.
CREATE TABLE avistamiento_confirmado (
    id_confirmacion INT NOT NULL AUTO_INCREMENT,
    id_avistamiento INT NOT NULL,
    id_usuario_alerto INT NOT NULL,
    id_usuario_dueno INT NOT NULL,
    id_mascota INT NOT NULL,
    fecha_confirmacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_confirmacion),
    UNIQUE KEY uq_confirmacion_avistamiento (id_avistamiento),
    KEY idx_confirmacion_alerto (id_usuario_alerto),
    KEY idx_confirmacion_dueno (id_usuario_dueno),
    KEY idx_confirmacion_mascota (id_mascota),
    CONSTRAINT fk_confirmacion_avistamiento FOREIGN KEY (id_avistamiento) REFERENCES avistamiento (id_avistamiento),
    CONSTRAINT fk_confirmacion_usuario_alerto FOREIGN KEY (id_usuario_alerto) REFERENCES usuario (id_usuario),
    CONSTRAINT fk_confirmacion_usuario_dueno FOREIGN KEY (id_usuario_dueno) REFERENCES usuario (id_usuario),
    CONSTRAINT fk_confirmacion_mascota FOREIGN KEY (id_mascota) REFERENCES mascota (id_mascota)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
