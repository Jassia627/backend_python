-- Script completo para recrear la tabla orientaciones_vocacionales
-- Asegurarse de que la extensión uuid-ossp esté habilitada
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Eliminar la tabla si existe
DROP TABLE IF EXISTS orientaciones_vocacionales CASCADE;

-- Crear la tabla con todas las columnas necesarias
CREATE TABLE IF NOT EXISTS orientaciones_vocacionales (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
   fecha_orientacion DATE,
   fecha_ingreso_programa DATE,
   tipo_participante VARCHAR(100),
   area_interes VARCHAR(100),
   resultado TEXT,
   orientador VARCHAR(200),
   observaciones TEXT,
   riesgo_spadies VARCHAR(50),
   created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
   updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_orientaciones_estudiante_id ON orientaciones_vocacionales(estudiante_id);
