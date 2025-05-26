from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.estudiantes_service import EstudiantesService
from models.estudiantes import (
    EstudianteCreate, EstudianteResponse, EstudianteUpdate
)
from utils.responses import success_response, error_response, handle_exception

import re

router = APIRouter()
service = EstudiantesService()

@router.get("/estudiantes", 
          summary="Obtener todos los estudiantes",
          description="Retorna una lista de todos los estudiantes registrados",
          response_model=Dict[str, Any],
          tags=["Estudiantes"])
async def get_estudiantes():
    try:
        estudiantes = service.get_all_estudiantes()
        return success_response(estudiantes, "Estudiantes obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener estudiantes")


@router.post("/estudiantes", 
           summary="Crear un nuevo estudiante",
           description="Registra un nuevo estudiante",
           response_model=Dict[str, Any],
           tags=["Estudiantes"])
async def create_estudiante(datos: Dict[str, Any]):
    try:
        print(f"Recibiendo datos de estudiante: {datos}")
        
        # Validar campos requeridos
        if not datos.get("documento"):
            return error_response("El número de documento es obligatorio", "El número de documento es obligatorio")
        if not datos.get("tipo_documento"):
            return error_response("El tipo de documento es obligatorio", "El tipo de documento es obligatorio")
        if not datos.get("nombres"):
            return error_response("Los nombres son obligatorios", "Los nombres son obligatorios")
        if not datos.get("apellidos"):
            return error_response("Los apellidos son obligatorios", "Los apellidos son obligatorios")

        # Validar numero_documento
        doc = datos["documento"]
        if not doc.isdigit():
            return error_response("El número de documento debe contener solo números", "Documento inválido")
        if not (7 <= len(doc) <= 10):
            return error_response("El número de documento debe tener entre 7 y 10 dígitos", "Documento inválido")

        # Validar tipo_documento
        if not datos["tipo_documento"].isalpha():
            return error_response("El tipo de documento debe contener solo letras", "Tipo de documento inválido")

        # Validar nombres y apellidos
        letras_re = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
        if not letras_re.fullmatch(datos["nombres"].strip()):
            return error_response("El nombre solo debe contener letras y espacios", "Nombre inválido")
        if not letras_re.fullmatch(datos["apellidos"].strip()):
            return error_response("El apellido solo debe contener letras y espacios", "Apellido inválido")

        # Validar teléfono si viene
        telefono = datos.get("telefono")
        if telefono:
            if not telefono.isdigit():
                return error_response("El teléfono debe contener solo números", "Teléfono inválido")
            if len(telefono) != 10:
                return error_response("El teléfono debe tener exactamente 10 dígitos", "Teléfono inválido")
            if not telefono.startswith("3"):
                return error_response("El teléfono debe comenzar con '3'", "Teléfono inválido")

        # Validar semestre si viene
        semestre = datos.get("semestre")
        if semestre and (not str(semestre).isdigit() or not (1 <= int(semestre) <= 10)):
            return error_response("El semestre debe ser un número entre 1 y 10", "Semestre inválido")

        # Validar estrato si viene
        estrato = datos.get("estrato")
        if estrato is not None and (not isinstance(estrato, int) or not (1 <= estrato <= 6)):
            return error_response("El estrato debe estar entre 1 y 6", "Estrato inválido")
        
        # ✅ Validar que el correo sea institucional
        correo = datos.get("correo").lower()
        if not correo.endswith("@unicesar.edu.co"):
            return error_response("El correo debe ser institucional (@unicesar.edu.co)", "Correo inválido")
        
        from data.estudiantes_data import EstudiantesData
        estudiantes_data = EstudiantesData()

        correo_existente = estudiantes_data.get_by_correo(datos.get("correo"))
        if correo_existente:
            return error_response("Ya existe un estudiante registrado con este correo", "Correo duplicado")

        # Crear estudiante
        result = service.create_estudiante(datos)
        return success_response(result, "Estudiante registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear estudiante")


