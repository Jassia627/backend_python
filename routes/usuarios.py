from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

import sys
import os

# Añadir el directorio raíz al path para poder importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar supabase desde config.py en la raíz
from config import supabase

router = APIRouter()

# Modelo para Usuario
class Usuario(BaseModel):
    """Modelo para representar un usuario del sistema."""
    email: EmailStr = Field(..., description="Correo electrónico del usuario, debe ser único")
    nombre: str = Field(..., description="Nombre del usuario")
    apellido: str = Field(..., description="Apellido del usuario")
    rol: str = Field(..., description="Rol del usuario en el sistema", examples=["admin", "docente", "psicologo", "coordinador"])
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@unicesar.edu.co",
                "nombre": "Juan",
                "apellido": "Pérez",
                "rol": "docente"
            }
        }

@router.get("/usuarios", 
          summary="Obtener todos los usuarios",
          description="Retorna una lista de todos los usuarios registrados en el sistema",
          response_model=List[Dict[str, Any]])
async def get_usuarios():
    """Obtiene todos los usuarios del sistema."""
    try:
        response = supabase.table("usuarios").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@router.post("/usuarios", 
           summary="Crear un nuevo usuario",
           description="Registra un nuevo usuario en el sistema",
           response_model=Dict[str, Any])
async def create_usuario(usuario: Usuario):
    """Crea un nuevo usuario en el sistema."""
    try:
        response = supabase.table("usuarios").insert(usuario.dict()).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")
