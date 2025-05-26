from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, date, time
from pydantic import BaseModel, Field

from config import supabase
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()

# Modelo para crear una intervención grupal
class IntervencionGrupalCreate(BaseModel):
    fecha_solicitud: date
    nombre_docente_permanencia: str
    celular_permanencia: str
    correo_permanencia: str
    estudiante_programa_academico_permanencia: str
    tipo_poblacion: str
    nombre_docente_asignatura: str
    celular_docente_asignatura: str
    correo_docente_asignatura: str
    estudiante_programa_academico_docente_asignatura: str
    asignatura_intervenir: str
    grupo: str
    semestre: str
    numero_estudiantes: str
    tematica_sugerida: Optional[str] = None
    fecha_estudiante_programa_academicoda: date
    hora: str
    aula: str
    bloque: str
    sede: str
    estado: str
    motivo: Optional[str] = None
    efectividad: Optional[str] = "Pendiente evaluación"
    estudiante_id: Optional[str] = None

# Modelo para respuesta
class IntervencionGrupalResponse(BaseModel):
    id: str
    fecha_solicitud: str
    nombre_docente_permanencia: str
    celular_permanencia: str
    correo_permanencia: str
    estudiante_programa_academico_permanencia: str
    tipo_poblacion: str
    nombre_docente_asignatura: str
    celular_docente_asignatura: str
    correo_docente_asignatura: str
    estudiante_programa_academico_docente_asignatura: str
    asignatura_intervenir: str
    grupo: str
    semestre: str
    numero_estudiantes: str
    tematica_sugerida: Optional[str] = None
    fecha_estudiante_programa_academicoda: str
    hora: str
    aula: str
    bloque: str
    sede: str
    estado: str
    motivo: Optional[str] = None
    efectividad: str
    created_at: datetime
    updated_at: datetime

@router.post("/intervenciones-grupales", 
           summary="Crear una nueva intervención grupal",
           description="Registra una nueva intervención grupal",
           response_model=Dict[str, Any],
           tags=["Intervenciones Grupales"])
async def create_intervencion_grupal(datos: Dict[str, Any]):
    """Crea una nueva intervención grupal."""
    try:
        # Validar campos requeridos
        campos_requeridos = [
            "fecha_solicitud", "nombre_docente_permanencia", "celular_permanencia",
            "correo_permanencia", "estudiante_programa_academico_permanencia", "tipo_poblacion",
            "nombre_docente_asignatura", "celular_docente_asignatura", "correo_docente_asignatura",
            "estudiante_programa_academico_docente_asignatura", "asignatura_intervenir",
            "grupo", "semestre", "numero_estudiantes", "fecha_estudiante_programa_academicoda",
            "hora", "aula", "bloque", "sede", "estado"
        ]
        
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return error_response(f"El campo {campo} es obligatorio", f"El campo {campo} es obligatorio")
        
        # Si el estado no es "se hizo", el motivo es obligatorio
        if datos["estado"] != "se hizo" and (not datos.get("motivo") or not datos["motivo"].strip()):
            return error_response("El motivo es obligatorio cuando el estado no es 'se hizo'", "El motivo es obligatorio")
        
        # Establecer efectividad por defecto si no está presente
        if "efectividad" not in datos:
            datos["efectividad"] = "Pendiente evaluación" if datos["estado"] == "se hizo" else "N/A"
        
        # Insertar en la base de datos
        result = supabase.table("intervenciones_grupales").insert(datos).execute()
        
        if not result.data:
            return error_response("Error al crear la intervención grupal", "Error al crear la intervención grupal")
        
        return success_response(result.data[0], "Intervención grupal creada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear intervención grupal")

@router.get("/intervenciones-grupales", 
          summary="Obtener todas las intervenciones grupales",
          description="Retorna una lista de todas las intervenciones grupales registradas",
          response_model=List[Dict[str, Any]],
          tags=["Intervenciones Grupales"])
async def get_intervenciones_grupales():
    """Obtiene todas las intervenciones grupales."""
    try:
        result = supabase.table("intervenciones_grupales").select("*").order("created_at", desc=True).execute()
        
        if not result.data:
            return []
        
        return result.data
    except Exception as e:
        print(f"Error al obtener intervenciones grupales: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener intervenciones grupales: {str(e)}")

@router.get("/intervenciones-grupales/{id}", 
          summary="Obtener una intervención grupal por ID",
          description="Retorna una intervención grupal específica según su ID",
          response_model=Dict[str, Any],
          tags=["Intervenciones Grupales"])
async def get_intervencion_grupal(id: str):
    """Obtiene una intervención grupal por su ID."""
    try:
        result = supabase.table("intervenciones_grupales").select("*").eq("id", id).execute()
        
        if not result.data or len(result.data) == 0:
            return error_response(f"Intervención grupal con ID {id} no encontrada", "Intervención grupal no encontrada", 404)
        
        return success_response(result.data[0], "Intervención grupal obtenida exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener intervención grupal")

@router.put("/intervenciones-grupales/{id}", 
          summary="Actualizar una intervención grupal",
          description="Actualiza una intervención grupal existente",
          response_model=Dict[str, Any],
          tags=["Intervenciones Grupales"])
async def update_intervencion_grupal(id: str, datos: Dict[str, Any]):
    """Actualiza una intervención grupal existente."""
    try:
        # Verificar si la intervención existe
        check = supabase.table("intervenciones_grupales").select("id").eq("id", id).execute()
        
        if not check.data or len(check.data) == 0:
            return error_response(f"Intervención grupal con ID {id} no encontrada", "Intervención grupal no encontrada", 404)
        
        # Si el estado no es "se hizo", el motivo es obligatorio
        if datos.get("estado") and datos["estado"] != "se hizo" and (not datos.get("motivo") or not datos["motivo"].strip()):
            return error_response("El motivo es obligatorio cuando el estado no es 'se hizo'", "El motivo es obligatorio")
        
        # Actualizar efectividad si se cambia el estado
        if datos.get("estado"):
            if datos["estado"] == "se hizo" and (not datos.get("efectividad") or datos.get("efectividad") == "N/A"):
                datos["efectividad"] = "Pendiente evaluación"
            elif datos["estado"] != "se hizo":
                datos["efectividad"] = "N/A"
        
        # Actualizar en la base de datos
        datos["updated_at"] = datetime.now().isoformat()
        result = supabase.table("intervenciones_grupales").update(datos).eq("id", id).execute()
        
        if not result.data:
            return error_response("Error al actualizar la intervención grupal", "Error al actualizar la intervención grupal")
        
        return success_response(result.data[0], "Intervención grupal actualizada exitosamente")
    except Exception as e:
        return handle_exception(e, "actualizar intervención grupal")

@router.delete("/intervenciones-grupales/{id}", 
             summary="Eliminar una intervención grupal",
             description="Elimina una intervención grupal existente",
             response_model=Dict[str, Any],
             tags=["Intervenciones Grupales"])
async def delete_intervencion_grupal(id: str):
    """Elimina una intervención grupal existente."""
    try:
        # Verificar si la intervención existe
        check = supabase.table("intervenciones_grupales").select("id").eq("id", id).execute()
        
        if not check.data or len(check.data) == 0:
            return error_response(f"Intervención grupal con ID {id} no encontrada", "Intervención grupal no encontrada", 404)
        
        # Eliminar de la base de datos
        result = supabase.table("intervenciones_grupales").delete().eq("id", id).execute()
        
        return success_response({"id": id}, "Intervención grupal eliminada exitosamente")
    except Exception as e:
        return handle_exception(e, "eliminar intervención grupal")
