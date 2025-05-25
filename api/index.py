from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

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

# Funciones de utilidad para respuestas
def success_response(data: Any, message: str, status_code: int = 200) -> Dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "message": message,
        "status_code": status_code
    }

def error_response(error: str, message: str, status_code: int = 400) -> Dict[str, Any]:
    return {
        "success": False,
        "error": error,
        "message": message,
        "status_code": status_code
    }

def handle_exception(e: Exception, operation: str) -> Dict[str, Any]:
    error_message = f"Error al {operation}: {str(e)}"
    print(error_message)
    return {
        "success": False,
        "error": error_message,
        "message": f"Hubo un problema al {operation}. Por favor, inténtelo de nuevo más tarde."
    }

# Función para inicializar Supabase
def get_supabase_client():
    try:
        from supabase import create_client
        
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("Variables de entorno de Supabase no configuradas")
            return None
        
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error al inicializar Supabase: {e}")
        return None

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

# Ruta para probar la conexión a Supabase
@app.get("/api/test-supabase")
async def test_supabase():
    supabase = get_supabase_client()
    if not supabase:
        return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
    
    try:
        response = supabase.table("software_solicitudes").select("count", count="exact").limit(1).execute()
        count = response.count if hasattr(response, 'count') else 0
        return success_response({"count": count}, "Conexión a Supabase exitosa")
    except Exception as e:
        return handle_exception(e, "consultar Supabase")

# ============== ENDPOINTS PARA SOFTWARE SOLICITUDES ==============

@app.get("/api/software-solicitudes")
async def get_software_solicitudes():
    """Obtiene todas las solicitudes de software."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("software_solicitudes").select("*").execute()
        return success_response(response.data, "Solicitudes de software obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener solicitudes de software")

@app.get("/api/software-solicitudes/{id}")
async def get_software_solicitud(id: str):
    """Obtiene una solicitud de software por su ID."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("software_solicitudes").select("*").eq("id", id).execute()
        if not response.data:
            return error_response(f"Solicitud de software con ID {id} no encontrada", "Solicitud no encontrada", 404)
        
        return success_response(response.data[0], "Solicitud de software obtenida exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener solicitud de software")

@app.post("/api/software-solicitudes")
async def create_software_solicitud(solicitud: Dict[str, Any]):
    """Crea una nueva solicitud de software."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        # Añadir valores por defecto para campos requeridos si no están presentes
        if "nombre_proyecto" not in solicitud or not solicitud["nombre_proyecto"]:
            # Usar nombre_asignatura como nombre_proyecto si está disponible
            if "nombre_asignatura" in solicitud and solicitud["nombre_asignatura"]:
                solicitud["nombre_proyecto"] = f"Proyecto {solicitud['nombre_asignatura']}"
            else:
                solicitud["nombre_proyecto"] = "Proyecto de Software"
        
        # Añadir estado por defecto si no está presente
        if "estado" not in solicitud or not solicitud["estado"]:
            solicitud["estado"] = "Pendiente"
            
        # Añadir fecha de solicitud si no está presente
        if "fecha_solicitud" not in solicitud or not solicitud["fecha_solicitud"]:
            solicitud["fecha_solicitud"] = datetime.now().isoformat()
        
        # Buscar programa_id si tenemos estudiante_programa_academico pero no programa_id
        if ("estudiante_programa_academico" in solicitud and 
            solicitud["estudiante_programa_academico"] and 
            "programa_id" not in solicitud):
            programa = supabase.table("programas").select("id").eq("nombre", solicitud["estudiante_programa_academico"]).execute()
            if programa.data and len(programa.data) > 0:
                solicitud["programa_id"] = programa.data[0]["id"]
        
        # Añadir timestamps si no están presentes
        if "created_at" not in solicitud:
            solicitud["created_at"] = datetime.now().isoformat()
        
        # Generar un ID para la solicitud si no tiene uno
        if "id" not in solicitud or not solicitud["id"]:
            solicitud["id"] = str(uuid.uuid4())
        
        # Insertar la solicitud en la base de datos
        response = supabase.table("software_solicitudes").insert(solicitud).execute()
        
        if not response.data:
            return error_response("No se pudo crear la solicitud", "Error al insertar en la base de datos")
        
        return success_response(response.data[0], "Solicitud de software creada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear solicitud de software")

# ============== ENDPOINTS PARA SOFTWARE ESTUDIANTES ==============

@app.get("/api/software-estudiantes")
async def get_software_estudiantes():
    """Obtiene todos los estudiantes de software."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("software_estudiantes").select("*").execute()
        return success_response(response.data, "Estudiantes de software obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener estudiantes de software")

