from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid

from config import supabase

router = APIRouter()

# Modelo para Servicio
class Servicio(BaseModel):
    """Modelo para representar un servicio de permanencia."""
    nombre: str = Field(..., description="Nombre del servicio de permanencia")
    descripcion: str = Field(..., description="Descripción detallada del servicio")
    icono: str = Field(..., description="Icono representativo del servicio")
    key: str = Field(..., description="Clave única para identificar el servicio")
    
    class Config:
        schema_extra = {
            "example": {
                "nombre": "Tutoría Académica",
                "descripcion": "Apoyo académico personalizado para estudiantes",
                "icono": "📚",
                "key": "tutoria"
            }
        }

@router.get("/servicios", 
          summary="Obtener todos los servicios",
          description="Retorna una lista de todos los servicios de permanencia disponibles",
          response_model=List[Dict[str, Any]])
async def get_servicios():
    """Obtiene todos los servicios de permanencia."""
    try:
        response = supabase.table("servicios").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener servicios: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {str(e)}")

@router.post("/servicios", 
           summary="Crear un nuevo servicio",
           description="Registra un nuevo servicio de permanencia en el sistema",
           response_model=Dict[str, Any])
async def create_servicio(servicio: Servicio):
    """Crea un nuevo servicio de permanencia."""
    try:
        response = supabase.table("servicios").insert(servicio.dict()).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear servicio: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear servicio: {str(e)}")

# Endpoints para Asistencias a Actividades
@router.get("/asistencias-actividades", 
          summary="Obtener todas las asistencias a actividades",
          description="Retorna una lista de todas las asistencias a actividades registradas",
          response_model=List[Dict[str, Any]])
async def get_asistencias_actividades():
    """Obtiene todas las asistencias a actividades."""
    try:
        response = supabase.table("asistencias_actividades").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener asistencias a actividades: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener asistencias a actividades: {str(e)}")

@router.post("/asistencias-actividades", 
           summary="Crear una nueva asistencia a actividad",
           description="Registra una nueva asistencia a actividad",
           response_model=Dict[str, Any])
