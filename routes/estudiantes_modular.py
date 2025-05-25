from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.estudiantes_service import EstudiantesService
from models.estudiantes import (
    EstudianteCreate, EstudianteResponse, EstudianteUpdate
)
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = EstudiantesService()

@router.get("/estudiantes", 
          summary="Obtener todos los estudiantes",
          description="Retorna una lista de todos los estudiantes registrados",
          response_model=Dict[str, Any],
          tags=["Estudiantes"])
async def get_estudiantes():
    """Obtiene todos los estudiantes."""
    try:
        estudiantes = service.get_all_estudiantes()
        return success_response(estudiantes, "Estudiantes obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener estudiantes")

@router.get("/estudiantes/{id}", 
          summary="Obtener un estudiante por ID",
          description="Retorna un estudiante específico según su ID",
          response_model=Dict[str, Any],
          tags=["Estudiantes"])
async def get_estudiante(id: str):
    """Obtiene un estudiante por su ID."""
    try:
        estudiante = service.get_estudiante_by_id(id)
        if not estudiante:
            return error_response(f"Estudiante con ID {id} no encontrado", "Estudiante no encontrado", 404)
        
        return success_response(estudiante, "Estudiante obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener estudiante")

@router.post("/estudiantes", 
           summary="Crear un nuevo estudiante",
           description="Registra un nuevo estudiante",
           response_model=Dict[str, Any],
           tags=["Estudiantes"])
async def create_estudiante(datos: Dict[str, Any]):
    """Crea un nuevo estudiante."""
    try:
        print(f"Recibiendo datos de estudiante: {datos}")
        
        # Validar campos requeridos
        if not datos.get("numero_documento"):
            return error_response("El número de documento es obligatorio", "El número de documento es obligatorio")
            
        if not datos.get("tipo_documento"):
            return error_response("El tipo de documento es obligatorio", "El tipo de documento es obligatorio")
            
        if not datos.get("nombres"):
            return error_response("Los nombres son obligatorios", "Los nombres son obligatorios")
            
        if not datos.get("apellidos"):
            return error_response("Los apellidos son obligatorios", "Los apellidos son obligatorios")
        
        # Crear estudiante
        result = service.create_estudiante(datos)
        
        return success_response(result, "Estudiante registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear estudiante")

@router.put("/estudiantes/{id}", 
          summary="Actualizar un estudiante",
          description="Actualiza los datos de un estudiante existente",
          response_model=Dict[str, Any],
          tags=["Estudiantes"])
async def update_estudiante(id: str, datos: Dict[str, Any]):
    """Actualiza un estudiante existente."""
    try:
        # Verificar si el estudiante existe
        estudiante_existente = service.get_estudiante_by_id(id)
        if not estudiante_existente:
            return error_response(f"Estudiante con ID {id} no encontrado", "Estudiante no encontrado", 404)
        
        # Actualizar estudiante
        result = service.update_estudiante(id, datos)
        
        return success_response(result, "Estudiante actualizado exitosamente")
    except Exception as e:
        return handle_exception(e, "actualizar estudiante")

@router.delete("/estudiantes/{id}", 
             summary="Eliminar un estudiante",
             description="Elimina un estudiante existente",
             response_model=Dict[str, Any],
             tags=["Estudiantes"])
async def delete_estudiante(id: str):
    """Elimina un estudiante existente."""
    try:
        # Verificar si el estudiante existe
        estudiante_existente = service.get_estudiante_by_id(id)
        if not estudiante_existente:
            return error_response(f"Estudiante con ID {id} no encontrado", "Estudiante no encontrado", 404)
        
        # Eliminar estudiante
        result = service.delete_estudiante(id)
        
        return success_response(result, "Estudiante eliminado exitosamente")
    except Exception as e:
        return handle_exception(e, "eliminar estudiante")

@router.get("/estudiantes/documento/{tipo_documento}/{numero_documento}", 
          summary="Buscar estudiante por documento",
          description="Busca un estudiante por tipo y número de documento",
          response_model=Dict[str, Any],
          tags=["Estudiantes"])
async def get_estudiante_by_documento(tipo_documento: str, numero_documento: str):
    """Busca un estudiante por tipo y número de documento."""
    try:
        estudiante = service.get_estudiante_by_documento(tipo_documento, numero_documento)
        if not estudiante:
            return error_response(
                f"Estudiante con documento {tipo_documento} {numero_documento} no encontrado", 
                "Estudiante no encontrado", 
                404
            )
        
        return success_response(estudiante, "Estudiante encontrado exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar estudiante por documento")

@router.post("/estudiantes/buscar-o-crear", 
           summary="Buscar o crear estudiante",
           description="Busca un estudiante por documento o lo crea si no existe",
           response_model=Dict[str, Any],
           tags=["Estudiantes"])
async def buscar_o_crear_estudiante(datos: Dict[str, Any]):
    """Busca un estudiante por documento o lo crea si no existe."""
    try:
        # Validar campos requeridos
        if not datos.get("numero_documento"):
            return error_response("El número de documento es obligatorio", "El número de documento es obligatorio")
            
        if not datos.get("tipo_documento"):
            return error_response("El tipo de documento es obligatorio", "El tipo de documento es obligatorio")
        
        # Buscar o crear estudiante
        result = service.buscar_o_crear_estudiante(datos)
        
        return success_response(result, "Operación realizada exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar o crear estudiante")
