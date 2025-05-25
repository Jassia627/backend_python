# Backend del Sistema de Permanencia UPC

Este es el backend para el Sistema de Información de la Unidad de Permanencia de la Universidad Popular del Cesar, desarrollado con FastAPI y Supabase.

## Características

- API RESTful desarrollada con FastAPI
- Integración con Supabase como base de datos
- Soporte para carga de datos desde archivos CSV
- Endpoints para todas las entidades del sistema
- Análisis de datos para estadísticas y visualizaciones

## Requisitos

- Python 3.8+
- Cuenta en Supabase

## Instalación

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
SUPABASE_URL=tu-url-de-supabase
SUPABASE_KEY=tu-clave-de-supabase
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
python main.py
```

El servidor estará disponible en `http://127.0.0.1:8001`.

## Documentación API

La documentación interactiva de la API estará disponible en:

- Swagger UI: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

## Estructura del Proyecto

```
backend_python/
├── main.py               # Punto de entrada principal
├── config.py             # Configuración de Supabase y variables de entorno
├── routes/               # Módulos de rutas por funcionalidad
│   ├── __init__.py       # Inicializador del paquete
│   ├── usuarios.py       # Endpoints para gestión de usuarios
│   ├── programas.py      # Endpoints para gestión de programas académicos
│   ├── estudiantes.py    # Endpoints para gestión de estudiantes
│   ├── servicios.py      # Endpoints para gestión de servicios
│   ├── estadisticas.py   # Endpoints para estadísticas
│   └── uploads.py        # Endpoints para carga de archivos
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Variables de entorno (no incluido en el repositorio)
└── .env.example          # Ejemplo de archivo de variables de entorno
```

## Endpoints Principales

### Usuarios
- `GET /api/usuarios`: Obtener todos los usuarios
- `POST /api/usuarios`: Crear un nuevo usuario

### Programas Académicos
- `GET /api/programas`: Obtener todos los programas
- `POST /api/programas`: Crear un nuevo programa

### Estudiantes
- `GET /api/estudiantes`: Obtener todos los estudiantes
- `POST /api/estudiantes`: Crear un nuevo estudiante
- `GET /api/estudiantes/{estudiante_id}`: Obtener un estudiante por ID
- `GET /api/estudiantes/programa/{programa_id}`: Obtener estudiantes por programa
- `GET /api/estudiantes/riesgo/{nivel_riesgo}`: Obtener estudiantes por nivel de riesgo

### Servicios
- `GET /api/servicios`: Obtener todos los servicios
- `POST /api/servicios`: Crear un nuevo servicio
- Múltiples endpoints adicionales para asistencias, fichas docente, intervenciones, etc.

### Estadísticas
- `GET /api/estadisticas`: Obtener estadísticas generales
- `GET /api/datos-permanencia`: Obtener datos para gráficos de permanencia

### Importación de Datos
- `POST /api/upload-csv`: Cargar datos desde archivo CSV

## Desarrollo

El backend ha sido modularizado para facilitar el mantenimiento y la escalabilidad. Cada grupo de endpoints relacionados se encuentra en su propio archivo dentro del directorio `routes/`.

Para añadir nuevos endpoints, simplemente crea un nuevo archivo en el directorio `routes/` y asegúrate de incluir el router en el archivo `main.py`.
- `/api/estadisticas`: Obtención de estadísticas generales
- `/api/datos-permanencia`: Datos para análisis y visualizaciones
- `/api/upload-csv`: Carga de datos desde archivos CSV
