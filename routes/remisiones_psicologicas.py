from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field

from config import supabase
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()

# Modelo para crear una remisión psicológica
class RemisionPsicologicaCreate(BaseModel):
    nombre_estudiante: str
    numero_documento: str
    programa_academico: str
    semestre: str
    motivo_remision: str
    docente_remite: str
    correo_docente: str
    telefono_docente: str
    fecha: date
    hora: str
    tipo_remision: str
    observaciones: Optional[str] = None

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
        return handle_exception(e, "obtener remisiones psicológicas")

@router.get("/remisiones-psicologicas/{id}", 
          summary="Obtener una remisión psicológica por ID",
          description="Retorna una remisión psicológica específica según su ID",
          response_model=Dict[str, Any])
async def get_remision_psicologica(id: str):
    """Obtiene una remisión psicológica por su ID."""
    try:
        response = supabase.table("remisiones_psicologicas").select("*").eq("id", id).execute()
        if not response.data:
            return error_response(f"Remisión psicológica con ID {id} no encontrada", "Remisión no encontrada", 404)
        
        return success_response(response.data[0], "Remisión psicológica obtenida exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener remisión psicológica")

@router.post("/remisiones-psicologicas", 
           summary="Crear una nueva remisión psicológica",
           description="Registra una nueva remisión psicológica",
           response_model=Dict[str, Any])
async def create_remision_psicologica(remision: RemisionPsicologicaCreate):
    """Crea una nueva remisión psicológica."""
    try:
        # Convertir el modelo Pydantic a diccionario
        remision_dict = remision.dict()
        
        print(f"Datos recibidos para remisión psicológica: {remision_dict}")
        
        # Mapear campos correctamente
        if "estudiante_programa_academico_academico" in remision_dict and not "programa_academico" in remision_dict:
            remision_dict["programa_academico"] = remision_dict["estudiante_programa_academico_academico"]
            print(f"Mapeando estudiante_programa_academico_academico a programa_academico: {remision_dict['programa_academico']}")
        
        # Si no hay programa_academico, establecer un valor por defecto
        if not "programa_academico" in remision_dict or not remision_dict["programa_academico"]:
            remision_dict["programa_academico"] = "No especificado"
            print(f"Estableciendo programa_academico por defecto: {remision_dict['programa_academico']}")
            
        # Buscar estudiante por número de documento
        estudiante = supabase.table("estudiantes").select("id").eq("documento", remision_dict["numero_documento"]).execute()
        if estudiante.data and len(estudiante.data) > 0:
            remision_dict["estudiante_id"] = estudiante.data[0]["id"]
            print(f"Estudiante encontrado con ID: {remision_dict['estudiante_id']}")
        else:
            # Si no se encuentra el estudiante, establecer estudiante_id como NULL
            remision_dict["estudiante_id"] = None
            print("No se encontró estudiante con ese documento")
        
        # Añadir timestamps
        remision_dict["created_at"] = datetime.now().isoformat()
        remision_dict["updated_at"] = datetime.now().isoformat()
        
        # Convertir fecha a formato string si es necesario
        if isinstance(remision_dict["fecha"], date):
            remision_dict["fecha"] = remision_dict["fecha"].isoformat()
        
        # Imprimir para depuración
        print(f"Remisión a insertar: {remision_dict}")
        
        # Insertar en la base de datos
        response = supabase.table("remisiones_psicologicas").insert(remision_dict).execute()
        
        if response.data and len(response.data) > 0:
            return success_response(response.data[0], "Remisión psicológica registrada exitosamente")
        else:
            return error_response("No se pudo registrar la remisión psicológica", "Error al registrar remisión")
    except Exception as e:
        print(f"Error al crear remisión psicológica: {str(e)}")
        import traceback
        traceback.print_exc()
        return handle_exception(e, "crear remisión psicológica")

@router.put("/remisiones-psicologicas/{id}", 
          summary="Actualizar una remisión psicológica",
          description="Actualiza los datos de una remisión psicológica existente",
          response_model=Dict[str, Any])
async def update_remision_psicologica(id: str, remision: Dict[str, Any]):
    """Actualiza una remisión psicológica existente."""
    try:
        # Verificar si la remisión existe
        check_response = supabase.table("remisiones_psicologicas").select("*").eq("id", id).execute()
        if not check_response.data:
            return error_response(f"Remisión psicológica con ID {id} no encontrada", "Remisión no encontrada", 404)
        
        # Actualizar timestamp
        remision["updated_at"] = datetime.now().isoformat()
        
        # Actualizar remisión
        response = supabase.table("remisiones_psicologicas").update(remision).eq("id", id).execute()
        
        return success_response(response.data[0], "Remisión psicológica actualizada exitosamente")
    except Exception as e:
        return handle_exception(e, "actualizar remisión psicológica")

@router.delete("/remisiones-psicologicas/{id}", 
             summary="Eliminar una remisión psicológica",
             description="Elimina una remisión psicológica existente",
             response_model=Dict[str, Any])
async def delete_remision_psicologica(id: str):
    """Elimina una remisión psicológica existente."""
    try:
        # Verificar si la remisión existe
        check_response = supabase.table("remisiones_psicologicas").select("*").eq("id", id).execute()
        if not check_response.data:
            return error_response(f"Remisión psicológica con ID {id} no encontrada", "Remisión no encontrada", 404)
        
        # Eliminar remisión
        response = supabase.table("remisiones_psicologicas").delete().eq("id", id).execute()
        
        return success_response({"id": id}, "Remisión psicológica eliminada exitosamente")
    except Exception as e:
        return handle_exception(e, "eliminar remisión psicológica")
