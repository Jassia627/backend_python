-- Script para crear la tabla servicios
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS servicios CASCADE;

-- Creamos la tabla con todas las columnas necesarias
CREATE TABLE public.servicios (
  id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(200) NOT NULL,
  descripcion TEXT,
  tipo VARCHAR(100),
  estado BOOLEAN DEFAULT TRUE,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT servicios_pkey PRIMARY KEY (id)
);

-- Creamos el índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_servicios_codigo ON public.servicios USING btree (codigo);
