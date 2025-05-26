-- Script para modificar la tabla comedor_universitario
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS comedor_universitario CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.comedor_universitario (
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
  CONSTRAINT comedor_universitario_pkey PRIMARY KEY (id),
  CONSTRAINT comedor_universitario_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_comedor_estudiante_id ON public.comedor_universitario USING btree (estudiante_id);

-- Creamos un alias para la tabla (para mantener compatibilidad con el código que usa el plural)
CREATE VIEW comedores_universitarios AS SELECT * FROM comedor_universitario;
