from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.usuarios_service import UsuariosService
from models.usuarios import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioLogin, Token
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = UsuariosService()

@router.get("/usuarios", 
          summary="Obtener todos los usuarios",
          description="Retorna una lista de todos los usuarios registrados",
          response_model=Dict[str, Any],
          tags=["Usuarios"])
async def get_usuarios():
    """Obtiene todos los usuarios."""
    
    try:
        usuarios = service.get_all_usuarios()
        return success_response(usuarios, "Usuarios obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener usuarios")


@router.post("/usuarios", 
           summary="Crear un nuevo usuario",
           description="Registra un nuevo usuario",
           response_model=Dict[str, Any],
           tags=["Usuarios"])
async def create_usuario(datos: Dict[str, Any]):
    """Crea un nuevo usuario."""
    
    try:
        # Validar campos requeridos
        if not datos.get("email"):
            return error_response("El email es obligatorio", "El email es obligatorio")
            
        if not datos.get("nombre"):
            return error_response("El nombre es obligatorio", "El nombre es obligatorio")
            
        if not datos.get("apellido"):
            return error_response("El apellido es obligatorio", "El apellido es obligatorio")
            
        if not datos.get("rol"):
            return error_response("El rol es obligatorio", "El rol es obligatorio")
            
        if not datos.get("password"):
            return error_response("La contraseña es obligatoria", "La contraseña es obligatoria")
        
        # Crear usuario
        result = service.create_usuario(datos)
        
        return success_response(result, "Usuario registrado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al crear usuario")
    except Exception as e:
        return handle_exception(e, "crear usuario")


