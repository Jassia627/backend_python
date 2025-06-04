from config import supabase
import json

def verificar_estructura_db():
    """
    Verifica la estructura de la base de datos y muestra información sobre las tablas y relaciones.
    """
    print("Verificando estructura de la base de datos...")
    
    # Obtener lista de tablas
    response = supabase.rpc('exec_sql', {'query': "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"}).execute()
    tablas = [row['table_name'] for row in response.data]
    
    print(f"\nTablas encontradas ({len(tablas)}):")
    for tabla in tablas:
        print(f"- {tabla}")
    
    # Verificar tablas específicas de permanencia
    tablas_permanencia = [
        "tutorias_academicas",
        "asesorias_psicologicas",
        "orientaciones_vocacionales",
        "comedores_universitarios",
        "apoyos_socioeconomicos",
        "talleres_habilidades",
        "seguimientos_academicos"
    ]
    
    print("\nVerificando tablas de permanencia:")
    for tabla in tablas_permanencia:
        if tabla in tablas:
            print(f"✅ {tabla} - Existe")
            
            # Verificar relación con estudiantes
            query = f"""
            SELECT ccu.table_name, ccu.column_name, ccu.constraint_name, 
                   kcu.referenced_table_name, kcu.referenced_column_name
            FROM information_schema.constraint_column_usage AS ccu
            JOIN information_schema.key_column_usage AS kcu 
                ON ccu.constraint_name = kcu.constraint_name
            WHERE ccu.table_name = '{tabla}'
              AND kcu.referenced_table_name = 'estudiantes'
            """
            
            try:
                rel_response = supabase.rpc('exec_sql', {'query': query}).execute()
                if rel_response.data and len(rel_response.data) > 0:
                    print(f"   ✅ Tiene relación con estudiantes")
                else:
                    print(f"   ❌ No se encontró relación con estudiantes")
            except Exception as e:
                print(f"   ❌ Error al verificar relación: {str(e)}")
        else:
            print(f"❌ {tabla} - No existe")
    
    # Verificar estructura de estudiantes
    try:
        estudiantes = supabase.table("estudiantes").select("*").limit(1).execute()
        print("\nEstructura de la tabla estudiantes:")
        if estudiantes.data:
            for key in estudiantes.data[0].keys():
                print(f"- {key}")
        else:
            print("No hay datos en la tabla estudiantes")
    except Exception as e:
        print(f"Error al verificar estudiantes: {str(e)}")

if __name__ == "__main__":
    verificar_estructura_db()
