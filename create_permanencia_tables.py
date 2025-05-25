from config import supabase
import time

def crear_tablas_permanencia():
    """
    Crea las tablas necesarias para los servicios de permanencia en Supabase.
    """
    print("Conectando a Supabase...")
    
    try:
        # Script SQL para crear todas las tablas de servicios de permanencia
        sql = """
        -- Tabla para Tutorías Académicas (POA)
        CREATE TABLE IF NOT EXISTS tutorias_academicas (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            nivel_riesgo TEXT NOT NULL,
            requiere_tutoria BOOLEAN DEFAULT FALSE,
            fecha_asignacion TEXT NOT NULL,
            acciones_apoyo TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Asesorías Psicológicas (POPS)
        CREATE TABLE IF NOT EXISTS asesorias_psicologicas (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            motivo_intervencion TEXT NOT NULL,
            tipo_intervencion TEXT NOT NULL,
            fecha_atencion TEXT NOT NULL,
            seguimiento TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Orientaciones Vocacionales (POVAU)
        CREATE TABLE IF NOT EXISTS orientaciones_vocacionales (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            tipo_participante TEXT NOT NULL,
            riesgo_spadies TEXT NOT NULL,
            fecha_ingreso_programa TEXT NOT NULL,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Comedor Universitario
        CREATE TABLE IF NOT EXISTS comedores_universitarios (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            condicion_socioeconomica TEXT NOT NULL,
            fecha_solicitud TEXT NOT NULL,
            aprobado BOOLEAN DEFAULT FALSE,
            tipo_comida TEXT NOT NULL,
            raciones_asignadas INTEGER NOT NULL,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Apoyos Socioeconómicos
        CREATE TABLE IF NOT EXISTS apoyos_socioeconomicos (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            tipo_vulnerabilidad TEXT,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Talleres de Habilidades
        CREATE TABLE IF NOT EXISTS talleres_habilidades (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            nombre_taller TEXT NOT NULL,
            fecha_taller TEXT NOT NULL,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Tabla para Seguimientos Académicos
        CREATE TABLE IF NOT EXISTS seguimientos_academicos (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            estado_participacion TEXT NOT NULL,
            observaciones_permanencia TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Ejecutar el SQL
        print("Creando tablas de servicios de permanencia...")
        supabase.rpc('exec_sql', {'query': sql}).execute()
        
        print("Tablas de servicios de permanencia creadas exitosamente.")
        print("\nEstructura de las tablas creadas:")
        print("1. tutorias_academicas - Registro de tutorías académicas (POA)")
        print("2. asesorias_psicologicas - Registro de asesorías psicológicas (POPS)")
        print("3. orientaciones_vocacionales - Registro de orientaciones vocacionales (POVAU)")
        print("4. comedores_universitarios - Registro de comedor universitario")
        print("5. apoyos_socioeconomicos - Registro de apoyos socioeconómicos")
        print("6. talleres_habilidades - Registro de talleres de habilidades")
        print("7. seguimientos_academicos - Registro de seguimientos académicos")
        
    except Exception as e:
        print(f"Error al crear tablas de servicios de permanencia: {e}")
        print("\nSQL para crear las tablas manualmente en la consola de Supabase:")
        print(sql)

if __name__ == "__main__":
    crear_tablas_permanencia()
