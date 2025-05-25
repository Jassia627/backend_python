"""Módulo de configuración para la aplicación.
Proporciona acceso a la configuración de la base de datos y otras configuraciones.
"""

import os
import sys

# Intentar cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Variables de entorno cargadas desde .env")
except ImportError:
    print("python-dotenv no está instalado, usando variables de entorno del sistema")

# Configuración de la aplicación
APP_NAME = "Sistema de Permanencia API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "API para el Sistema de Permanencia de la Universidad Popular del Cesar"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificar que las variables de Supabase estén definidas
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ADVERTENCIA: Variables de Supabase no configuradas correctamente")
    if 'vercel' in os.environ.get('VERCEL', ''):
        print("Ejecutando en Vercel: asegúrate de configurar las variables de entorno en el panel de Vercel")

# Configuración del servidor
HOST = os.getenv("HOST", "0.0.0.0")  # Cambiado a 0.0.0.0 para Vercel
PORT = int(os.getenv("PORT", "8000"))  # Puerto estándar para Vercel

# Configuración CORS
# Permitir todos los orígenes para desarrollo, ajustar para producción
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# Otras configuraciones
# Usar un directorio temporal para uploads en Vercel
if 'vercel' in os.environ.get('VERCEL', ''):
    UPLOAD_FOLDER = "/tmp/uploads"
else:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

# Crear el directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Importar supabase desde database.py
from .database import supabase

__all__ = [
    'supabase',
    'APP_NAME', 'APP_VERSION', 'APP_DESCRIPTION', 'DEBUG',
    'SUPABASE_URL', 'SUPABASE_KEY',
    'HOST', 'PORT',
    'CORS_ORIGINS', 'CORS_METHODS', 'CORS_HEADERS',
    'UPLOAD_FOLDER'
]
