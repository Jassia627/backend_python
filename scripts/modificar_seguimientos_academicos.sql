-- Script para modificar la tabla seguimientos_academicos
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS seguimientos_academicos CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.seguimientos_academicos (
  id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
  estudiante_id uuid NOT NULL,
  fecha_seguimiento DATE,  -- Ahora es opcional
  periodo_academico VARCHAR(20),
  promedio_actual DECIMAL(3, 2),
  materias_perdidas INTEGER DEFAULT 0,
  materias_cursadas INTEGER DEFAULT 0,
  observaciones TEXT,
  observaciones_permanencia TEXT,
  requiere_tutoria BOOLEAN DEFAULT FALSE,
  estado_participacion VARCHAR(50),
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT seguimientos_academicos_pkey PRIMARY KEY (id),
  CONSTRAINT seguimientos_academicos_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_seguimientos_estudiante_id ON public.seguimientos_academicos USING btree (estudiante_id);
