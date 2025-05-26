-- Script para modificar la tabla apoyos_socioeconomicos
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS apoyos_socioeconomicos CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.apoyos_socioeconomicos (
  id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
  estudiante_id uuid NOT NULL,
  tipo_apoyo VARCHAR(100),  -- Ahora es opcional
  monto DECIMAL(10, 2),
  fecha_otorgamiento DATE,
  fecha_finalizacion DATE,
  estado VARCHAR(50) DEFAULT 'activo',
  tipo_vulnerabilidad VARCHAR(100),
  observaciones TEXT,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT apoyos_socioeconomicos_pkey PRIMARY KEY (id),
  CONSTRAINT apoyos_socioeconomicos_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_apoyos_estudiante_id ON public.apoyos_socioeconomicos USING btree (estudiante_id);
