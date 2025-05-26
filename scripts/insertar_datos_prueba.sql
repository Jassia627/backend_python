-- Script para insertar datos de prueba en la tabla permanencia

-- Primero, asegúrate de que la tabla existe
CREATE TABLE IF NOT EXISTS public.permanencia (
    id SERIAL PRIMARY KEY,
    servicio VARCHAR(255) NOT NULL,
    estrato INTEGER NOT NULL,
    inscritos INTEGER NOT NULL,
    estudiante_programa_academico VARCHAR(255) NOT NULL,
    riesgo_desercion VARCHAR(50) NOT NULL,
    tipo_vulnerabilidad VARCHAR(100) NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    semestre INTEGER NOT NULL,
    matriculados INTEGER NOT NULL DEFAULT 0,
    desertores INTEGER NOT NULL DEFAULT 0,
    graduados INTEGER NOT NULL DEFAULT 0,
    requiere_tutoria VARCHAR(5) NOT NULL,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Limpiar datos existentes (opcional)
-- TRUNCATE TABLE public.permanencia RESTART IDENTITY;

-- Insertar datos de prueba
INSERT INTO public.permanencia (
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
-- Programa 1: LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA
('POA', 1, 20, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Académica', '2023-1', 3, 1, 0, 0, 'Sí'),
('POVAU', 2, 15, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Medio', 'Social', '2023-1', 5, 1, 0, 0, 'No'),
('Comedor', 1, 25, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Alto', 'Económica', '2023-1', 2, 1, 0, 0, 'Sí'),
('POPS', 3, 10, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Psicológica', '2023-2', 4, 1, 0, 0, 'No'),
('Intervención Grupal', 2, 18, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Medio', 'Social', '2023-2', 6, 1, 0, 0, 'Sí'),

-- Programa 2: ENFERMERÍA
('POA', 2, 30, 'ENFERMERÍA', 'Medio', 'Académica', '2023-1', 1, 1, 0, 0, 'Sí'),
('POVAU', 1, 22, 'ENFERMERÍA', 'Bajo', 'Social', '2023-1', 3, 1, 0, 0, 'No'),
('Comedor', 3, 28, 'ENFERMERÍA', 'Alto', 'Económica', '2023-1', 5, 1, 0, 0, 'Sí'),
('POPS', 2, 15, 'ENFERMERÍA', 'Medio', 'Psicológica', '2023-2', 7, 1, 0, 0, 'No'),
('Atención Individual', 1, 20, 'ENFERMERÍA', 'Bajo', 'Social', '2023-2', 9, 1, 0, 0, 'Sí'),

-- Programa 3: CONTADURIA PUBLICA
('POA', 3, 25, 'CONTADURIA PUBLICA', 'Alto', 'Académica', '2023-1', 2, 1, 0, 0, 'Sí'),
('POVAU', 2, 18, 'CONTADURIA PUBLICA', 'Medio', 'Social', '2023-1', 4, 1, 0, 0, 'No'),
('Comedor', 1, 30, 'CONTADURIA PUBLICA', 'Bajo', 'Económica', '2023-1', 6, 1, 0, 0, 'Sí'),
('POPS', 3, 12, 'CONTADURIA PUBLICA', 'Alto', 'Psicológica', '2023-2', 8, 1, 0, 0, 'No'),
('Intervención Grupal', 2, 22, 'CONTADURIA PUBLICA', 'Medio', 'Social', '2023-2', 10, 1, 0, 0, 'Sí'),

-- Programa 4: MUSICA
('POA', 1, 15, 'MUSICA', 'Bajo', 'Académica', '2023-1', 1, 1, 0, 0, 'Sí'),
('POVAU', 3, 10, 'MUSICA', 'Alto', 'Social', '2023-1', 3, 1, 0, 0, 'No'),
('Comedor', 2, 18, 'MUSICA', 'Medio', 'Económica', '2023-1', 5, 1, 0, 0, 'Sí'),
('POPS', 1, 8, 'MUSICA', 'Bajo', 'Psicológica', '2023-2', 7, 1, 0, 0, 'No'),
('Atención Individual', 3, 12, 'MUSICA', 'Alto', 'Social', '2023-2', 9, 1, 0, 0, 'Sí'),

-- Programa 5: INGENIERÍA AGROINDUSTRIAL
('POA', 2, 20, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Académica', '2023-1', 2, 1, 0, 0, 'Sí'),
('POVAU', 1, 15, 'INGENIERÍA AGROINDUSTRIAL', 'Bajo', 'Social', '2023-1', 4, 1, 0, 0, 'No'),
('Comedor', 3, 25, 'INGENIERÍA AGROINDUSTRIAL', 'Alto', 'Económica', '2023-1', 6, 1, 0, 0, 'Sí'),
('POPS', 2, 10, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Psicológica', '2023-2', 8, 1, 0, 0, 'No'),
('Intervención Grupal', 1, 18, 'INGENIERÍA AGROINDUSTRIAL', 'Bajo', 'Social', '2023-2', 10, 1, 0, 0, 'Sí');

-- Añadir algunos registros con desertores y graduados
INSERT INTO public.permanencia (
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
-- Desertores
('POA', 1, 5, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Alto', 'Económica', '2022-1', 3, 0, 1, 0, 'Sí'),
('POVAU', 2, 3, 'ENFERMERÍA', 'Alto', 'Social', '2022-1', 5, 0, 1, 0, 'Sí'),
('Comedor', 1, 4, 'CONTADURIA PUBLICA', 'Alto', 'Académica', '2022-1', 2, 0, 1, 0, 'Sí'),
('POPS', 3, 2, 'MUSICA', 'Alto', 'Psicológica', '2022-2', 4, 0, 1, 0, 'Sí'),
('Intervención Grupal', 2, 3, 'INGENIERÍA AGROINDUSTRIAL', 'Alto', 'Económica', '2022-2', 6, 0, 1, 0, 'Sí'),

-- Graduados
('POA', 2, 8, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Académica', '2021-1', 10, 1, 0, 1, 'No'),
('POVAU', 1, 6, 'ENFERMERÍA', 'Bajo', 'Social', '2021-1', 10, 1, 0, 1, 'No'),
('Comedor', 3, 7, 'CONTADURIA PUBLICA', 'Bajo', 'Económica', '2021-1', 10, 1, 0, 1, 'No'),
('POPS', 2, 5, 'MUSICA', 'Bajo', 'Psicológica', '2021-2', 10, 1, 0, 1, 'No'),
('Atención Individual', 1, 6, 'INGENIERÍA AGROINDUSTRIAL', 'Bajo', 'Social', '2021-2', 10, 1, 0, 1, 'No');
