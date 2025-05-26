-- Script para modificar la tabla asistencias y agregar la columna servicio_id
-- Primero verificamos si la columna ya existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'asistencias' AND column_name = 'servicio_id'
    ) THEN
        -- Agregamos la columna servicio_id como NOT NULL con referencia a la tabla servicios
        ALTER TABLE asistencias 
        ADD COLUMN servicio_id UUID NOT NULL REFERENCES servicios(id) ON DELETE CASCADE;
        
        -- Creamos un índice para mejorar el rendimiento
        CREATE INDEX IF NOT EXISTS idx_asistencias_servicio_id ON asistencias(servicio_id);
    END IF;
END
$$;
