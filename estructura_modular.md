# Estructura Modular para el Backend

## 1. Estructura de Directorios

```
backend_python/
├── config/                  # Configuración de la aplicación
│   ├── __init__.py
│   ├── database.py          # Configuración de Supabase
│   └── settings.py          # Configuración general
├── models/                  # Modelos de datos (Pydantic)
│   ├── __init__.py
│   ├── estudiantes.py       # Modelos relacionados con estudiantes
│   ├── programas.py         # Modelos relacionados con programas
│   ├── servicios.py         # Modelos relacionados con servicios
│   ├── permanencia.py       # Modelos relacionados con servicios de permanencia
│   └── usuarios.py          # Modelos relacionados con usuarios
├── data/            # Capa de acceso a datos
│   ├── __init__.py
│   ├── base_data.py   # Data base con operaciones comunes
│   ├── estudiantes_data.py  # Acceso a datos de estudiantes
│   ├── programas_data.py    # Acceso a datos de programas
│   ├── servicios_data.py    # Acceso a datos de servicios
│   ├── permanencia_data.py  # Acceso a datos de servicios de permanencia
│   └── usuarios_data.py     # Acceso a datos de usuarios
├── services/                # Lógica de negocio
│   ├── __init__.py
│   ├── estudiantes_service.py  # Servicio para estudiantes
│   ├── programas_service.py    # Servicio para programas
│   ├── servicios_service.py    # Servicio para servicios
│   ├── permanencia_service.py  # Servicio para servicios de permanencia
│   └── usuarios_service.py     # Servicio para usuarios
├── routes/                  # Rutas de la API
│   ├── __init__.py
│   ├── estudiantes.py       # Rutas para estudiantes
│   ├── programas.py         # Rutas para programas
│   ├── servicios.py         # Rutas para servicios
│   ├── permanencia.py       # Rutas para servicios de permanencia
│   └── usuarios.py          # Rutas para usuarios
├── utils/                   # Utilidades comunes
│   ├── __init__.py
│   ├── validators.py        # Validadores comunes
│   ├── formatters.py        # Formateadores de datos
│   └── error_handlers.py    # Manejadores de errores
├── tests/                   # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── test_estudiantes.py
│   ├── test_programas.py
│   ├── test_servicios.py
│   ├── test_permanencia.py
│   └── test_usuarios.py
├── .env                     # Variables de entorno
├── .env.example             # Ejemplo de variables de entorno
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias
└── README.md                # Documentación
```

## 2. Implementación por Capas

### 2.1. Capa de Modelos (models/)

Define la estructura de los datos utilizando Pydantic.

Ejemplo (`models/estudiantes.py`):
```python
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class EstudianteBase(BaseModel):
    documento: str
    tipo_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteResponse(EstudianteBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
```

### 2.2. Capa de Data (data/)

Encapsula el acceso a la base de datos.

Ejemplo (`data/base_data.py`):
```python
from typing import Dict, List, Any, Optional, Type
from pydantic import BaseModel

from config.database import supabase

class BaseData:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_all(self) -> List[Dict[str, Any]]:
        response = supabase.table(self.table_name).select("*").execute()
        return response.data

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        response = supabase.table(self.table_name).select("*").eq("id", id).execute()
        return response.data[0] if response.data else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = supabase.table(self.table_name).insert(data).execute()
        return response.data[0] if response.data else {}

    def update(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = supabase.table(self.table_name).update(data).eq("id", id).execute()
        return response.data[0] if response.data else {}

    def delete(self, id: str) -> bool:
        response = supabase.table(self.table_name).delete().eq("id", id).execute()
        return len(response.data) > 0
```

Ejemplo (`data/estudiantes_repo.py`):
```python
from typing import Dict, List, Any, Optional
from .base_data import BaseData

class EstudiantesData(BaseData):
    def __init__(self):
        super().__init__("estudiantes")

    def get_by_documento(self, documento: str) -> Optional[Dict[str, Any]]:
        response = supabase.table(self.table_name).select("*").eq("documento", documento).execute()
        return response.data[0] if response.data else None
```

### 2.3. Capa de Servicios (services/)

Implementa la lógica de negocio.

Ejemplo (`services/estudiantes_service.py`):
```python
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from data.estudiantes_repo import EstudiantesData
from models.estudiantes import EstudianteCreate, EstudianteResponse

class EstudiantesService:
    def __init__(self):
        self.data = EstudiantesData()

    def get_all_estudiantes(self) -> List[EstudianteResponse]:
        estudiantes = self.data.get_all()
        return [EstudianteResponse(**estudiante) for estudiante in estudiantes]

    def create_estudiante(self, estudiante: EstudianteCreate) -> EstudianteResponse:
        estudiante_data = estudiante.dict()
        estudiante_data["created_at"] = datetime.now().isoformat()
        estudiante_data["updated_at"] = datetime.now().isoformat()
        
        result = self.data.create(estudiante_data)
        return EstudianteResponse(**result)

    def get_or_create_estudiante(self, estudiante: EstudianteCreate) -> EstudianteResponse:
        # Buscar estudiante por documento
        existing = self.data.get_by_documento(estudiante.documento)
        
        if existing:
            return EstudianteResponse(**existing)
        
        # Crear nuevo estudiante
        return self.create_estudiante(estudiante)
```

### 2.4. Capa de Rutas (routes/)

Define los endpoints de la API.

Ejemplo (`routes/estudiantes.py`):
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models.estudiantes import EstudianteCreate, EstudianteResponse
from services.estudiantes_service import EstudiantesService

router = APIRouter()
service = EstudiantesService()

@router.get("/", response_model=List[EstudianteResponse])
async def get_estudiantes():
    """Obtiene todos los estudiantes."""
    try:
        return service.get_all_estudiantes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes: {str(e)}")

@router.post("/", response_model=EstudianteResponse)
async def create_estudiante(estudiante: EstudianteCreate):
    """Crea un nuevo estudiante."""
    try:
        return service.create_estudiante(estudiante)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear estudiante: {str(e)}")
```

## 3. Punto de Entrada (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from routes import estudiantes, programas, servicios, permanencia, usuarios

app = FastAPI(
    title="Sistema de Permanencia API",
    description="API para el Sistema de Permanencia de la Universidad Popular del Cesar",
    version="1.0.0",
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
app.include_router(estudiantes.router, prefix="/api/estudiantes", tags=["Estudiantes"])
app.include_router(programas.router, prefix="/api/programas", tags=["Programas"])
app.include_router(servicios.router, prefix="/api/servicios", tags=["Servicios"])
app.include_router(permanencia.router, prefix="/api", tags=["Servicios de Permanencia"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
```

## 4. Ventajas de esta Estructura

1. **Separación de responsabilidades**: Cada capa tiene una responsabilidad clara.
2. **Reutilización de código**: Los data y servicios base permiten reutilizar código común.
3. **Mantenibilidad**: Es más fácil mantener y extender el código cuando está bien organizado.
4. **Testabilidad**: Es más fácil escribir pruebas unitarias para cada capa.
5. **Escalabilidad**: La estructura permite agregar nuevas funcionalidades sin modificar el código existente.
