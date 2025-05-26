-- Script para modificar la tabla programas y establecer un valor por defecto para nivel
-- Primero modificamos la columna nivel para que tenga un valor por defecto
ALTER TABLE programas 
ALTER COLUMN nivel SET DEFAULT 'Pregrado';

-- Actualizamos los registros existentes que tienen nivel NULL
UPDATE programas
SET nivel = 'Pregrado'
WHERE nivel IS NULL;

-- Verificamos la estructura actual de la tabla
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'programas'
ORDER BY ordinal_position;
