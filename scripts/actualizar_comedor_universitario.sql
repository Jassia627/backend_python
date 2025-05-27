-- Script para actualizar la tabla comedor_universitario
-- Agregar la columna tipo_comida que falta (con un valor por defecto)
ALTER TABLE public.comedor_universitario 
ADD COLUMN IF NOT EXISTS tipo_comida VARCHAR(50) NOT NULL DEFAULT 'Almuerzo';

-- Actualizar registros existentes para asignar un valor por defecto
UPDATE public.comedor_universitario 
SET tipo_comida = 'Almuerzo' 
WHERE tipo_comida IS NULL;

-- Comentario explicativo
COMMENT ON COLUMN public.comedor_universitario.tipo_comida IS 'Tipo de comida solicitada (desayuno, almuerzo, cena, etc.)';
