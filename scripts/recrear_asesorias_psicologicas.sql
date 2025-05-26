
-- Script para recrear la tabla asesorias_psicologicas
DROP TABLE IF EXISTS asesorias_psicologicas CASCADE;

CREATE TABLE IF NOT EXISTS asesorias_psicologicas (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
   motivo_consulta TEXT,
   motivo_intervencion TEXT,
   tipo_intervencion VARCHAR(100),
   fecha DATE NOT NULL,
   fecha_atencion DATE,
   psicologo VARCHAR(200),
   seguimiento TEXT,
   created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
   updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
    