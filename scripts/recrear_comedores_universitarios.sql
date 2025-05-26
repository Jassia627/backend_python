-- Script para recrear la tabla comedores_universitarios directamente
-- Primero eliminamos las tablas existentes si existen
DROP TABLE IF EXISTS comedores_universitarios CASCADE;
DROP TABLE IF EXISTS comedor_universitario CASCADE;
DROP VIEW IF EXISTS comedores_universitarios;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.comedores_universitarios (
  id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
  estudiante_id uuid NOT NULL,
  condicion_socioeconomica character varying(50) NOT NULL,
  fecha_solicitud date,
  aprobado boolean DEFAULT false,
  observaciones TEXT,
  tipo_subsidio character varying(100),
  periodo_academico character varying(50),
  estrato integer,
  raciones_asignadas integer DEFAULT 0,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT comedores_universitarios_pkey PRIMARY KEY (id),
  CONSTRAINT comedores_universitarios_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_comedores_estudiante_id ON public.comedores_universitarios USING btree (estudiante_id);
