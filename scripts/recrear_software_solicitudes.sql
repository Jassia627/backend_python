-- Script para recrear la tabla software_solicitudes con todos los campos necesarios
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS software_solicitudes CASCADE;

-- Creamos la tabla con todas las columnas necesarias según el frontend
CREATE TABLE public.software_solicitudes (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid,
    nombre_solicitante VARCHAR(100) NOT NULL,
    correo_solicitante VARCHAR(100) NOT NULL,
    telefono_solicitante VARCHAR(20),
    programa_academico VARCHAR(100) NOT NULL,
    nombre_software VARCHAR(100) NOT NULL,
    version VARCHAR(50),
    justificacion TEXT NOT NULL,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT software_solicitudes_pkey PRIMARY KEY (id)
);

-- Creamos un índice para búsquedas por estudiante_id
CREATE INDEX IF NOT EXISTS idx_software_solicitudes_estudiante_id ON public.software_solicitudes USING btree (estudiante_id);

-- Agregamos la restricción de clave foránea, pero permitimos NULL para estudiante_id
ALTER TABLE public.software_solicitudes 
ADD CONSTRAINT software_solicitudes_estudiante_id_fkey 
FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE SET NULL;

-- Comentario explicativo
COMMENT ON TABLE public.software_solicitudes IS 'Tabla que almacena las solicitudes de software de estudiantes';
