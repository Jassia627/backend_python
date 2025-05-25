from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr
import uuid

from config import supabase

router = APIRouter()

# Modelo para Estudiante
class Estudiante(BaseModel):
    """Modelo para representar un estudiante en el sistema."""
    codigo: str = Field(..., description="Código estudiantil único")
    tipo_documento: str = Field(..., description="Tipo de documento de identidad (CC, TI, etc.)")
    documento: str = Field(..., description="Número de documento de identidad")
    nombre: str = Field(..., description="Nombre del estudiante")
    apellido: str = Field(..., description="Apellido del estudiante")
    email: EmailStr = Field(..., description="Correo electrónico institucional")
    telefono: str = Field(..., description="Número de teléfono de contacto")
    programa_id: uuid.UUID = Field(..., description="ID del programa académico al que pertenece")
    semestre: int = Field(..., description="Semestre actual del estudiante", ge=1, le=10)
    estrato: int = Field(..., description="Estrato socioeconómico", ge=1, le=6)
    riesgo_desercion: str = Field(..., description="Nivel de riesgo de deserción", examples=["alto", "medio", "bajo"])
    
    class Config:
        schema_extra = {
            "example": {
                "codigo": "20181578032",
                "tipo_documento": "CC",
                "documento": "1065832145",
                "nombre": "María",
                "apellido": "González",
                "email": "maria.gonzalez@unicesar.edu.co",
                "telefono": "3157894562",
                "programa_id": "123e4567-e89b-12d3-a456-426614174000",
                "semestre": 5,
                "estrato": 3,
                "riesgo_desercion": "medio"
            }
        }

@router.get("/estudiantes", 
          summary="Obtener todos los estudiantes",
          description="Retorna una lista de todos los estudiantes registrados",
          response_model=List[Dict[str, Any]])
async def get_estudiantes():
    """Obtiene todos los estudiantes."""
    try:
        response = supabase.table("estudiantes").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener estudiantes: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes: {str(e)}")

@router.post("/estudiantes", 
           summary="Crear un nuevo estudiante",
           description="Registra un nuevo estudiante en el sistema",
           response_model=Dict[str, Any])
async def create_estudiante(estudiante: Estudiante):
    """Crea un nuevo estudiante."""
    try:
        response = supabase.table("estudiantes").insert(estudiante.dict()).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear estudiante: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear estudiante: {str(e)}")

@router.get("/estudiantes/{estudiante_id}", 
          summary="Obtener un estudiante por ID",
          description="Retorna los datos de un estudiante específico",
          response_model=Dict[str, Any])
async def get_estudiante(estudiante_id: str):
    """Obtiene un estudiante por su ID."""
    try:
        response = supabase.table("estudiantes").select("*").eq("id", estudiante_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Estudiante con ID {estudiante_id} no encontrado")
        return response.data[0]
    except Exception as e:
        print(f"Error al obtener estudiante: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiante: {str(e)}")

@router.get("/estudiantes/programa/{programa_id}", 
          summary="Obtener estudiantes por programa",
          description="Retorna una lista de estudiantes filtrados por programa académico",
          response_model=List[Dict[str, Any]])
async def get_estudiantes_by_programa(programa_id: str):
    """Obtiene estudiantes filtrados por programa académico."""
    try:
        response = supabase.table("estudiantes").select("*").eq("programa_id", programa_id).execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener estudiantes por programa: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes por programa: {str(e)}")

@router.get("/estudiantes/riesgo/{nivel_riesgo}", 
          summary="Obtener estudiantes por nivel de riesgo",
          description="Retorna una lista de estudiantes filtrados por nivel de riesgo de deserción",
          response_model=List[Dict[str, Any]])
async def get_estudiantes_by_riesgo(nivel_riesgo: str):
    """Obtiene estudiantes filtrados por nivel de riesgo de deserción."""
    try:
        response = supabase.table("estudiantes").select("*").eq("riesgo_desercion", nivel_riesgo).execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener estudiantes por riesgo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes por riesgo: {str(e)}")
