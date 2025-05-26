from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


from services.programas_service import ProgramasService
from models.programas import (
    ProgramaCreate, ProgramaResponse, ProgramaUpdate
)
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = ProgramasService()

FACULTADES_UPC = [
    "Facultad Ciencias Administrativas contables y económicas",
    "Facultad de bellas artes",
    "Facultad de derecho, ciencias políticas y sociales",
    "Facultad DE Ciencias Básicas",
    "Facultad ingenierías y tecnologías",
    "Facultad Ciencias de la salud",
    "Facultad DE Educación"
]

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

        # Validar formato tipo INF-101
        if not isinstance(datos["codigo"], str) or not re.match(r"^[A-Z]{3}-\d{3}$", datos["codigo"]):
            return error_response("El código debe tener el formato ABC-123 (3 letras mayúsculas, guion y 3 números)", "Código inválido")


        if not datos.get("nombre"):
            return error_response("El nombre es obligatorio", "El nombre es obligatorio")
        if not isinstance(datos["nombre"], str) or not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,100}$", datos["nombre"]):
            return error_response("El nombre debe contener solo letras y espacios (mínimo 3, máximo 100 caracteres)", "Nombre inválido")

        if not datos.get("facultad"):
            return error_response("La facultad es obligatoria", "La facultad es obligatoria")
        if datos["facultad"] not in FACULTADES_UPC:
            return error_response(f"La facultad '{datos['facultad']}' no es válida", "Facultad inválida")

        # Validar nivel
        if "nivel" in datos:
            if datos["nivel"] not in ["Pregrado", "Postgrado"]:
                return error_response("El nivel debe ser 'Pregrado' o 'Postgrado'", "Nivel inválido")

        # Validar modalidad
        if "modalidad" in datos:
           if datos["modalidad"] not in ["Presencial", "Virtual", "Hibrido"]:
            return error_response("La modalidad debe ser 'Presencial' o 'Virtual' o 'Hibrido'", "Modalidad inválida")

        # Validar estado
        if "estado" in datos:
           if datos["estado"] not in ["Activo", "Inactivo"]:
            return error_response("El estado debe ser 'Activo' o 'Inactivo'", "Estado inválido")

        
        # Crear programa
        result = service.create_programa(datos)
        
        return success_response(result, "Programa registrado exitosamente")
    except ValueError as ve:
        return error_response(str(ve), "Error al crear programa")
    except Exception as e:
        return handle_exception(e, "crear programa")



