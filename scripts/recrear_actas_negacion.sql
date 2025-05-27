-- Script para recrear la tabla actas_negacion
DROP TABLE IF EXISTS actas_negacion CASCADE;

CREATE TABLE public.actas_negacion (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid,
    nombre_estudiante VARCHAR(100) NOT NULL,
    documento_tipo VARCHAR(50) NOT NULL,
    documento_numero VARCHAR(50) NOT NULL,
    documento_expedido_en VARCHAR(100) NOT NULL,
    estudiante_programa_academico VARCHAR(100) NOT NULL,
    semestre VARCHAR(10) NOT NULL,
    fecha_firma_dia VARCHAR(10) NOT NULL, -- Cambiado a 10 para acomodar valores como '050'
    fecha_firma_mes VARCHAR(10) NOT NULL,
    fecha_firma_anio VARCHAR(10) NOT NULL,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_completa VARCHAR(50), -- Campo adicional para la fecha completa en formato ISO
    fecha_legible VARCHAR(50), -- Campo adicional para la fecha en formato legible
    firma_estudiante VARCHAR(100) NOT NULL,
    documento_firma_estudiante VARCHAR(50) NOT NULL,
    docente_permanencia VARCHAR(100) NOT NULL,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT actas_negacion_pkey PRIMARY KEY (id)
);

-- Creamos un índice para búsquedas por estudiante_id
CREATE INDEX IF NOT EXISTS idx_actas_negacion_estudiante_id ON public.actas_negacion USING btree (estudiante_id);

-- Agregamos la restricción de clave foránea, pero permitimos NULL para estudiante_id
ALTER TABLE public.actas_negacion 
ADD CONSTRAINT actas_negacion_estudiante_id_fkey 
FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE SET NULL;

-- Comentario explicativo
COMMENT ON TABLE public.actas_negacion IS 'Tabla que almacena las actas de negación de servicios por parte de estudiantes';
