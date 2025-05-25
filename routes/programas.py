from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from config import supabase

router = APIRouter()

# Modelo para Programa
class Programa(BaseModel):
    """Modelo para representar un programa académico."""
    nombre: str = Field(..., description="Nombre completo del programa académico")
    facultad: str = Field(..., description="Facultad a la que pertenece el programa")
    codigo: str = Field(..., description="Código único del programa académico")
    
    class Config:
        schema_extra = {
            "example": {
                "nombre": "Ingeniería de Sistemas",
                "facultad": "Ingeniería",
                "codigo": "ING-SIS"
            }
        }

@router.get("/programas", 
          summary="Obtener todos los programas académicos",
          description="Retorna una lista de todos los programas académicos registrados",
          response_model=List[Dict[str, Any]])
async def get_programas():
    """Obtiene todos los programas académicos."""
    try:
        response = supabase.table("programas").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener programas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener programas: {str(e)}")

@router.post("/programas", 
           summary="Crear un nuevo programa académico",
           description="Registra un nuevo programa académico en el sistema",
           response_model=Dict[str, Any])
async def create_programa(programa: Programa):
    """Crea un nuevo programa académico."""
    try:
        response = supabase.table("programas").insert(programa.dict()).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear programa: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear programa: {str(e)}")
