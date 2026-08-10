ALTER TABLE usuario
    ADD COLUMN tema_preferido VARCHAR(20) NOT NULL DEFAULT 'claro',
    ADD COLUMN reducir_movimiento TINYINT(1) NOT NULL DEFAULT 0;
