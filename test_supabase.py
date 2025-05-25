import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key[:10]}...")

try:
    # Inicializar cliente de Supabase
    supabase: Client = create_client(supabase_url, supabase_key)
    print("Conexión a Supabase establecida correctamente")
    
    # Verificar si la tabla usuarios existe
    try:
        response = supabase.table("usuarios").select("*").execute()
        print(f"Tabla usuarios accesible. Registros: {len(response.data)}")
        print(f"Datos: {response.data}")
    except Exception as e:
        print(f"Error al acceder a la tabla usuarios: {e}")
    
    # Verificar si la tabla programas existe
    try:
        response = supabase.table("programas").select("*").execute()
        print(f"Tabla programas accesible. Registros: {len(response.data)}")
        print(f"Datos: {response.data}")
    except Exception as e:
        print(f"Error al acceder a la tabla programas: {e}")
    
    # Intentar insertar un registro de prueba
    try:
        response = supabase.table("programas").insert({
            "nombre": "Programa de Prueba",
            "facultad": "Facultad de Prueba",
            "codigo": "TEST-001"
        }).execute()
        print(f"Inserción exitosa: {response.data}")
    except Exception as e:
        print(f"Error al insertar: {e}")
        
except Exception as e:
    print(f"Error al conectar con Supabase: {e}")
