import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno si no se han cargado ya
if not os.getenv("SUPABASE_URL"):
    load_dotenv()

# Configuración de Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Inicializar cliente de Supabase
try:
    supabase: Client = create_client(supabase_url, supabase_key)
    print(f"Conexión a Supabase establecida correctamente: {supabase_url}")
except Exception as e:
    print(f"Error al conectar con Supabase: {e}")
    raise

# Exportar supabase para que pueda ser importado desde este módulo
__all__ = ['supabase']
