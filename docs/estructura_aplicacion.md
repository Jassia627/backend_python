# Estructura de la Aplicación

## Índice
- [Visión General](#visión-general)
- [Estructura de Directorios](#estructura-de-directorios)
- [Componentes Principales](#componentes-principales)
- [Flujo de Datos](#flujo-de-datos)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Configuración](#configuración)
- [Despliegue](#despliegue)

## Visión General

El Sistema de Permanencia de la Universidad Popular del Cesar es una aplicación backend desarrollada con FastAPI que proporciona servicios para gestionar la permanencia estudiantil, incluyendo seguimiento académico, servicios de apoyo, intervenciones grupales y estadísticas. La aplicación se conecta a una base de datos Supabase para almacenar y recuperar información.

## Estructura de Directorios

```
backend_python/
│
├── config/                   # Configuración de la aplicación
│   └── __init__.py           # Variables de entorno y configuración
│
├── models/                   # Modelos de datos (Pydantic)
│   ├── estudiantes.py        # Modelos para estudiantes
│   ├── programas.py          # Modelos para programas académicos
│   ├── servicios.py          # Modelos para servicios
│   ├── permanencia.py        # Modelos para permanencia
│   └── usuarios.py           # Modelos para usuarios
│
├── routes/                   # Rutas de la API (endpoints)
│   ├── actas.py              # Endpoints para actas
│   ├── estadisticas.py       # Endpoints para estadísticas
│   ├── estudiantes_modular.py # Endpoints para estudiantes
│   ├── importar_intervenciones.py # Endpoints para importar intervenciones
│   ├── intervenciones_grupales.py # Endpoints para intervenciones grupales
│   ├── permanencia_modular.py # Endpoints para permanencia
│   ├── programas.py          # Endpoints para programas académicos
│   ├── servicios_modular.py  # Endpoints para servicios
│   ├── uploads.py            # Endpoints para importación de datos
│   └── usuarios.py           # Endpoints para usuarios
│
├── scripts/                  # Scripts SQL para la base de datos
│   ├── crear_tabla_permanencia.sql # Crear tabla de permanencia
│   ├── crear_tabla_servicios.sql # Crear tabla de servicios
│   ├── recrear_intervenciones_grupales.sql # Recrear tabla de intervenciones
│   └── ... (otros scripts)
│
├── services/                 # Lógica de negocio
│   └── ... (servicios)
│
├── utils/                    # Utilidades y funciones auxiliares
│   └── responses.py          # Funciones para respuestas estándar
│
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación general
```

## Componentes Principales

### 1. Configuración (`config/`)

Este módulo maneja la configuración de la aplicación, incluyendo:
- Variables de entorno (cargadas desde `.env`)
- Conexión a Supabase
- Configuración del servidor
- Configuración CORS

### 2. Modelos (`models/`)

Define los modelos de datos utilizando Pydantic, que proporcionan:
- Validación de datos
- Serialización/deserialización
- Documentación automática para Swagger/OpenAPI

Principales modelos:
- **Estudiantes**: Información de estudiantes (documento, nombres, programa académico, etc.)
- **Programas**: Programas académicos (nombre, facultad, nivel)
- **Servicios**: Servicios ofrecidos (código, nombre, descripción)
- **Permanencia**: Registros de permanencia estudiantil
- **Usuarios**: Información de usuarios del sistema

### 3. Rutas (`routes/`)

Contiene los endpoints de la API organizados por módulos:
- **estudiantes_modular.py**: Gestión de estudiantes
- **programas.py**: Gestión de programas académicos
- **servicios_modular.py**: Gestión de servicios
- **intervenciones_grupales.py**: Gestión de intervenciones grupales
- **permanencia_modular.py**: Gestión de permanencia
- **actas.py**: Gestión de actas
- **estadisticas.py**: Endpoints para estadísticas
- **uploads.py**: Importación de datos desde CSV

### 4. Scripts (`scripts/`)

Scripts SQL para:
- Crear y modificar tablas
- Consultar datos
- Verificar estructura de la base de datos
- Insertar datos de prueba

### 5. Servicios (`services/`)

Implementa la lógica de negocio separada de los endpoints, siguiendo el patrón de diseño de servicios.

### 6. Utilidades (`utils/`)

Funciones auxiliares como:
- Manejo de respuestas estándar (éxito, error)
- Manejo de excepciones
- Conversión de formatos

### 7. Punto de entrada (`main.py`)

Inicializa la aplicación FastAPI, configura middleware CORS y registra todos los routers.

## Flujo de Datos

1. **Solicitud HTTP**: El cliente envía una solicitud a un endpoint.
2. **Middleware**: La solicitud pasa por middleware (CORS, etc.).
3. **Router**: El router correspondiente maneja la solicitud.
4. **Validación**: Los datos se validan usando modelos Pydantic.
5. **Procesamiento**: Se ejecuta la lógica de negocio (consultas a Supabase, etc.).
6. **Respuesta**: Se devuelve una respuesta HTTP con los datos solicitados o confirmación.

## Tecnologías Utilizadas

- **FastAPI**: Framework web de alto rendimiento para APIs.
- **Pydantic**: Validación de datos y serialización.
- **Supabase**: Base de datos y autenticación.
- **Pandas**: Procesamiento de datos para importación CSV.
- **Python 3.10+**: Lenguaje de programación.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

## Configuración

La aplicación utiliza variables de entorno para configuración:

- `SUPABASE_URL`: URL de la instancia de Supabase.
- `SUPABASE_KEY`: Clave de API de Supabase.
- `HOST`: Host para el servidor (por defecto: 0.0.0.0).
- `PORT`: Puerto para el servidor (por defecto: 8000).
- `DEBUG`: Modo de depuración (True/False).

Estas variables se cargan desde un archivo `.env` usando `python-dotenv`.

## Despliegue

### Desarrollo local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python main.py
```

### Producción

Para despliegue en producción, se recomienda:
- Usar Gunicorn como servidor WSGI
- Configurar un proxy inverso (Nginx)
- Usar variables de entorno para configuración
- Deshabilitar el modo de depuración
