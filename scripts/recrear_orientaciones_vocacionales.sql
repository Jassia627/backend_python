-- Script para recrear la tabla orientaciones_vocacionales

DROP TABLE IF EXISTS orientaciones_vocacionales CASCADE;

CREATE TABLE IF NOT EXISTS orientaciones_vocacionales (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
   fecha_orientacion DATE NOT NULL,
   fecha_ingreso_programa DATE,
   area_interes VARCHAR(100),
   resultado TEXT,
   orientador VARCHAR(200),
   observaciones TEXT,
   riesgo_spadies VARCHAR(50),
   created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
   updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
