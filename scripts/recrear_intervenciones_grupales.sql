-- Script para recrear la tabla intervenciones_grupales con todos los campos necesarios
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS intervenciones_grupales CASCADE;

-- Creamos la tabla con todas las columnas necesarias según el frontend
CREATE TABLE public.intervenciones_grupales (
    id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(),
    estudiante_id uuid REFERENCES estudiantes(id) ON DELETE SET NULL,
    fecha_solicitud DATE NOT NULL,
    nombre_docente_permanencia VARCHAR(200) NOT NULL,
    celular_permanencia VARCHAR(20) NOT NULL,
    correo_permanencia VARCHAR(100) NOT NULL,
    estudiante_programa_academico_permanencia VARCHAR(200) NOT NULL,
    tipo_poblacion VARCHAR(100) NOT NULL,
    nombre_docente_asignatura VARCHAR(200) NOT NULL,
    celular_docente_asignatura VARCHAR(20) NOT NULL,
    correo_docente_asignatura VARCHAR(100) NOT NULL,
    estudiante_programa_academico_docente_asignatura VARCHAR(200) NOT NULL,
    asignatura_intervenir VARCHAR(200) NOT NULL,
    grupo VARCHAR(20) NOT NULL,
    semestre VARCHAR(20) NOT NULL,
    numero_estudiantes VARCHAR(20) NOT NULL,
    tematica_sugerida TEXT,
    fecha_estudiante_programa_academicoda DATE NOT NULL,
    hora TIME NOT NULL,
    aula VARCHAR(50) NOT NULL,
    bloque VARCHAR(50) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    motivo TEXT,
    efectividad VARCHAR(50) DEFAULT 'Pendiente evaluación',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT intervenciones_grupales_pkey PRIMARY KEY (id)
);

-- Creamos índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_intervenciones_grupales_estudiante_id ON intervenciones_grupales(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_intervenciones_grupales_fecha ON intervenciones_grupales(fecha_solicitud);
CREATE INDEX IF NOT EXISTS idx_intervenciones_grupales_estado ON intervenciones_grupales(estado);
