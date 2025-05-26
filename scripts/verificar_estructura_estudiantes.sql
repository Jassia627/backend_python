-- Script para verificar la estructura actual de la tabla estudiantes
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public' 
    AND table_name = 'estudiantes'
ORDER BY 
    ordinal_position;
