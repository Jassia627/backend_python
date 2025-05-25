from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from config import supabase
from routes.usuarios import router as usuarios_router
from routes.programas import router as programas_router
from routes.estudiantes import router as estudiantes_router
from routes.servicios import router as servicios_router
from routes.estadisticas import router as estadisticas_router
from routes.uploads import router as uploads_router
from routes.actas import router as actas_router
from routes.permanencia import router as permanencia_router

# Inicializar FastAPI
app = FastAPI(
    title="API Sistema de Permanencia UPC",
    description="API para el Sistema de Información de la Unidad de Permanencia de la Universidad Popular del Cesar. Esta API permite gestionar todos los servicios de permanencia estudiantil, incluyendo tutorías académicas, apoyo psicológico, talleres formativos, seguimiento académico y comedor universitario.",
    version="1.0.0",
    docs_url=None,  # Desactivamos la URL de docs predeterminada para personalizarla
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Universidad Popular del Cesar",
        "url": "https://www.unicesar.edu.co",
        "email": "permanencia@unicesar.edu.co"
    },
    license_info={
        "name": "Uso interno - UPC",
        "url": "https://www.unicesar.edu.co/licencia"
    },
    terms_of_service="https://www.unicesar.edu.co/terminos"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz que redirecciona a la documentación
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Personalizar documentación Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Documentación API",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
