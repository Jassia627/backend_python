from config import supabase
import time

def recreate_asistencias_actividades_table():
    """
    Elimina la tabla asistencias_actividades existente y crea una nueva con la estructura correcta.
    """
    print("Conectando a Supabase...")
    
    try:
        # 1. Eliminar la tabla existente
        print("Eliminando tabla asistencias_actividades existente...")
        supabase.table("asistencias_actividades").delete().execute()
        
        # Esperar un momento para asegurar que la operación se complete
        time.sleep(2)
        
        # 2. Ejecutar SQL para crear la tabla con la estructura correcta
        print("Creando nueva tabla asistencias_actividades...")
        sql = """
        CREATE TABLE IF NOT EXISTS asistencias_actividades (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            nombre_estudiante TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            estudiante_programa_academico TEXT NOT NULL,
            estudiante_programa_academico_academico TEXT,
            semestre TEXT NOT NULL,
            nombre_actividad TEXT NOT NULL,
            modalidad TEXT NOT NULL,
            tipo_actividad TEXT NOT NULL,
            fecha_actividad TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            modalidad_registro TEXT NOT NULL,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Ejecutar el SQL
        supabase.rpc('exec_sql', {'query': sql}).execute()
        
        print("Tabla asistencias_actividades recreada exitosamente.")
        print("\nEstructura de la tabla asistencias_actividades:")
        print("- id: UUID (Primary Key)")
        print("- estudiante_id: UUID (Foreign Key, OPCIONAL)")
        print("- nombre_estudiante: TEXT (NOT NULL)")
        print("- numero_documento: TEXT (NOT NULL)")
        print("- estudiante_programa_academico: TEXT (NOT NULL)")
        print("- estudiante_programa_academico_academico: TEXT (OPCIONAL)")
        print("- semestre: TEXT (NOT NULL)")
        print("- nombre_actividad: TEXT (NOT NULL)")
        print("- modalidad: TEXT (NOT NULL)")
        print("- tipo_actividad: TEXT (NOT NULL)")
        print("- fecha_actividad: TEXT (NOT NULL)")
        print("- hora_inicio: TEXT (NOT NULL)")
        print("- hora_fin: TEXT (NOT NULL)")
        print("- modalidad_registro: TEXT (NOT NULL)")
        print("- observaciones: TEXT (OPCIONAL)")
        print("- created_at: TIMESTAMP WITH TIME ZONE")
        print("- updated_at: TIMESTAMP WITH TIME ZONE")
        
    except Exception as e:
        print(f"Error al recrear la tabla asistencias_actividades: {e}")
        
        # Intentar crear la tabla desde cero si hubo un error al eliminarla
        try:
            print("\nIntentando crear la tabla desde cero...")
            sql = """
            DROP TABLE IF EXISTS asistencias_actividades;
            
            CREATE TABLE asistencias_actividades (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                estudiante_id UUID REFERENCES estudiantes(id),
                nombre_estudiante TEXT NOT NULL,
                numero_documento TEXT NOT NULL,
                estudiante_programa_academico TEXT NOT NULL,
                estudiante_programa_academico_academico TEXT,
                semestre TEXT NOT NULL,
                nombre_actividad TEXT NOT NULL,
                modalidad TEXT NOT NULL,
                tipo_actividad TEXT NOT NULL,
                fecha_actividad TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                modalidad_registro TEXT NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Ejecutar el SQL
            supabase.rpc('exec_sql', {'query': sql}).execute()
            print("Tabla asistencias_actividades creada exitosamente.")
            
        except Exception as e2:
            print(f"Error al crear la tabla desde cero: {e2}")
            print("\nSQL para crear la tabla manualmente en la consola de Supabase:")
            print("""
DROP TABLE IF EXISTS asistencias_actividades;

CREATE TABLE asistencias_actividades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID REFERENCES estudiantes(id),
    nombre_estudiante TEXT NOT NULL,
    numero_documento TEXT NOT NULL,
    estudiante_programa_academico TEXT NOT NULL,
    estudiante_programa_academico_academico TEXT,
    semestre TEXT NOT NULL,
    nombre_actividad TEXT NOT NULL,
    modalidad TEXT NOT NULL,
    tipo_actividad TEXT NOT NULL,
    fecha_actividad TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    modalidad_registro TEXT NOT NULL,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
            """)

if __name__ == "__main__":
    recreate_asistencias_actividades_table()
