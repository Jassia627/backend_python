from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.programas_service import ProgramasService
from models.programas import (
    ProgramaCreate, ProgramaResponse, ProgramaUpdate
)
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = ProgramasService()

@router.get("/programas", 
          summary="Obtener todos los programas académicos",
          description="Retorna una lista de todos los programas académicos registrados",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programas():
    """Obtiene todos los programas académicos."""
    try:
        programas = service.get_all_programas()
        return success_response(programas, "Programas obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener programas")

@router.get("/programas/{id}", 
          summary="Obtener un programa por ID",
          description="Retorna un programa específico según su ID",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programa(id: str):
    """Obtiene un programa por su ID."""
    try:
        programa = service.get_programa_by_id(id)
        if not programa:
            return error_response(f"Programa con ID {id} no encontrado", "Programa no encontrado", 404)
        
        return success_response(programa, "Programa obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener programa")

@router.post("/programas", 
           summary="Crear un nuevo programa académico",
           description="Registra un nuevo programa académico",
           response_model=Dict[str, Any],
           tags=["Programas"])
async def create_programa(datos: Dict[str, Any]):
    """Crea un nuevo programa académico."""
    try:
        # Validar campos requeridos
        if not datos.get("codigo"):
            return error_response("El código es obligatorio", "El código es obligatorio")
            
        if not datos.get("nombre"):
            return error_response("El nombre es obligatorio", "El nombre es obligatorio")
            
        if not datos.get("facultad"):
            return error_response("La facultad es obligatoria", "La facultad es obligatoria")
        
        # Crear programa
        result = service.create_programa(datos)
        
        return success_response(result, "Programa registrado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al crear programa")
    except Exception as e:
        return handle_exception(e, "crear programa")

@router.put("/programas/{id}", 
          summary="Actualizar un programa",
          description="Actualiza los datos de un programa existente",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def update_programa(id: str, datos: Dict[str, Any]):
    """Actualiza un programa existente."""
    try:
        # Verificar si el programa existe
        programa_existente = service.get_programa_by_id(id)
        if not programa_existente:
            return error_response(f"Programa con ID {id} no encontrado", "Programa no encontrado", 404)
        
        # Actualizar programa
        result = service.update_programa(id, datos)
        
        return success_response(result, "Programa actualizado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al actualizar programa")
    except Exception as e:
        return handle_exception(e, "actualizar programa")

@router.delete("/programas/{id}", 
             summary="Eliminar un programa",
             description="Elimina un programa existente",
             response_model=Dict[str, Any],
             tags=["Programas"])
async def delete_programa(id: str):
    """Elimina un programa existente."""
    try:
        # Verificar si el programa existe
        programa_existente = service.get_programa_by_id(id)
        if not programa_existente:
            return error_response(f"Programa con ID {id} no encontrado", "Programa no encontrado", 404)
        
        # Eliminar programa
        result = service.delete_programa(id)
        
        return success_response(result, "Programa eliminado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al eliminar programa")
    except Exception as e:
        return handle_exception(e, "eliminar programa")

@router.get("/programas/codigo/{codigo}", 
          summary="Buscar programa por código",
          description="Busca un programa por su código",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programa_by_codigo(codigo: str):
    """Busca un programa por su código."""
    try:
        programa = service.get_programa_by_codigo(codigo)
        if not programa:
            return error_response(
                f"Programa con código {codigo} no encontrado", 
                "Programa no encontrado", 
                404
            )
        
        return success_response(programa, "Programa encontrado exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar programa por código")

@router.get("/programas/facultad/{facultad}", 
          summary="Buscar programas por facultad",
          description="Busca programas por facultad",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programas_by_facultad(facultad: str):
    """Busca programas por facultad."""
    try:
        programas = service.get_programas_by_facultad(facultad)
        return success_response(programas, "Programas encontrados exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar programas por facultad")

@router.get("/programas/nivel/{nivel}", 
          summary="Buscar programas por nivel",
          description="Busca programas por nivel académico",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programas_by_nivel(nivel: str):
    """Busca programas por nivel académico."""
    try:
        programas = service.get_programas_by_nivel(nivel)
        return success_response(programas, "Programas encontrados exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar programas por nivel")

@router.get("/programas/activos", 
          summary="Obtener programas activos",
          description="Retorna una lista de todos los programas activos",
          response_model=Dict[str, Any],
          tags=["Programas"])
async def get_programas_activos():
    """Obtiene todos los programas activos."""
    try:
        programas = service.get_programas_activos()
        return success_response(programas, "Programas activos obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener programas activos")