async def create_asistencia_actividad(asistencia: Dict[str, Any]):
    """Crea una nueva asistencia a actividad."""
    try:
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
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "estudiante_id", "nombre_estudiante", "numero_documento", 
            "estudiante_programa_academico", "estudiante_programa_academico_academico", 
            "semestre", "nombre_actividad", "modalidad", "tipo_actividad", 
            "fecha_actividad", "hora_inicio", "hora_fin", "modalidad_registro", 
            "observaciones", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        asistencia_filtrada = {k: v for k, v in asistencia.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Asistencia original: {asistencia}")
        print(f"Asistencia filtrada: {asistencia_filtrada}")
        
        response = supabase.table("asistencias_actividades").insert(asistencia_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear asistencia a actividad: {e}")
        return {
            "success": False,
            "error": f"Error al crear asistencia a actividad: {str(e)}",
            "message": "Hubo un problema al procesar la asistencia. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Fichas Docente
@router.get("/fichas-docente", 
          summary="Obtener todas las fichas docente",
          description="Retorna una lista de todas las fichas docente registradas",
          response_model=List[Dict[str, Any]])
async def get_fichas_docente():
    """Obtiene todas las fichas docente."""
    try:
        response = supabase.table("fichas_docente").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener fichas docente: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener fichas docente: {str(e)}")

@router.post("/fichas-docente", 
           summary="Crear una nueva ficha docente",
           description="Registra una nueva ficha docente",
           response_model=Dict[str, Any])
async def create_ficha_docente(ficha: Dict[str, Any]):
    """Crea una nueva ficha docente."""
    try:
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "nombres_apellidos", "documento_identidad", "fecha_nacimiento_dia", 
            "fecha_nacimiento_mes", "fecha_nacimiento_ano", "direccion_residencia", 
            "celular", "correo_institucional", "correo_personal", "preferencia_correo", 
            "facultad", "estudiante_programa_academico", "asignaturas", "creditos_asignaturas", 
            "ciclo_formacion", "pregrado", "especializacion", "maestria", "doctorado", 
            "grupo_investigacion", "cual_grupo", "horas_semanales", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        ficha_filtrada = {k: v for k, v in ficha.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Ficha original: {ficha}")
        print(f"Ficha filtrada: {ficha_filtrada}")
        
        response = supabase.table("fichas_docente").insert(ficha_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear ficha docente: {e}")
        return {
            "success": False,
            "error": f"Error al crear ficha docente: {str(e)}",
            "message": "Hubo un problema al procesar la ficha docente. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Intervenciones Grupales
@router.get("/intervenciones-grupales", 
          summary="Obtener todas las intervenciones grupales",
          description="Retorna una lista de todas las intervenciones grupales registradas",
          response_model=List[Dict[str, Any]])
async def get_intervenciones_grupales():
    """Obtiene todas las intervenciones grupales."""
    try:
        response = supabase.table("intervenciones_grupales").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener intervenciones grupales: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener intervenciones grupales: {str(e)}")

@router.post("/intervenciones-grupales", 
           summary="Crear una nueva intervención grupal",
           description="Registra una nueva intervención grupal",
           response_model=Dict[str, Any])
async def create_intervencion_grupal(intervencion: Dict[str, Any]):
    """Crea una nueva intervención grupal."""
    try:
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "fecha_solicitud", "nombre_docente_permanencia", "celular_permanencia", 
            "correo_permanencia", "estudiante_programa_academico_permanencia", "tipo_poblacion", 
            "nombre_docente_asignatura", "celular_docente_asignatura", "correo_docente_asignatura", 
            "estudiante_programa_academico_docente_asignatura", "asignatura_intervenir", "grupo", 
            "semestre", "numero_estudiantes", "tematica_sugerida", "fecha_estudiante_programa_academicoda", 
            "hora", "aula", "bloque", "sede", "estado", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        intervencion_filtrada = {k: v for k, v in intervencion.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Intervención original: {intervencion}")
        print(f"Intervención filtrada: {intervencion_filtrada}")
        
        response = supabase.table("intervenciones_grupales").insert(intervencion_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear intervención grupal: {e}")
        return {
            "success": False,
            "error": f"Error al crear intervención grupal: {str(e)}",
            "message": "Hubo un problema al procesar la intervención grupal. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Remisiones Psicológicas
@router.get("/remisiones-psicologicas", 
          summary="Obtener todas las remisiones psicológicas",
          description="Retorna una lista de todas las remisiones psicológicas registradas",
          response_model=List[Dict[str, Any]])
async def get_remisiones_psicologicas():
    """Obtiene todas las remisiones psicológicas."""
    try:
        response = supabase.table("remisiones_psicologicas").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener remisiones psicológicas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener remisiones psicológicas: {str(e)}")

@router.post("/remisiones-psicologicas", 
           summary="Crear una nueva remisión psicológica",
           description="Registra una nueva remisión psicológica",
           response_model=Dict[str, Any])
async def create_remision_psicologica(remision: Dict[str, Any]):
    """Crea una nueva remisión psicológica."""
    try:
        # Manejar el campo estudiante_programa_academico_academico
        if "estudiante_programa_academico_academico" in remision:
            # Asegurarse de que también exista el campo estudiante_programa_academico
            remision["estudiante_programa_academico"] = remision["estudiante_programa_academico_academico"]
        
        # Buscar estudiante por número de documento si está disponible
        if "numero_documento" in remision and "estudiante_id" not in remision:
            estudiante = supabase.table("estudiantes").select("id").eq("documento", remision["numero_documento"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                remision["estudiante_id"] = estudiante.data[0]["id"]
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                remision["estudiante_id"] = None
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "estudiante_id", "nombre_estudiante", "numero_documento", 
            "estudiante_programa_academico", "estudiante_programa_academico_academico", 
            "semestre", "motivo_remision", "docente_remite", "correo_docente", 
            "telefono_docente", "fecha", "hora", "tipo_remision", "observaciones", 
            "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        remision_filtrada = {k: v for k, v in remision.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Remisión original: {remision}")
        print(f"Remisión filtrada: {remision_filtrada}")
        
        response = supabase.table("remisiones_psicologicas").insert(remision_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear remisión psicológica: {e}")
        return {
            "success": False,
            "error": f"Error al crear remisión psicológica: {str(e)}",
            "message": "Hubo un problema al procesar la remisión psicológica. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Software Solicitudes
@router.get("/software-solicitudes", 
          summary="Obtener todas las solicitudes de software",
          description="Retorna una lista de todas las solicitudes de software registradas",
          response_model=List[Dict[str, Any]])
async def get_software_solicitudes():
    """Obtiene todas las solicitudes de software."""
    try:
        response = supabase.table("software_solicitudes").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener solicitudes de software: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes de software: {str(e)}")

@router.post("/software-solicitudes", 
           summary="Crear una nueva solicitud de software",
           description="Registra una nueva solicitud de software",
           response_model=Dict[str, Any])
async def create_software_solicitud(solicitud: Dict[str, Any]):
    """Crea una nueva solicitud de software."""
    try:
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
            from datetime import datetime
            solicitud["fecha_solicitud"] = datetime.now().isoformat()
        
        # Buscar programa_id si tenemos estudiante_programa_academico pero no programa_id
        if ("estudiante_programa_academico" in solicitud and 
            solicitud["estudiante_programa_academico"] and 
            "programa_id" not in solicitud):
            programa = supabase.table("programas").select("id").eq("nombre", solicitud["estudiante_programa_academico"]).execute()
            if programa.data and len(programa.data) > 0:
                solicitud["programa_id"] = programa.data[0]["id"]
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "estudiante_id", "programa_id", "usuario_id", "docente_tutor", 
            "facultad", "estudiante_programa_academico", "nombre_asignatura", 
            "nombre_proyecto", "descripcion", "estado", "fecha_solicitud", 
            "fecha_aprobacion", "observaciones", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        solicitud_filtrada = {k: v for k, v in solicitud.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Solicitud original: {solicitud}")
        print(f"Solicitud filtrada: {solicitud_filtrada}")
        
        # Insertar la solicitud filtrada
        response = supabase.table("software_solicitudes").insert(solicitud_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear solicitud de software: {e}")
        # Devolver un error más amigable y con información útil
        return {
            "success": False,
            "error": f"Error al crear solicitud de software: {str(e)}",
            "message": "Hubo un problema al procesar la solicitud. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Software Estudiantes
@router.get("/software-estudiantes", 
          summary="Obtener todos los estudiantes de software",
          description="Retorna una lista de todos los estudiantes de software registrados",
          response_model=List[Dict[str, Any]])
async def get_software_estudiantes():
    """Obtiene todos los estudiantes de software."""
    try:
        response = supabase.table("software_estudiantes").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener estudiantes de software: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes de software: {str(e)}")

@router.post("/software-estudiantes", 
           summary="Crear un nuevo estudiante de software",
           description="Registra un nuevo estudiante de software",
           response_model=Dict[str, Any])
async def create_software_estudiante(estudiante: Dict[str, Any]):
    """Crea un nuevo estudiante de software."""
    try:
        # Buscar estudiante_id por número de identificación si está disponible
        if "numero_identificacion" in estudiante and "estudiante_id" not in estudiante:
            est = supabase.table("estudiantes").select("id").eq("documento", estudiante["numero_identificacion"]).execute()
            if est.data and len(est.data) > 0:
                estudiante["estudiante_id"] = est.data[0]["id"]
        
        # Verificar si solicitud_id es un UUID válido
        import uuid
        if "solicitud_id" in estudiante:
            try:
                # Intentar convertir a UUID para verificar si es válido
                uuid.UUID(estudiante["solicitud_id"])
            except ValueError:
                # Si no es un UUID válido, buscar la solicitud por nombre o descripción
                print(f"Buscando solicitud con nombre o descripción: {estudiante['solicitud_id']}")
                
                # Intentar buscar por nombre_proyecto
                solicitud = supabase.table("software_solicitudes").select("id").eq("nombre_proyecto", estudiante["solicitud_id"]).execute()
                
                # Si no se encuentra, intentar buscar por nombre_asignatura
                if not solicitud.data or len(solicitud.data) == 0:
                    solicitud = supabase.table("software_solicitudes").select("id").eq("nombre_asignatura", estudiante["solicitud_id"]).execute()
                
                # Si se encuentra, usar ese ID
                if solicitud.data and len(solicitud.data) > 0:
                    estudiante["solicitud_id"] = solicitud.data[0]["id"]
                    print(f"Encontrada solicitud con ID: {estudiante['solicitud_id']}")
                else:
                    # Si no se encuentra, crear una nueva solicitud
                    nueva_solicitud = {
                        "nombre_proyecto": estudiante["solicitud_id"],
                        "nombre_asignatura": estudiante.get("asignatura", ""),
                        "estudiante_programa_academico": estudiante.get("programa", ""),
                        "docente_tutor": estudiante.get("docente", ""),
                        "estado": "Pendiente"
                    }
                    
                    solicitud_response = supabase.table("software_solicitudes").insert(nueva_solicitud).execute()
                    if solicitud_response.data and len(solicitud_response.data) > 0:
                        estudiante["solicitud_id"] = solicitud_response.data[0]["id"]
                        print(f"Creada nueva solicitud con ID: {estudiante['solicitud_id']}")
                    else:
                        # Si no se puede crear, eliminar el campo para evitar errores
                        del estudiante["solicitud_id"]
                        print("No se pudo crear una nueva solicitud, se omitirá el campo solicitud_id")
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "solicitud_id", "estudiante_id", "numero_identificacion", 
            "nombre_estudiante", "correo", "telefono", "semestre", 
            "programa", "asignatura", "docente", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        estudiante_filtrado = {k: v for k, v in estudiante.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Estudiante original: {estudiante}")
        print(f"Estudiante filtrado: {estudiante_filtrado}")
        
        response = supabase.table("software_estudiantes").insert(estudiante_filtrado).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear estudiante de software: {e}")
        return {
            "success": False,
            "error": f"Error al crear estudiante de software: {str(e)}",
            "message": "Hubo un problema al procesar el estudiante. Por favor, verifique los campos e intente nuevamente."
        }
