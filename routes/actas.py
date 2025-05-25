from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from config import supabase

router = APIRouter()

class ActaNegacion(BaseModel):
    """Modelo para representar un acta de negación de servicio."""
    estudiante_id: Optional[uuid.UUID] = Field(None, description="ID del estudiante que niega el servicio")
    nombre_estudiante: str = Field(..., description="Nombre completo del estudiante")
    documento_tipo: str = Field(..., description="Tipo de documento del estudiante")
    documento_numero: str = Field(..., description="Número de documento del estudiante")
    documento_expedido_en: str = Field(..., description="Lugar de expedición del documento")
    estudiante_programa_academico: str = Field(..., description="Programa académico del estudiante")
    semestre: str = Field(..., description="Semestre actual del estudiante")
    fecha_firma_dia: str = Field(..., description="Día de la firma del acta")
    fecha_firma_mes: str = Field(..., description="Mes de la firma del acta")
    fecha_firma_anio: str = Field(..., description="Año de la firma del acta")
    firma_estudiante: str = Field(..., description="Firma del estudiante (texto)")
    documento_firma_estudiante: str = Field(..., description="Documento de la persona que firma")
    docente_permanencia: str = Field(..., description="Docente de permanencia")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales sobre la negación")
    created_at: Optional[str] = Field(None, description="Fecha de creación del acta")

@router.get("/actas-negacion", 
          summary="Obtener todas las actas de negación",
          description="Retorna una lista de todas las actas de negación registradas",
          response_model=List[Dict[str, Any]])
async def get_actas_negacion():
    """Obtiene todas las actas de negación."""
    try:
        response = supabase.table("actas_negacion").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener actas de negación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener actas de negación: {str(e)}")

@router.post("/actas-negacion", 
           summary="Crear una nueva acta de negación",
           description="Registra una nueva acta de negación de servicio",
           response_model=Dict[str, Any])
async def create_acta_negacion(acta: Dict[str, Any]):
    """Crea una nueva acta de negación."""
    try:
        # Añadir fecha de creación si no está presente
        if "created_at" not in acta:
            acta["created_at"] = datetime.now().isoformat()
        
        # Buscar estudiante por número de documento si no se proporciona estudiante_id
        if "documento_numero" in acta:
            estudiante = supabase.table("estudiantes").select("id").eq("documento", acta["documento_numero"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                acta["estudiante_id"] = estudiante.data[0]["id"]
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                acta["estudiante_id"] = None
        else:
            # Si no hay número de documento, establecer estudiante_id como NULL
            acta["estudiante_id"] = None
        
        print(f"Creando acta de negación: {acta}")
        response = supabase.table("actas_negacion").insert(acta).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear acta de negación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear acta de negación: {str(e)}")

@router.get("/actas-negacion/{acta_id}", 
          summary="Obtener un acta de negación por ID",
          description="Retorna los datos de un acta de negación específica",
          response_model=Dict[str, Any])
async def get_acta_negacion(acta_id: str):
    """Obtiene un acta de negación por su ID."""
    try:
        response = supabase.table("actas_negacion").select("*").eq("id", acta_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Acta de negación con ID {acta_id} no encontrada")
        return response.data[0]
    except Exception as e:
        print(f"Error al obtener acta de negación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener acta de negación: {str(e)}")

@router.delete("/actas-negacion/{acta_id}", 
             summary="Eliminar un acta de negación",
             description="Elimina un acta de negación específica",
             response_model=Dict[str, Any])
async def delete_acta_negacion(acta_id: str):
    """Elimina un acta de negación."""
    try:
        response = supabase.table("actas_negacion").delete().eq("id", acta_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Acta de negación con ID {acta_id} no encontrada")
        return {"message": "Acta de negación eliminada correctamente", "id": acta_id}
    except Exception as e:
        print(f"Error al eliminar acta de negación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar acta de negación: {str(e)}")
