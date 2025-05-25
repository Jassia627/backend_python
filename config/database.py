import os
import sys

# Intentar cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    if not os.getenv("SUPABASE_URL"):
        load_dotenv()
        print("Variables de entorno cargadas desde .env en database.py")
except ImportError:
    print("python-dotenv no está instalado en database.py, usando variables de entorno del sistema")

# Configuración de Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Verificar que las credenciales existan
if not supabase_url or not supabase_key:
    print("ERROR: Variables de entorno SUPABASE_URL o SUPABASE_KEY no definidas")
    if 'vercel' in os.environ.get('VERCEL', ''):
        print("Ejecutando en Vercel: asegúrate de configurar las variables de entorno en el panel de Vercel")
    # No lanzar error aquí para permitir que la aplicación se inicie en Vercel
    # En su lugar, los endpoints manejarán los errores cuando se intente acceder a la base de datos

# Inicializar cliente de Supabase
try:
    from supabase import create_client, Client
    supabase: Client = create_client(supabase_url, supabase_key)
    print(f"Conexión a Supabase establecida correctamente: {supabase_url}")
except Exception as e:
    print(f"Error al conectar con Supabase: {e}")
    if 'vercel' not in os.environ.get('VERCEL', ''):
        # Solo lanzar error si no estamos en Vercel
        raise
    else:
        # En Vercel, definir una clase de cliente falsa para evitar errores de importación
        class DummyClient:
            def __getattr__(self, name):
                def method(*args, **kwargs):
                    return None
                return method
        supabase = DummyClient()
        print("Se ha creado un cliente de Supabase ficticio para Vercel")

# Exportar supabase para que pueda ser importado desde este módulo
__all__ = ['supabase']
