-- Script para recrear la tabla asistencias con todas las columnas necesarias
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS asistencias CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.asistencias (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    servicio_id uuid NOT NULL REFERENCES servicios(id) ON DELETE CASCADE,
    actividad VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    asistio BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT asistencias_pkey PRIMARY KEY (id)
);

-- Creamos índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_asistencias_estudiante_id ON asistencias(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_servicio_id ON asistencias(servicio_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON asistencias(fecha);
