-- Script para eliminar y recrear la tabla permanencia
-- Primero eliminamos la tabla si existe
DROP TABLE IF EXISTS permanencia;

-- Creamos la tabla con los campos necesarios
CREATE TABLE permanencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    servicio TEXT,
    estrato INTEGER,
    inscritos INTEGER DEFAULT 0,
    estudiante_programa_academico TEXT,
    riesgo_desercion TEXT,
    tipo_vulnerabilidad TEXT,
    periodo TEXT,
    semestre INTEGER,
    matriculados INTEGER DEFAULT 0,
    desertores INTEGER DEFAULT 0,
    graduados INTEGER DEFAULT 0,
    requiere_tutoria TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comentarios sobre la tabla
COMMENT ON TABLE permanencia IS 'Tabla que almacena información sobre la permanencia de estudiantes';
COMMENT ON COLUMN permanencia.servicio IS 'Servicio de permanencia (POA, POVAU, Comedor, etc.)';
COMMENT ON COLUMN permanencia.estrato IS 'Estrato socioeconómico del estudiante (1-6)';
COMMENT ON COLUMN permanencia.inscritos IS 'Cantidad de estudiantes inscritos';
COMMENT ON COLUMN permanencia.estudiante_programa_academico IS 'Programa académico del estudiante';
COMMENT ON COLUMN permanencia.riesgo_desercion IS 'Nivel de riesgo de deserción (Muy bajo, Bajo, Medio, Alto, Muy Alto)';
COMMENT ON COLUMN permanencia.tipo_vulnerabilidad IS 'Tipo de vulnerabilidad (Académica, Social, Psicológica, Económica)';
COMMENT ON COLUMN permanencia.periodo IS 'Periodo académico (ej. 2023-1)';
COMMENT ON COLUMN permanencia.semestre IS 'Semestre del estudiante';
COMMENT ON COLUMN permanencia.matriculados IS 'Indica si el estudiante está matriculado (0 o 1)';
COMMENT ON COLUMN permanencia.desertores IS 'Indica si el estudiante ha desertado (0 o 1)';
COMMENT ON COLUMN permanencia.graduados IS 'Indica si el estudiante se ha graduado (0 o 1)';
COMMENT ON COLUMN permanencia.requiere_tutoria IS 'Indica si el estudiante requiere tutoría (Sí o No)';

