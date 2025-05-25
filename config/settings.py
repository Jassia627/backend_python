import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la aplicación
APP_NAME = "Sistema de Permanencia API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "API para el Sistema de Permanencia de la Universidad Popular del Cesar"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configuración del servidor
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8001"))

# Configuración CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Otras configuraciones
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
