from typing import Dict, Any, Optional, List, Union
from fastapi import HTTPException
from fastapi.responses import JSONResponse

def success_response(data: Any = None, message: str = "Operación exitosa") -> Dict[str, Any]:
    """
    Crea una respuesta de éxito estándar.
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje de éxito
        
    Returns:
        Respuesta de éxito
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(error: str, message: str = "Ha ocurrido un error", status_code: int = 400) -> Dict[str, Any]:
    """
    Crea una respuesta de error estándar.
    
    Args:
        error: Descripción técnica del error
        message: Mensaje de error para el usuario
        status_code: Código de estado HTTP
        
    Returns:
        Respuesta de error
    """
    return {
        "success": False,
        "error": error,
        "message": message
    }

def handle_exception(e: Exception, operation: str) -> Dict[str, Any]:
    """
    Maneja una excepción y crea una respuesta de error apropiada.
    
    Args:
        e: Excepción a manejar
        operation: Descripción de la operación que falló
        
    Returns:
        Respuesta de error
    """
    error_message = f"Error al {operation}: {str(e)}"
    user_message = f"Hubo un problema al {operation}. Por favor, verifique los campos e intente nuevamente."
    
    print(error_message)
    
    return error_response(error_message, user_message)

def raise_not_found(resource: str, id: str) -> None:
    """
    Lanza una excepción HTTP 404 para un recurso no encontrado.
    
    Args:
        resource: Nombre del recurso
        id: ID del recurso
    """
    raise HTTPException(status_code=404, detail=f"{resource} con ID {id} no encontrado")

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Valida que todos los campos requeridos estén presentes en los datos.
    
    Args:
        data: Datos a validar
        required_fields: Lista de campos requeridos
        
    Raises:
        ValueError: Si falta algún campo requerido
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(f"Faltan campos requeridos: {', '.join(missing_fields)}")

def filter_valid_fields(data: Dict[str, Any], valid_fields: List[str]) -> Dict[str, Any]:
    """
    Filtra los campos válidos de un diccionario.
    
    Args:
        data: Datos a filtrar
        valid_fields: Lista de campos válidos
        
    Returns:
        Diccionario con solo los campos válidos
    """
    return {k: v for k, v in data.items() if k in valid_fields}
