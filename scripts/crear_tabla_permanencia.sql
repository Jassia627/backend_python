-- Script para crear la tabla permanencia en Supabase

CREATE TABLE public.permanencia (
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

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX idx_permanencia_servicio ON public.permanencia(servicio);
CREATE INDEX idx_permanencia_estrato ON public.permanencia(estrato);
CREATE INDEX idx_permanencia_programa ON public.permanencia(estudiante_programa_academico);
CREATE INDEX idx_permanencia_riesgo ON public.permanencia(riesgo_desercion);
CREATE INDEX idx_permanencia_periodo ON public.permanencia(periodo);

-- Comentarios para la tabla y columnas
COMMENT ON TABLE public.permanencia IS 'Tabla que almacena los datos de permanencia estudiantil';
COMMENT ON COLUMN public.permanencia.id IS 'Identificador único del registro';
COMMENT ON COLUMN public.permanencia.servicio IS 'Servicio de permanencia utilizado (POA, POVAU, Comedor, etc.)';
COMMENT ON COLUMN public.permanencia.estrato IS 'Estrato socioeconómico del estudiante (1-6)';
COMMENT ON COLUMN public.permanencia.inscritos IS 'Cantidad de estudiantes inscritos';
COMMENT ON COLUMN public.permanencia.estudiante_programa_academico IS 'Programa académico al que pertenece el estudiante';
COMMENT ON COLUMN public.permanencia.riesgo_desercion IS 'Nivel de riesgo de deserción (Muy bajo, Bajo, Medio, Alto, Muy Alto)';
COMMENT ON COLUMN public.permanencia.tipo_vulnerabilidad IS 'Tipo de vulnerabilidad (Académica, Social, Psicológica, Económica)';
COMMENT ON COLUMN public.permanencia.periodo IS 'Periodo académico en formato YYYY-S';
COMMENT ON COLUMN public.permanencia.semestre IS 'Semestre que cursa el estudiante (1-10)';
COMMENT ON COLUMN public.permanencia.matriculados IS 'Indica si el estudiante está matriculado (0=No, 1=Sí)';
COMMENT ON COLUMN public.permanencia.desertores IS 'Indica si el estudiante ha desertado (0=No, 1=Sí)';
COMMENT ON COLUMN public.permanencia.graduados IS 'Indica si el estudiante se ha graduado (0=No, 1=Sí)';
COMMENT ON COLUMN public.permanencia.requiere_tutoria IS 'Indica si el estudiante requiere tutoría (Sí/No)';
COMMENT ON COLUMN public.permanencia.fecha_registro IS 'Fecha y hora de registro del dato';

-- Permisos (ajustar según las necesidades)
ALTER TABLE public.permanencia ENABLE ROW LEVEL SECURITY;

-- Política para permitir lectura a todos los usuarios autenticados
CREATE POLICY "Permitir lectura a usuarios autenticados" 
    ON public.permanencia FOR SELECT 
    USING (auth.role() = 'authenticated');

-- Política para permitir inserción a usuarios autenticados
CREATE POLICY "Permitir inserción a usuarios autenticados" 
    ON public.permanencia FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

-- Política para permitir actualización a usuarios autenticados
CREATE POLICY "Permitir actualización a usuarios autenticados" 
    ON public.permanencia FOR UPDATE 
    USING (auth.role() = 'authenticated');

-- Ejemplo de datos de muestra (opcional)
INSERT INTO public.permanencia (servicio, estrato, inscritos, estudiante_programa_academico, riesgo_desercion, tipo_vulnerabilidad, periodo, semestre, matriculados, desertores, graduados, requiere_tutoria)
VALUES
    ('POA', 1, 10, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Bajo', 'Académica', '2023-1', 3, 1, 0, 0, 'Sí'),
    ('POVAU', 2, 8, 'ENFERMERÍA', 'Medio', 'Social', '2023-1', 5, 1, 0, 0, 'No'),
    ('Comedor', 1, 15, 'CONTADURIA PUBLICA', 'Alto', 'Económica', '2023-1', 2, 1, 0, 0, 'Sí'),
    ('POPS', 3, 5, 'MUSICA', 'Bajo', 'Psicológica', '2023-1', 4, 1, 0, 0, 'No'),
    ('Intervención Grupal', 2, 12, 'INGENIERÍA AGROINDUSTRIAL', 'Medio', 'Social', '2023-1', 6, 1, 0, 0, 'Sí'),
    ('Atención Individual', 1, 7, 'LICENCIATURA EN ESPAÑOL E INGLÉS', 'Alto', 'Académica', '2023-1', 1, 1, 0, 0, 'Sí'),
    ('POA', 2, 9, 'RECREACIÓN Y DEPORTES', 'Bajo', 'Económica', '2023-1', 7, 1, 0, 0, 'No'),
    ('POVAU', 3, 6, 'LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA', 'Medio', 'Psicológica', '2023-1', 8, 1, 0, 0, 'Sí'),
    ('Comedor', 1, 14, 'ENFERMERÍA', 'Alto', 'Social', '2023-1', 2, 1, 0, 0, 'Sí'),
    ('POPS', 2, 8, 'CONTADURIA PUBLICA', 'Bajo', 'Académica', '2023-1', 3, 1, 0, 0, 'No');
