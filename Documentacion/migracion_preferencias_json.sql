-- Las preferencias se almacenan en un solo documento JSON por usuario.
ALTER TABLE usuario
    ADD COLUMN preferencias JSON NULL;

-- Conserva las preferencias que se alcanzaron a guardar con la versión anterior.
UPDATE usuario
SET preferencias = JSON_OBJECT(
    'tema', COALESCE(tema_preferido, 'claro'),
    'reducir_movimiento', IF(COALESCE(reducir_movimiento, 0) = 1, TRUE, FALSE)
)
WHERE preferencias IS NULL;

ALTER TABLE usuario
    DROP COLUMN tema_preferido,
    DROP COLUMN reducir_movimiento;
