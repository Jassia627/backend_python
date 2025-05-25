from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict, Any

# Crear una aplicación FastAPI simplificada para Vercel
app = FastAPI(title="API Sistema de Permanencia UPC")

# Configuración CORS para Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba
@app.get("/")
async def root():
    return {
        "message": "API del Sistema de Permanencia UPC funcionando en Vercel",
        "status": "online"
    }

# Ruta de estado para Supabase
@app.get("/api/status")
async def status():
    supabase_url = os.environ.get("SUPABASE_URL")
    return {
        "status": "online",
        "supabase_configured": supabase_url is not None,
        "environment": "vercel"
    }

# Función para manejar errores
def handle_exception(e: Exception, operation: str) -> Dict[str, Any]:
    error_message = f"Error al {operation}: {str(e)}"
    print(error_message)
    return {
        "success": False,
        "error": error_message,
        "message": f"Hubo un problema al {operation}. Por favor, inténtelo de nuevo más tarde."
    }

# Ruta de ejemplo para probar la conexión a Supabase
@app.get("/api/test-supabase")
async def test_supabase():
    try:
        # Intentar importar e inicializar Supabase
        from supabase import create_client
        
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "message": "Variables de entorno de Supabase no configuradas"
            }
        
        # Intentar conectar a Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        # Probar una consulta simple
        try:
            response = supabase.table("software_solicitudes").select("count", count="exact").limit(1).execute()
            count = response.count if hasattr(response, 'count') else 0
            return {
                "success": True,
                "message": "Conexión a Supabase exitosa",
                "count": count
            }
        except Exception as query_error:
            return handle_exception(query_error, "consultar Supabase")
            
    except Exception as e:
        return handle_exception(e, "inicializar Supabase")
