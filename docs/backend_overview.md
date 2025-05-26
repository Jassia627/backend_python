# Documentación del Backend

## Visión General

El backend del sistema de permanencia estudiantil está desarrollado en Python utilizando el framework FastAPI. Este sistema permite gestionar y analizar datos relacionados con la permanencia de estudiantes en la universidad, incluyendo información sobre programas académicos, servicios de bienestar universitario, y seguimiento de riesgo de deserción.

## Arquitectura

El sistema sigue una arquitectura basada en API RESTful con los siguientes componentes principales:

1. **FastAPI**: Framework web de alto rendimiento para construir APIs con Python.
2. **Supabase**: Plataforma de base de datos PostgreSQL como servicio, utilizada para almacenar todos los datos del sistema.
3. **Pandas**: Biblioteca de análisis de datos utilizada para procesar archivos CSV y manipular datos.

## Estructura del Proyecto

```
backend_python/
├── config/
│   └── __init__.py        # Configuración de conexión a Supabase
├── routes/
│   ├── uploads.py         # Endpoints para carga de datos
│   ├── estudiantes.py     # Endpoints para gestión de estudiantes
│   ├── estadisticas.py    # Endpoints para datos estadísticos
│   └── ...
├── scripts/
│   └── create_tables.sql  # Script para crear tablas en la base de datos
├── main.py                # Punto de entrada de la aplicación
└── requirements.txt       # Dependencias del proyecto
```

## Tecnologías Utilizadas

- **Python 3.9+**: Lenguaje de programación principal.
- **FastAPI**: Framework web para crear APIs.
- **Supabase**: Base de datos PostgreSQL como servicio.
- **Pandas**: Procesamiento y análisis de datos.
- **Pydantic**: Validación de datos y configuración.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

## Flujo de Datos

1. Los datos se cargan al sistema a través de archivos CSV mediante el endpoint de carga.
2. Los datos se procesan y se validan antes de ser almacenados en la base de datos.
3. Los endpoints de estadísticas consultan la base de datos para generar información agregada.
4. El frontend consume estos endpoints para mostrar gráficos y tablas informativas.

## Seguridad

- La autenticación se maneja a través de Supabase Auth.
- Las claves de API y credenciales se almacenan como variables de entorno.
- Se implementan validaciones de datos para prevenir inyecciones SQL y otros ataques.

## Manejo de Errores

El sistema implementa un manejo robusto de errores que:
- Proporciona mensajes de error descriptivos.
- Registra errores detallados para depuración.
- Continúa procesando datos incluso cuando ocurren errores en registros individuales.
