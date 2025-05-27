from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, date, time
from pydantic import BaseModel, Field

from config import supabase
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()

# Modelo para crear una intervención grupal
class IntervencionGrupalCreate(BaseModel):
    fecha_solicitud: date
    nombre_docente_permanencia: str
    celular_permanencia: str
    correo_permanencia: str
    estudiante_programa_academico_permanencia: str
    tipo_poblacion: str
    nombre_docente_asignatura: str
    celular_docente_asignatura: str
    correo_docente_asignatura: str
    estudiante_programa_academico_docente_asignatura: str
    asignatura_intervenir: str
    grupo: str
    semestre: str
    numero_estudiantes: str
    tematica_sugerida: Optional[str] = None
    fecha_estudiante_programa_academicoda: date
    hora: str
    aula: str
    bloque: str
    sede: str
    estado: str
    motivo: Optional[str] = None
    efectividad: Optional[str] = "Pendiente evaluación"
    estudiante_id: Optional[str] = None

# Modelo para respuesta
class IntervencionGrupalResponse(BaseModel):
    id: str
    fecha_solicitud: str
    nombre_docente_permanencia: str
    celular_permanencia: str
    correo_permanencia: str
    estudiante_programa_academico_permanencia: str
    tipo_poblacion: str
    nombre_docente_asignatura: str
    celular_docente_asignatura: str
    correo_docente_asignatura: str
    estudiante_programa_academico_docente_asignatura: str
    asignatura_intervenir: str
    grupo: str
    semestre: str
    numero_estudiantes: str
    tematica_sugerida: Optional[str] = None
    fecha_estudiante_programa_academicoda: str
    hora: str
    aula: str
    bloque: str
    sede: str
    estado: str
    motivo: Optional[str] = None
    efectividad: str
    created_at: datetime
    updated_at: datetime

@router.post("/intervenciones-grupales", 
           summary="Crear una nueva intervención grupal",
           description="Registra una nueva intervención grupal",
           response_model=Dict[str, Any],
           tags=["Intervenciones Grupales"])
async def create_intervencion_grupal(datos: Dict[str, Any]):
    """Crea una nueva intervención grupal."""
    try:
        import re

        # Campos requeridos
        campos_requeridos = [
            "fecha_solicitud", "nombre_docente_permanencia", "celular_permanencia",
            "correo_permanencia", "estudiante_programa_academico_permanencia", "tipo_poblacion",
            "nombre_docente_asignatura", "celular_docente_asignatura", "correo_docente_asignatura",
            "estudiante_programa_academico_docente_asignatura", "asignatura_intervenir",
            "grupo", "semestre", "numero_estudiantes", "fecha_estudiante_programa_academicoda",
            "hora", "aula", "bloque", "sede", "estado"
        ]
        for campo in campos_requeridos:
            if campo not in datos or not str(datos[campo]).strip():
                return error_response(f"El campo '{campo}' es obligatorio.", f"El campo '{campo}' es obligatorio.")

        # Validaciones específicas
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", datos["fecha_solicitud"]):
            return error_response("Formato inválido para 'fecha_solicitud'.", "Debe ser YYYY-MM-DD.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", datos["nombre_docente_permanencia"]):
            return error_response("Nombre de docente de permanencia inválido.", "Debe contener solo letras y espacios.")

        if not re.match(r"^3\d{9}$", datos["celular_permanencia"]):
            return error_response("Celular de permanencia inválido.", "Debe tener 10 dígitos y comenzar por 3.")

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", datos["correo_permanencia"]):
            return error_response("Correo de permanencia inválido.", "Debe ser un correo electrónico válido.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-\(\)]+$", datos["estudiante_programa_academico_permanencia"]):
            return error_response("Programa académico de permanencia inválido.", "Solo letras, espacios y algunos símbolos.")

        if datos["tipo_poblacion"] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            return error_response("Tipo de población inválido.", "Debe ser uno de: a, b, c, d, e, f, g.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", datos["nombre_docente_asignatura"]):
            return error_response("Nombre de docente de asignatura inválido.", "Solo letras y espacios.")

        if not re.match(r"^3\d{9}$", datos["celular_docente_asignatura"]):
            return error_response("Celular de docente de asignatura inválido.", "Debe tener 10 dígitos y comenzar por 3.")

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", datos["correo_docente_asignatura"]):
            return error_response("Correo de docente de asignatura inválido.", "Debe ser un correo electrónico válido.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-\(\)]+$", datos["estudiante_programa_academico_docente_asignatura"]):
            return error_response("Programa académico del docente inválido.", "Solo letras, espacios y algunos símbolos.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", datos["asignatura_intervenir"]):
            return error_response("Asignatura a intervenir inválida.", "Solo letras y espacios.")

        if not re.match(r"^\d{2}:\d{2}$", datos["hora"]):
            return error_response("Formato de hora inválido.", "Debe ser HH:MM.")

        if not datos["aula"].isdigit():
            return error_response("Aula inválida.", "Debe contener solo números.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", datos["bloque"]):
            return error_response("Bloque inválido.", "Solo letras y espacios.")

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", datos["sede"]):
            return error_response("Sede inválida.", "Solo letras y espacios.")

        estado = datos["estado"].strip().lower()
        opciones_estado = ["se hizo", "no se hizo", "en espera", "sin disponibilidad de tallerista"]
        if estado not in opciones_estado:
            return error_response("Estado inválido.", "Debe ser uno de: se hizo, no se hizo, en espera, sin disponibilidad de tallerista.")
        datos["estado"] = estado

        if estado != "se hizo" and (not datos.get("motivo") or not datos["motivo"].strip()):
            return error_response("Motivo requerido.", "Debe especificarse un motivo cuando el estado no es 'se hizo'.")

        # Establecer efectividad por defecto si no se envía
        if "efectividad" not in datos:
            datos["efectividad"] = "Pendiente evaluación" if estado == "se hizo" else "N/A"

        # Timestamps
        now = datetime.utcnow().isoformat()
        datos["created_at"] = now
        datos["updated_at"] = now

        # Insertar en base de datos
        result = supabase.table("intervenciones_grupales").insert(datos).execute()

        if not result.data:
            return error_response("Error al crear la intervención grupal", "No se insertaron datos")

        return success_response(result.data[0], "Intervención grupal creada exitosamente")

    except Exception as e:
        return handle_exception(e, "crear intervención grupal")

