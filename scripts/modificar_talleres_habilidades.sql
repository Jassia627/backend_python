-- Script para modificar la tabla talleres_habilidades
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS talleres_habilidades CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.talleres_habilidades (
  id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
  estudiante_id uuid NOT NULL,
  nombre_taller VARCHAR(200) NOT NULL,
  fecha_inicio DATE,  -- Ahora es opcional
  fecha_fin DATE,
  fecha_taller DATE,
  horas_completadas INTEGER DEFAULT 0,
  certificado BOOLEAN DEFAULT FALSE,
  facilitador VARCHAR(200),
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  observaciones TEXT,  -- Agregamos esta columna que parece estar en uso
  CONSTRAINT talleres_habilidades_pkey PRIMARY KEY (id),
  CONSTRAINT talleres_habilidades_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_talleres_estudiante_id ON public.talleres_habilidades USING btree (estudiante_id);
