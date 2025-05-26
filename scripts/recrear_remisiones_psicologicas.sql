-- Script para recrear la tabla remisiones_psicologicas con todos los campos necesarios
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS remisiones_psicologicas CASCADE;

-- Creamos la tabla con todas las columnas necesarias según el frontend
CREATE TABLE public.remisiones_psicologicas (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid,
    nombre_estudiante VARCHAR(100) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    programa_academico VARCHAR(100) NOT NULL,
    semestre VARCHAR(10) NOT NULL,
    motivo_remision TEXT NOT NULL,
    docente_remite VARCHAR(100) NOT NULL,
    correo_docente VARCHAR(100) NOT NULL,
    telefono_docente VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    tipo_remision VARCHAR(50) NOT NULL,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT remisiones_psicologicas_pkey PRIMARY KEY (id)
);

-- Creamos un índice para búsquedas por estudiante_id
CREATE INDEX IF NOT EXISTS idx_remisiones_estudiante_id ON public.remisiones_psicologicas USING btree (estudiante_id);

-- Creamos un índice para búsquedas por número de documento
CREATE INDEX IF NOT EXISTS idx_remisiones_numero_documento ON public.remisiones_psicologicas USING btree (numero_documento);

-- Agregamos la restricción de clave foránea, pero permitimos NULL para estudiante_id
ALTER TABLE public.remisiones_psicologicas 
ADD CONSTRAINT remisiones_psicologicas_estudiante_id_fkey 
FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE SET NULL;

-- Comentario explicativo
COMMENT ON TABLE public.remisiones_psicologicas IS 'Tabla que almacena las remisiones psicológicas de estudiantes';
