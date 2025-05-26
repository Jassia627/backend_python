-- Script para recrear las tablas de permanencia estudiantil
-- Primero eliminamos las tablas existentes si existen

-- Eliminar tablas secundarias primero para evitar problemas con las claves foráneas
DROP TABLE IF EXISTS permanencia CASCADE;
DROP TABLE IF EXISTS povau CASCADE;
DROP TABLE IF EXISTS poa CASCADE;
DROP TABLE IF EXISTS comedores_universitarios CASCADE;
DROP TABLE IF EXISTS registro_beneficios CASCADE;
DROP TABLE IF EXISTS solicitudes_atencion CASCADE;
DROP TABLE IF EXISTS intervenciones_grupales CASCADE;
DROP TABLE IF EXISTS remisiones_psicologicas CASCADE;
DROP TABLE IF EXISTS asesorias_psicologicas CASCADE;
DROP TABLE IF EXISTS orientaciones_vocacionales CASCADE;
DROP TABLE IF EXISTS apoyos_socioeconomicos CASCADE;
DROP TABLE IF EXISTS talleres_habilidades CASCADE;
DROP TABLE IF EXISTS seguimientos_academicos CASCADE;
DROP TABLE IF EXISTS formatos_asistencia CASCADE;
DROP TABLE IF EXISTS asistencias CASCADE;
DROP TABLE IF EXISTS tutorias_academicas CASCADE;
DROP TABLE IF EXISTS programas CASCADE;

-- Ahora creamos las tablas con las relaciones correctas

-- Tabla POVAU (Programa de Orientación Vocacional y Adaptación a la Universidad)
CREATE TABLE IF NOT EXISTS povau (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    tipo_participante VARCHAR(100) NOT NULL,
    fecha_ingreso DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla POA (Plan Operativo Anual)
CREATE TABLE IF NOT EXISTS poa (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    ciclo_formacion VARCHAR(100) NOT NULL,
    nombre_asignatura VARCHAR(200),
    fecha DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Comedor Universitario
CREATE TABLE IF NOT EXISTS comedores_universitarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    condicion_socioeconomica VARCHAR(50) NOT NULL,
    fecha_solicitud DATE,
    aprobado BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Registro de Beneficios
CREATE TABLE IF NOT EXISTS registro_beneficios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_inscripcion DATE NOT NULL,
    estado_solicitud BOOLEAN DEFAULT FALSE,
    periodo_academico VARCHAR(20),
    fecha_inicio DATE,
    fecha_finalizacion DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Solicitudes de Atención Individual
CREATE TABLE IF NOT EXISTS solicitudes_atencion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_atencion DATE NOT NULL,
    motivo_atencion VARCHAR(100) DEFAULT 'general',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Intervenciones Grupales
CREATE TABLE IF NOT EXISTS intervenciones_grupales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_solicitud DATE NOT NULL,
    fecha_recepcion DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Remisiones Psicológicas
CREATE TABLE IF NOT EXISTS remisiones_psicologicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_remision DATE NOT NULL,
    tipo_remision VARCHAR(100) DEFAULT 'general',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Asesorías Psicológicas
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

-- Tabla Orientaciones Vocacionales
CREATE TABLE IF NOT EXISTS orientaciones_vocacionales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_orientacion DATE NOT NULL,
    fecha_ingreso_programa DATE,
    area_interes VARCHAR(100),
    resultado TEXT,
    orientador VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Apoyos Socioeconómicos
CREATE TABLE IF NOT EXISTS apoyos_socioeconomicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    tipo_apoyo VARCHAR(100) NOT NULL,
    monto DECIMAL(10, 2),
    fecha_otorgamiento DATE NOT NULL,
    fecha_finalizacion DATE,
    estado VARCHAR(50) DEFAULT 'activo',
    tipo_vulnerabilidad VARCHAR(100),
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Talleres de Habilidades
CREATE TABLE IF NOT EXISTS talleres_habilidades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    nombre_taller VARCHAR(200) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    fecha_taller DATE,
    horas_completadas INTEGER DEFAULT 0,
    certificado BOOLEAN DEFAULT FALSE,
    facilitador VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Seguimientos Académicos
CREATE TABLE IF NOT EXISTS seguimientos_academicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_seguimiento DATE NOT NULL,
    periodo_academico VARCHAR(20),
    promedio_actual DECIMAL(3, 2),
    materias_perdidas INTEGER DEFAULT 0,
    materias_cursadas INTEGER DEFAULT 0,
    observaciones TEXT,
    requiere_tutoria BOOLEAN DEFAULT FALSE,
    estado_participacion VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Formatos de Asistencia
CREATE TABLE IF NOT EXISTS formatos_asistencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    numero_asistencia INTEGER DEFAULT 1,
    fecha DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Asistencias
CREATE TABLE IF NOT EXISTS asistencias (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    actividad VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    asistio BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Programas Académicos
CREATE TABLE IF NOT EXISTS programas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    facultad VARCHAR(100) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    modalidad VARCHAR(50),
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Tutorías Académicas
CREATE TABLE IF NOT EXISTS tutorias_academicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    asignatura VARCHAR(100),
    fecha_tutoria DATE,
    fecha_asignacion DATE,
    hora_inicio TIME,
    hora_fin TIME,
    tutor VARCHAR(200),
    acciones_apoyo TEXT,
    nivel_riesgo VARCHAR(50),
    requiere_tutoria BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla Permanencia (para estadísticas)
CREATE TABLE IF NOT EXISTS permanencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    servicio VARCHAR(100) NOT NULL,
    estrato INTEGER,
    inscritos INTEGER DEFAULT 0,
    estudiante_programa_academico VARCHAR(200),
    riesgo_desercion VARCHAR(50),
    tipo_vulnerabilidad VARCHAR(100),
    periodo VARCHAR(20),
    semestre INTEGER,
    matriculados INTEGER DEFAULT 0,
    desertores INTEGER DEFAULT 0,
    graduados INTEGER DEFAULT 0,
    requiere_tutoria VARCHAR(2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_povau_estudiante_id ON povau(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_poa_estudiante_id ON poa(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_comedor_estudiante_id ON comedores_universitarios(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_beneficios_estudiante_id ON registro_beneficios(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_atencion_estudiante_id ON solicitudes_atencion(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_intervenciones_estudiante_id ON intervenciones_grupales(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_remisiones_estudiante_id ON remisiones_psicologicas(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_asesorias_estudiante_id ON asesorias_psicologicas(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_orientaciones_estudiante_id ON orientaciones_vocacionales(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_apoyos_estudiante_id ON apoyos_socioeconomicos(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_talleres_estudiante_id ON talleres_habilidades(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_seguimientos_estudiante_id ON seguimientos_academicos(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_estudiante_id ON formatos_asistencia(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_estudiante_id ON asistencias(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_tutorias_estudiante_id ON tutorias_academicas(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_programas_codigo ON programas(codigo);
CREATE INDEX IF NOT EXISTS idx_programas_facultad ON programas(facultad);
CREATE INDEX IF NOT EXISTS idx_permanencia_servicio ON permanencia(servicio);
CREATE INDEX IF NOT EXISTS idx_permanencia_programa ON permanencia(estudiante_programa_academico);
