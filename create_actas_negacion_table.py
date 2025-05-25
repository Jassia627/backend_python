from config import supabase
import time

def recreate_actas_negacion_table():
    """
    Elimina la tabla actas_negacion existente y crea una nueva con la estructura correcta.
    """
    print("Conectando a Supabase...")
    
    try:
        # 1. Eliminar la tabla existente
        print("Eliminando tabla actas_negacion existente...")
        supabase.table("actas_negacion").delete().execute()
        
        # Esperar un momento para asegurar que la operación se complete
        time.sleep(2)
        
        # 2. Ejecutar SQL para crear la tabla con la estructura correcta
        print("Creando nueva tabla actas_negacion...")
        sql = """
        CREATE TABLE IF NOT EXISTS actas_negacion (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            estudiante_id UUID REFERENCES estudiantes(id),
            nombre_estudiante TEXT NOT NULL,
            documento_tipo TEXT NOT NULL,
            documento_numero TEXT NOT NULL,
            documento_expedido_en TEXT NOT NULL,
            estudiante_programa_academico TEXT NOT NULL,
            semestre TEXT NOT NULL,
            fecha_firma_dia TEXT NOT NULL,
            fecha_firma_mes TEXT NOT NULL,
            fecha_firma_anio TEXT NOT NULL,
            firma_estudiante TEXT NOT NULL,
            documento_firma_estudiante TEXT NOT NULL,
            docente_permanencia TEXT NOT NULL,
            observaciones TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Ejecutar el SQL
        supabase.rpc('exec_sql', {'query': sql}).execute()
        
        print("Tabla actas_negacion recreada exitosamente.")
        print("\nEstructura de la tabla actas_negacion:")
        print("- id: UUID (Primary Key)")
        print("- estudiante_id: UUID (Foreign Key, OPCIONAL)")
        print("- nombre_estudiante: TEXT (NOT NULL)")
        print("- documento_tipo: TEXT (NOT NULL)")
        print("- documento_numero: TEXT (NOT NULL)")
        print("- documento_expedido_en: TEXT (NOT NULL)")
        print("- estudiante_programa_academico: TEXT (NOT NULL)")
        print("- semestre: TEXT (NOT NULL)")
        print("- fecha_firma_dia: TEXT (NOT NULL)")
        print("- fecha_firma_mes: TEXT (NOT NULL)")
        print("- fecha_firma_anio: TEXT (NOT NULL)")
        print("- firma_estudiante: TEXT (NOT NULL)")
        print("- documento_firma_estudiante: TEXT (NOT NULL)")
        print("- docente_permanencia: TEXT (NOT NULL)")
        print("- observaciones: TEXT (OPCIONAL)")
        print("- created_at: TIMESTAMP WITH TIME ZONE")
        print("- updated_at: TIMESTAMP WITH TIME ZONE")
        
    except Exception as e:
        print(f"Error al recrear la tabla actas_negacion: {e}")
        
        # Intentar crear la tabla desde cero si hubo un error al eliminarla
        try:
            print("\nIntentando crear la tabla desde cero...")
            sql = """
            DROP TABLE IF EXISTS actas_negacion;
            
            CREATE TABLE actas_negacion (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                estudiante_id UUID REFERENCES estudiantes(id),
                nombre_estudiante TEXT NOT NULL,
                documento_tipo TEXT NOT NULL,
                documento_numero TEXT NOT NULL,
                documento_expedido_en TEXT NOT NULL,
                estudiante_programa_academico TEXT NOT NULL,
                semestre TEXT NOT NULL,
                fecha_firma_dia TEXT NOT NULL,
                fecha_firma_mes TEXT NOT NULL,
                fecha_firma_anio TEXT NOT NULL,
                firma_estudiante TEXT NOT NULL,
                documento_firma_estudiante TEXT NOT NULL,
                docente_permanencia TEXT NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Ejecutar el SQL
            supabase.rpc('exec_sql', {'query': sql}).execute()
            print("Tabla actas_negacion creada exitosamente.")
            
        except Exception as e2:
            print(f"Error al crear la tabla desde cero: {e2}")
            print("\nSQL para crear la tabla manualmente en la consola de Supabase:")
            print("""
DROP TABLE IF EXISTS actas_negacion;

CREATE TABLE actas_negacion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estudiante_id UUID REFERENCES estudiantes(id),
    nombre_estudiante TEXT NOT NULL,
    documento_tipo TEXT NOT NULL,
    documento_numero TEXT NOT NULL,
    documento_expedido_en TEXT NOT NULL,
    estudiante_programa_academico TEXT NOT NULL,
    semestre TEXT NOT NULL,
    fecha_firma_dia TEXT NOT NULL,
    fecha_firma_mes TEXT NOT NULL,
    fecha_firma_anio TEXT NOT NULL,
    firma_estudiante TEXT NOT NULL,
    documento_firma_estudiante TEXT NOT NULL,
    docente_permanencia TEXT NOT NULL,
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
            """)

if __name__ == "__main__":
    recreate_actas_negacion_table()
