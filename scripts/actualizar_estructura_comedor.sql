-- Script para actualizar la estructura de la tabla comedor_universitario
-- Agregar las columnas que faltan para que coincida con los datos que se están intentando insertar

-- Primero, agregar la columna tipo_subsidio si no existe
ALTER TABLE public.comedor_universitario 
ADD COLUMN IF NOT EXISTS tipo_subsidio VARCHAR(50);

-- Luego, agregar la columna periodo_academico si no existe
ALTER TABLE public.comedor_universitario 
ADD COLUMN IF NOT EXISTS periodo_academico VARCHAR(50);

-- Finalmente, agregar la columna estrato si no existe
ALTER TABLE public.comedor_universitario 
ADD COLUMN IF NOT EXISTS estrato INTEGER;

-- Comentarios explicativos
COMMENT ON COLUMN public.comedor_universitario.tipo_subsidio IS 'Tipo de subsidio otorgado al estudiante';
COMMENT ON COLUMN public.comedor_universitario.periodo_academico IS 'Periodo académico en el que se otorga el beneficio';
COMMENT ON COLUMN public.comedor_universitario.estrato IS 'Estrato socioeconómico del estudiante';
