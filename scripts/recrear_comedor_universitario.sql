-- Script para recrear la tabla comedor_universitario con todas las columnas necesarias
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS comedor_universitario CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.comedor_universitario (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    condicion_socioeconomica VARCHAR(50) NOT NULL,
    fecha_solicitud DATE,
    aprobado BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    tipo_subsidio VARCHAR(100),
    periodo_academico VARCHAR(50),
    estrato INTEGER,
    raciones_asignadas INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT comedor_universitario_pkey PRIMARY KEY (id)
);

-- Creamos un índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_comedor_estudiante_id ON comedor_universitario(estudiante_id);
