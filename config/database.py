# Importar la configuración de Supabase existente
import sys
import os

# Añadir el directorio raíz al path para poder importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la configuración existente
from config import supabase

# Exportar supabase para que pueda ser importado desde este módulo
__all__ = ['supabase']
