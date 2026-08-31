-- Ejecutar en las bases de datos que ya aplicaron migracion_informes_excel.sql.
-- El formato deja de ser necesario porque cada informe siempre guarda PDF y Excel.
ALTER TABLE informe
    DROP COLUMN formato_archivo;
