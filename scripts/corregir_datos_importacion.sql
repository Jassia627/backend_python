-- Script para corregir los problemas de importación de datos
-- 1. Actualizar la tabla comedor_universitario para agregar valores por defecto a tipo_comida
UPDATE public.comedor_universitario
SET tipo_comida = 'Almuerzo'
WHERE tipo_comida IS NULL;

-- 2. Actualizar la tabla remisiones_psicologicas para agregar valores por defecto a campos obligatorios
UPDATE public.remisiones_psicologicas
SET nombre_estudiante = 'Estudiante importado'
WHERE nombre_estudiante IS NULL;

UPDATE public.remisiones_psicologicas
SET numero_documento = '0000000000'
WHERE numero_documento IS NULL;

UPDATE public.remisiones_psicologicas
SET programa_academico = 'No especificado'
WHERE programa_academico IS NULL;

UPDATE public.remisiones_psicologicas
SET semestre = '1'
WHERE semestre IS NULL;

UPDATE public.remisiones_psicologicas
SET motivo_remision = 'Importado desde CSV'
WHERE motivo_remision IS NULL;

UPDATE public.remisiones_psicologicas
SET docente_remite = 'Docente por defecto'
WHERE docente_remite IS NULL;

UPDATE public.remisiones_psicologicas
SET correo_docente = 'docente@ejemplo.com'
WHERE correo_docente IS NULL;

UPDATE public.remisiones_psicologicas
SET telefono_docente = '0000000000'
WHERE telefono_docente IS NULL;

UPDATE public.remisiones_psicologicas
SET fecha = CURRENT_DATE
WHERE fecha IS NULL;

UPDATE public.remisiones_psicologicas
SET hora = '12:00'
WHERE hora IS NULL;

UPDATE public.remisiones_psicologicas
SET tipo_remision = 'individual'
WHERE tipo_remision IS NULL;

-- Asegurarse de que fecha_remision tenga un valor (copiado de fecha si existe)
UPDATE public.remisiones_psicologicas
SET fecha_remision = fecha
WHERE fecha_remision IS NULL AND fecha IS NOT NULL;

-- Si ambos son NULL, usar la fecha actual
UPDATE public.remisiones_psicologicas
SET fecha_remision = CURRENT_DATE
WHERE fecha_remision IS NULL AND fecha IS NULL;
