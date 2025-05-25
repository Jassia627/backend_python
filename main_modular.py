from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Importar rutas
from routes.usuarios import router as usuarios_router
from routes.programas import router as programas_router
from routes.estudiantes_modular import router as estudiantes_router
from routes.servicios import router as servicios_router
from routes.estadisticas import router as estadisticas_router
from routes.uploads import router as uploads_router
from routes.actas import router as actas_router
from routes.permanencia_modular import router as permanencia_router

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Permanencia API",
    description="API para el Sistema de Permanencia de la Universidad Popular del Cesar",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Incluir todos los routers
app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])
app.include_router(programas_router, prefix="/api", tags=["Programas"])
app.include_router(estudiantes_router, prefix="/api", tags=["Estudiantes"])
app.include_router(servicios_router, prefix="/api", tags=["Servicios"])
app.include_router(estadisticas_router, prefix="/api", tags=["Estadísticas"])
app.include_router(uploads_router, prefix="/api", tags=["Importación de Datos"])
app.include_router(actas_router, prefix="/api", tags=["Actas"])
app.include_router(permanencia_router, prefix="/api", tags=["Servicios de Permanencia"])

# Ruta raíz
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a la API del Sistema de Permanencia de la UPC",
        "version": app.version,
        "documentation": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_modular:app", host="127.0.0.1", port=8001, reload=True)
