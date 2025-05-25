import sys
import os

# Añadir el directorio raíz al path para poder importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar supabase desde config.py
try:
    from config import supabase
    # Exportar supabase para que pueda ser importado desde este paquete
    __all__ = ['supabase']
except ImportError:
    print("Error al importar supabase desde config.py")
    # Intentar importar directamente
    try:
        import os
        from dotenv import load_dotenv
        from supabase import create_client, Client

        # Cargar variables de entorno
        load_dotenv()

        # Configuración de Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        # Inicializar cliente de Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        print(f"Conexión a Supabase establecida correctamente: {supabase_url}")
        
        # Exportar supabase
        __all__ = ['supabase']
    except Exception as e:
        print(f"Error al conectar con Supabase: {e}")
        raise