-- Datos de ejemplo para probar la aplicación
INSERT INTO permanencia (
    servicio, 
    estrato, 
    inscritos, 
    estudiante_programa_academico, 
    riesgo_desercion, 
    tipo_vulnerabilidad, 
    periodo, 
    semestre, 
    matriculados, 
    desertores, 
    graduados, 
    requiere_tutoria
) VALUES 
-- POA - Programa de Orientación Académica
('POA', 1, 15, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Alto', 'Académica', '2023-1', 3, 1, 0, 0, 'Sí'),
('POA', 2, 12, 'ENFERMERÍA', 'Medio', 'Social', '2023-1', 5, 1, 0, 0, 'Sí'),
('POA', 3, 8, 'CONTADURIA PUBLICA', 'Bajo', 'Económica', '2023-1', 7, 1, 0, 0, 'No'),
('POA', 4, 5, 'MUSICA', 'Muy bajo', 'Social', '2023-1', 2, 1, 0, 0, 'No'),
('POA', 5, 3, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Académica', '2023-1', 4, 1, 0, 0, 'Sí'),
('POA', 6, 2, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Alto', 'Psicológica', '2023-1', 6, 1, 0, 0, 'Sí'),

-- POVAU - Programa de Orientación Vocacional y Adaptación a la Vida Universitaria
('POVAU', 1, 18, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Medio', 'Social', '2023-1', 1, 1, 0, 0, 'Sí'),
('POVAU', 2, 14, 'ENFERMERÍA', 'Bajo', 'Académica', '2023-1', 1, 1, 0, 0, 'No'),
('POVAU', 3, 10, 'CONTADURIA PUBLICA', 'Muy bajo', 'Económica', '2023-1', 1, 1, 0, 0, 'No'),
('POVAU', 4, 6, 'MUSICA', 'Bajo', 'Psicológica', '2023-1', 1, 1, 0, 0, 'Sí'),
('POVAU', 5, 4, 'RECREACIÓN Y DEPORTES', 'Medio', 'Social', '2023-1', 1, 1, 0, 0, 'Sí'),
('POVAU', 6, 2, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Alto', 'Académica', '2023-1', 1, 1, 0, 0, 'Sí'),

-- Comedor
('Comedor', 1, 20, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Económica', '2023-1', 4, 1, 0, 0, 'No'),
('Comedor', 2, 15, 'ENFERMERÍA', 'Muy bajo', 'Económica', '2023-1', 3, 1, 0, 0, 'No'),
('Comedor', 3, 10, 'CONTADURIA PUBLICA', 'Medio', 'Económica', '2023-1', 5, 1, 0, 0, 'Sí'),
('Comedor', 4, 5, 'MUSICA', 'Alto', 'Económica', '2023-1', 2, 1, 0, 0, 'Sí'),
('Comedor', 5, 3, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Económica', '2023-1', 6, 1, 0, 0, 'No'),
('Comedor', 6, 1, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Bajo', 'Económica', '2023-1', 8, 1, 0, 0, 'No'),

-- POPS - Programa de Orientación Psicosocial
('POPS', 1, 12, 'RECREACIÓN Y DEPORTES', 'Alto', 'Psicológica', '2023-1', 3, 1, 0, 0, 'Sí'),
('POPS', 2, 10, 'ENFERMERÍA', 'Medio', 'Psicológica', '2023-1', 5, 1, 0, 0, 'Sí'),
('POPS', 3, 7, 'CONTADURIA PUBLICA', 'Bajo', 'Psicológica', '2023-1', 2, 1, 0, 0, 'No'),
('POPS', 4, 4, 'MUSICA', 'Muy bajo', 'Psicológica', '2023-1', 4, 1, 0, 0, 'No'),
('POPS', 5, 2, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Psicológica', '2023-1', 6, 1, 0, 0, 'Sí'),
('POPS', 6, 1, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Alto', 'Psicológica', '2023-1', 7, 1, 0, 0, 'Sí'),

-- Intervención Grupal
('Intervención Grupal', 1, 10, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Medio', 'Social', '2023-1', 2, 1, 0, 0, 'Sí'),
('Intervención Grupal', 2, 8, 'ENFERMERÍA', 'Bajo', 'Académica', '2023-1', 4, 1, 0, 0, 'No'),
('Intervención Grupal', 3, 6, 'CONTADURIA PUBLICA', 'Alto', 'Psicológica', '2023-1', 6, 1, 0, 0, 'Sí'),
('Intervención Grupal', 4, 4, 'MUSICA', 'Muy bajo', 'Económica', '2023-1', 3, 1, 0, 0, 'No'),
('Intervención Grupal', 5, 2, 'INGENIERÍA AGROINDUSTRIAL', 'Bajo', 'Social', '2023-1', 5, 1, 0, 0, 'No'),
('Intervención Grupal', 6, 1, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Medio', 'Académica', '2023-1', 7, 1, 0, 0, 'Sí'),

-- Atención Individual
('Atención Individual', 1, 8, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Alto', 'Psicológica', '2023-1', 3, 1, 0, 0, 'Sí'),
('Atención Individual', 2, 7, 'ENFERMERÍA', 'Medio', 'Social', '2023-1', 5, 1, 0, 0, 'Sí'),
('Atención Individual', 3, 5, 'CONTADURIA PUBLICA', 'Bajo', 'Académica', '2023-1', 2, 1, 0, 0, 'No'),
('Atención Individual', 4, 3, 'MUSICA', 'Muy bajo', 'Económica', '2023-1', 4, 1, 0, 0, 'No'),
('Atención Individual', 5, 2, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Psicológica', '2023-1', 6, 1, 0, 0, 'Sí'),
('Atención Individual', 6, 1, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Alto', 'Social', '2023-1', 7, 1, 0, 0, 'Sí');

-- Agregar algunos registros con desertores
INSERT INTO permanencia (
    servicio, 
    estrato, 
    inscritos, 
    estudiante_programa_academico, 
    riesgo_desercion, 
    tipo_vulnerabilidad, 
    periodo, 
    semestre, 
    matriculados, 
    desertores, 
    graduados, 
    requiere_tutoria
) VALUES 
('POA', 1, 5, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Muy Alto', 'Académica', '2022-2', 2, 0, 1, 0, 'Sí'),
('POVAU', 2, 3, 'ENFERMERÍA', 'Alto', 'Económica', '2022-2', 1, 0, 1, 0, 'Sí'),
('Comedor', 1, 4, 'CONTADURIA PUBLICA', 'Alto', 'Económica', '2022-2', 3, 0, 1, 0, 'Sí'),
('POPS', 3, 2, 'MUSICA', 'Muy Alto', 'Psicológica', '2022-2', 2, 0, 1, 0, 'Sí'),
('Intervención Grupal', 2, 3, 'INGENIERÍA AGROINDUSTRIAL', 'Alto', 'Social', '2022-2', 4, 0, 1, 0, 'Sí'),
('Atención Individual', 1, 2, 'RECREACIÓN Y DEPORTES', 'Muy Alto', 'Académica', '2022-2', 3, 0, 1, 0, 'Sí');

-- Agregar algunos registros con graduados
INSERT INTO permanencia (
    servicio, 
    estrato, 
    inscritos, 
    estudiante_programa_academico, 
    riesgo_desercion, 
    tipo_vulnerabilidad, 
    periodo, 
    semestre, 
    matriculados, 
    desertores, 
    graduados, 
    requiere_tutoria
) VALUES 
('POA', 3, 2, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Académica', '2022-1', 10, 0, 0, 1, 'No'),
('POVAU', 2, 3, 'ENFERMERÍA', 'Muy bajo', 'Social', '2022-1', 10, 0, 0, 1, 'No'),
('Comedor', 1, 1, 'CONTADURIA PUBLICA', 'Bajo', 'Económica', '2022-1', 10, 0, 0, 1, 'No'),
('POPS', 4, 2, 'MUSICA', 'Muy bajo', 'Psicológica', '2022-1', 10, 0, 0, 1, 'No');