@app.get("/api/software-estudiantes/{id}")
async def get_software_estudiante(id: str):
    """Obtiene un estudiante de software por su ID."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("software_estudiantes").select("*").eq("id", id).execute()
        if not response.data:
            return error_response(f"Estudiante de software con ID {id} no encontrado", "Estudiante no encontrado", 404)
        
        return success_response(response.data[0], "Estudiante de software obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener estudiante de software")

@app.post("/api/software-estudiantes")
async def create_software_estudiante(estudiante: Dict[str, Any]):
    """Crea un nuevo estudiante de software."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        # Asegurar que los campos requeridos estén presentes
        required_fields = ["solicitud_id", "numero_identificacion", "nombre_estudiante"]
        for field in required_fields:
            if field not in estudiante or not estudiante[field]:
                return error_response(f"Campo requerido '{field}' faltante", "Datos incompletos")
        
        # Convertir solicitud_id a UUID si es necesario
        if "solicitud_id" in estudiante and estudiante["solicitud_id"]:
            try:
                # Verificar si es un UUID válido
                uuid_obj = uuid.UUID(estudiante["solicitud_id"])
                estudiante["solicitud_id"] = str(uuid_obj)
            except ValueError:
                print(f"solicitud_id no es un UUID válido: {estudiante['solicitud_id']}")
                # Si no es un UUID válido, intentamos buscar la solicitud por otro campo
                # (esto depende de tu lógica de negocio)
        
        # Generar un ID para el estudiante si no tiene uno
        if "id" not in estudiante or not estudiante["id"]:
            estudiante["id"] = str(uuid.uuid4())
        
        # Añadir timestamps si no están presentes
        if "created_at" not in estudiante:
            estudiante["created_at"] = datetime.now().isoformat()
        
        # Insertar el estudiante en la base de datos
        print(f"Insertando estudiante: {estudiante}")
        response = supabase.table("software_estudiantes").insert(estudiante).execute()
        
        if not response.data:
            return error_response("No se pudo crear el estudiante", "Error al insertar en la base de datos")
        
        return success_response(response.data[0], "Estudiante de software creado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear estudiante de software")

# ============== ENDPOINTS PARA FICHAS DOCENTE ==============

@app.get("/api/fichas-docente")
async def get_fichas_docente():
    """Obtiene todas las fichas docente."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("fichas_docente").select("*").execute()
        return success_response(response.data, "Fichas docente obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener fichas docente")

@app.post("/api/fichas-docente")
async def create_ficha_docente(ficha: Dict[str, Any]):
    """Crea una nueva ficha docente."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        # Generar un ID para la ficha si no tiene uno
        if "id" not in ficha or not ficha["id"]:
            ficha["id"] = str(uuid.uuid4())
        
        # Añadir timestamps si no están presentes
        if "created_at" not in ficha:
            ficha["created_at"] = datetime.now().isoformat()
        
        # Insertar la ficha en la base de datos
        response = supabase.table("fichas_docente").insert(ficha).execute()
        
        if not response.data:
            return error_response("No se pudo crear la ficha docente", "Error al insertar en la base de datos")
        
        return success_response(response.data[0], "Ficha docente creada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear ficha docente")

# ============== ENDPOINTS PARA ASISTENCIAS A ACTIVIDADES ==============

@app.get("/api/asistencias-actividades")
async def get_asistencias_actividades():
    """Obtiene todas las asistencias a actividades."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("asistencias_actividades").select("*").execute()
        return success_response(response.data, "Asistencias a actividades obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener asistencias a actividades")

@app.post("/api/asistencias-actividades")
async def create_asistencia_actividad(asistencia: Dict[str, Any]):
    """Crea una nueva asistencia a actividad."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        # Manejar el campo estudiante_programa_academico_academico
        if "estudiante_programa_academico_academico" in asistencia:
            # Asegurarse de que también exista el campo estudiante_programa_academico
            asistencia["estudiante_programa_academico"] = asistencia["estudiante_programa_academico_academico"]
        
        # Buscar estudiante por número de documento si está disponible
        if "numero_documento" in asistencia and "estudiante_id" not in asistencia:
            estudiante = supabase.table("estudiantes").select("id").eq("documento", asistencia["numero_documento"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                asistencia["estudiante_id"] = estudiante.data[0]["id"]
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                asistencia["estudiante_id"] = None
        
        # Generar un ID para la asistencia si no tiene uno
        if "id" not in asistencia or not asistencia["id"]:
            asistencia["id"] = str(uuid.uuid4())
        
        # Añadir timestamps si no están presentes
        if "created_at" not in asistencia:
            asistencia["created_at"] = datetime.now().isoformat()
        
        # Insertar la asistencia en la base de datos
        response = supabase.table("asistencias_actividades").insert(asistencia).execute()
        
        if not response.data:
            return error_response("No se pudo crear la asistencia", "Error al insertar en la base de datos")
        
        return success_response(response.data[0], "Asistencia a actividad creada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear asistencia a actividad")

# ============== ENDPOINTS PARA SERVICIOS ==============

@app.get("/api/servicios")
async def get_servicios():
    """Obtiene todos los servicios."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("servicios").select("*").execute()
        return success_response(response.data, "Servicios obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener servicios")

@app.get("/api/servicios/{id}")
async def get_servicio(id: str):
    """Obtiene un servicio por su ID."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        response = supabase.table("servicios").select("*").eq("id", id).execute()
        if not response.data:
            return error_response(f"Servicio con ID {id} no encontrado", "Servicio no encontrado", 404)
        
        return success_response(response.data[0], "Servicio obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener servicio")

@app.post("/api/servicios")
async def create_servicio(servicio: Dict[str, Any]):
    """Crea un nuevo servicio."""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return error_response("Supabase no inicializado", "No se pudo conectar a Supabase")
        
        # Generar un ID para el servicio si no tiene uno
        if "id" not in servicio or not servicio["id"]:
            servicio["id"] = str(uuid.uuid4())
        
        # Añadir timestamps si no están presentes
        if "created_at" not in servicio:
            servicio["created_at"] = datetime.now().isoformat()
        
        # Insertar el servicio en la base de datos
        response = supabase.table("servicios").insert(servicio).execute()
        
        if not response.data:
            return error_response("No se pudo crear el servicio", "Error al insertar en la base de datos")
        
        return success_response(response.data[0], "Servicio creado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear servicio")
