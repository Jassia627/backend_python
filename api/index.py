from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import sys
import os

# Añadir el directorio raíz al path para poder importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Importar configuración
    from config import (
        APP_NAME, APP_VERSION, APP_DESCRIPTION,
        CORS_ORIGINS, CORS_METHODS, CORS_HEADERS
    )
except ImportError:
    # Valores por defecto si no se puede importar config
    APP_NAME = "API Sistema Permanencia UPC"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "API del Sistema de Permanencia de la UPC"
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]

try:
    # Importar rutas
    from routes.usuarios import router as usuarios_router
    from routes.programas import router as programas_router
    from routes.estudiantes_modular import router as estudiantes_router
    from routes.servicios_modular import router as servicios_router
    from routes.estadisticas import router as estadisticas_router
    from routes.uploads import router as uploads_router
    from routes.actas import router as actas_router
    from routes.permanencia_modular import router as permanencia_router
    from routes.intervenciones_grupales import router as intervenciones_grupales_router
    from routes.importar_intervenciones import router as importar_intervenciones_router
    
    ROUTES_AVAILABLE = True
except ImportError as e:
    print(f"Error importando rutas: {e}")
    ROUTES_AVAILABLE = False

# Inicializar FastAPI
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Personalización de la documentación OpenAPI
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

# Incluir todos los routers solo si están disponibles
if ROUTES_AVAILABLE:
    app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])
    app.include_router(programas_router, prefix="/api", tags=["Programas"])
    app.include_router(estudiantes_router, prefix="/api", tags=["Estudiantes"])
    app.include_router(servicios_router, prefix="/api", tags=["Servicios"])
    app.include_router(estadisticas_router, prefix="/api", tags=["Estadísticas"])
    app.include_router(uploads_router, prefix="/api", tags=["Importación de Datos"])
    app.include_router(actas_router, prefix="/api", tags=["Actas"])
    app.include_router(permanencia_router, prefix="/api", tags=["Servicios de Permanencia"])
    app.include_router(intervenciones_grupales_router, prefix="/api", tags=["Intervenciones Grupales"])
    app.include_router(importar_intervenciones_router, prefix="/api", tags=["Importación de Intervenciones"])

# Ruta raíz
@app.get("/docs", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a la API del Sistema de Permanencia de la UPC",
        "version": app.version,
        "documentation": "/docs",
        "redoc": "/redoc",
        "status": "Desplegado en Vercel"
    }

# Ruta de health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "routes_loaded": ROUTES_AVAILABLE
    }

# Para Vercel - IMPORTANTE
handler = app