-- Script para actualizar la tabla remisiones_psicologicas
-- Agregar la columna fecha_remision que falta
ALTER TABLE public.remisiones_psicologicas 
ADD COLUMN IF NOT EXISTS fecha_remision DATE;

-- Actualizar registros existentes para copiar la fecha actual a fecha_remision
UPDATE public.remisiones_psicologicas 
SET fecha_remision = fecha 
WHERE fecha_remision IS NULL;

-- Comentario explicativo
COMMENT ON COLUMN public.remisiones_psicologicas.fecha_remision IS 'Fecha en que se realizó la remisión';
