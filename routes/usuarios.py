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

@router.get("/usuarios/{id}", 
          summary="Obtener un usuario por ID",
          description="Retorna un usuario específico según su ID",
          response_model=Dict[str, Any],
          tags=["Usuarios"])
async def get_usuario(id: str):
    """Obtiene un usuario por su ID."""
    
    try:
        usuario = service.get_usuario_by_id(id)
        if not usuario:
            return error_response(f"Usuario con ID {id} no encontrado", "Usuario no encontrado", 404)
        
        return success_response(usuario, "Usuario obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener usuario")

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

@router.put("/usuarios/{id}", 
          summary="Actualizar un usuario",
          description="Actualiza los datos de un usuario existente",
          response_model=Dict[str, Any],
          tags=["Usuarios"])
async def update_usuario(id: str, datos: Dict[str, Any]):
    """Actualiza un usuario existente."""
    
    try:
        # Verificar si el usuario existe
        usuario_existente = service.get_usuario_by_id(id)
        if not usuario_existente:
            return error_response(f"Usuario con ID {id} no encontrado", "Usuario no encontrado", 404)
        
        # Actualizar usuario
        result = service.update_usuario(id, datos)
        
        return success_response(result, "Usuario actualizado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al actualizar usuario")
    except Exception as e:
        return handle_exception(e, "actualizar usuario")

@router.delete("/usuarios/{id}", 
             summary="Eliminar un usuario",
             description="Elimina un usuario existente",
             response_model=Dict[str, Any],
             tags=["Usuarios"])
async def delete_usuario(id: str):
    """Elimina un usuario existente."""
    
    try:
        # Verificar si el usuario existe
        usuario_existente = service.get_usuario_by_id(id)
        if not usuario_existente:
            return error_response(f"Usuario con ID {id} no encontrado", "Usuario no encontrado", 404)
        
        # Eliminar usuario
        result = service.delete_usuario(id)
        
        return success_response(result, "Usuario eliminado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al eliminar usuario")
    except Exception as e:
        return handle_exception(e, "eliminar usuario")

@router.get("/usuarios/email/{email}", 
          summary="Buscar usuario por email",
          description="Busca un usuario por su email",
          response_model=Dict[str, Any],
          tags=["Usuarios"])
async def get_usuario_by_email(email: str):
    """Busca un usuario por su email."""
    
    try:
        usuario = service.get_usuario_by_email(email)
        if not usuario:
            return error_response(
                f"Usuario con email {email} no encontrado", 
                "Usuario no encontrado", 
                404
            )
        
        return success_response(usuario, "Usuario encontrado exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar usuario por email")

@router.get("/usuarios/rol/{rol}", 
          summary="Buscar usuarios por rol",
          description="Busca usuarios por rol",
          response_model=Dict[str, Any],
          tags=["Usuarios"])
async def get_usuarios_by_rol(rol: str):
    """Busca usuarios por rol."""
    
    try:
        usuarios = service.get_usuarios_by_rol(rol)
        return success_response(usuarios, "Usuarios encontrados exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar usuarios por rol")

@router.post("/login", 
           summary="Iniciar sesión",
           description="Autentica un usuario y devuelve un token de acceso",
           response_model=Dict[str, Any],
           tags=["Autenticación"])
async def login(datos: Dict[str, Any]):
    """Inicia sesión de un usuario."""
    
    try:
        # Validar campos requeridos
        if not datos.get("email"):
            return error_response("El email es obligatorio", "El email es obligatorio")
            
        if not datos.get("password"):
            return error_response("La contraseña es obligatoria", "La contraseña es obligatoria")
        
        # Autenticar usuario
        token = service.login(datos["email"], datos["password"])
        if not token:
            return error_response("Credenciales inválidas", "Credenciales inválidas", status.HTTP_401_UNAUTHORIZED)
        
        return success_response({"access_token": token.access_token, "token_type": token.token_type}, "Inicio de sesión exitoso")
    except Exception as e:
        return handle_exception(e, "iniciar sesión")
