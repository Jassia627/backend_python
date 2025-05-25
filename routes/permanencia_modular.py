from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.permanencia_service import PermanenciaService
from models.permanencia import (
    TutoriaAcademicaCreate, TutoriaAcademicaResponse,
    AsesoriaPsicologicaCreate, AsesoriaPsicologicaResponse,
    OrientacionVocacionalCreate, OrientacionVocacionalResponse,
    ComedorUniversitarioCreate, ComedorUniversitarioResponse,
    ApoyoSocioeconomicoCreate, ApoyoSocioeconomicoResponse,
    TallerHabilidadesCreate, TallerHabilidadesResponse,
    SeguimientoAcademicoCreate, SeguimientoAcademicoResponse
)
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = PermanenciaService()

# Endpoints para Tutoría Académica (POA)

@router.get("/tutoria", 
          summary="Obtener todas las tutorías académicas",
          description="Retorna una lista de todas las tutorías académicas registradas",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_tutorias_academicas():
    """Obtiene todas las tutorías académicas."""
    try:
        tutorias = service.get_all_tutorias()
        return success_response(tutorias, "Tutorías académicas obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener tutorías académicas")

@router.post("/tutoria", 
           summary="Crear una nueva tutoría académica",
           description="Registra una nueva tutoría académica",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_tutoria_academica(datos: Dict[str, Any]):
    """Crea una nueva tutoría académica."""
    try:
        print(f"Recibiendo datos de tutoría: {datos}")
        
        # Validar campos requeridos
        if not datos.get("nivel_riesgo"):
            return error_response("El nivel de riesgo es obligatorio", "El nivel de riesgo es obligatorio")
            
        if not datos.get("fecha_asignacion"):
            return error_response("La fecha de asignación es obligatoria", "La fecha de asignación es obligatoria")
        
        # Crear tutoría
        result = service.create_tutoria(datos)
        
        return success_response(result, "Tutoría académica registrada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear tutoría académica")

# Endpoints para Asesoría Psicológica (POPS)

@router.get("/psicologia", 
          summary="Obtener todas las asesorías psicológicas",
          description="Retorna una lista de todas las asesorías psicológicas registradas",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_asesorias_psicologicas():
    """Obtiene todas las asesorías psicológicas."""
    try:
        asesorias = service.get_all_asesorias()
        return success_response(asesorias, "Asesorías psicológicas obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener asesorías psicológicas")

@router.post("/psicologia", 
           summary="Crear una nueva asesoría psicológica",
           description="Registra una nueva asesoría psicológica",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_asesoria_psicologica(datos: Dict[str, Any]):
    """Crea una nueva asesoría psicológica."""
    try:
        print(f"Recibiendo datos de asesoría psicológica: {datos}")
        
        # Validar campos requeridos
        if not datos.get("motivo_intervencion"):
            return error_response("El motivo de intervención es obligatorio", "El motivo de intervención es obligatorio")
            
        if not datos.get("tipo_intervencion"):
            return error_response("El tipo de intervención es obligatorio", "El tipo de intervención es obligatorio")
            
        if not datos.get("fecha_atencion"):
            return error_response("La fecha de atención es obligatoria", "La fecha de atención es obligatoria")
        
        # Crear asesoría
        result = service.create_asesoria(datos)
        
        return success_response(result, "Asesoría psicológica registrada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear asesoría psicológica")

# Endpoints para Orientación Vocacional (POVAU)

@router.get("/vocacional", 
          summary="Obtener todas las orientaciones vocacionales",
          description="Retorna una lista de todas las orientaciones vocacionales registradas",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_orientaciones_vocacionales():
    """Obtiene todas las orientaciones vocacionales."""
    try:
        orientaciones = service.get_all_orientaciones()
        return success_response(orientaciones, "Orientaciones vocacionales obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener orientaciones vocacionales")

@router.post("/vocacional", 
           summary="Crear una nueva orientación vocacional",
           description="Registra una nueva orientación vocacional",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_orientacion_vocacional(datos: Dict[str, Any]):
    """Crea una nueva orientación vocacional."""
    try:
        print(f"Recibiendo datos de orientación vocacional: {datos}")
        
        # Validar campos requeridos
        if not datos.get("tipo_participante"):
            return error_response("El tipo de participante es obligatorio", "El tipo de participante es obligatorio")
            
        if not datos.get("riesgo_spadies"):
            return error_response("El riesgo SPADIES es obligatorio", "El riesgo SPADIES es obligatorio")
            
        if not datos.get("fecha_ingreso_programa"):
            return error_response("La fecha de ingreso al programa es obligatoria", "La fecha de ingreso al programa es obligatoria")
        
        # Crear orientación
        result = service.create_orientacion(datos)
        
        return success_response(result, "Orientación vocacional registrada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear orientación vocacional")

# Endpoints para Comedor Universitario

@router.get("/comedor", 
          summary="Obtener todos los registros de comedor universitario",
          description="Retorna una lista de todos los registros de comedor universitario",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_comedores_universitarios():
    """Obtiene todos los registros de comedor universitario."""
    try:
        comedores = service.get_all_comedores()
        return success_response(comedores, "Registros de comedor universitario obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener registros de comedor universitario")

@router.post("/comedor", 
           summary="Crear un nuevo registro de comedor universitario",
           description="Registra un nuevo beneficiario de comedor universitario",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_comedor_universitario(datos: Dict[str, Any]):
    """Crea un nuevo registro de comedor universitario."""
    try:
        print(f"Recibiendo datos de comedor universitario: {datos}")
        
        # Validar campos requeridos
        if not datos.get("condicion_socioeconomica"):
            return error_response("La condición socioeconómica es obligatoria", "La condición socioeconómica es obligatoria")
            
        if not datos.get("fecha_solicitud"):
            return error_response("La fecha de solicitud es obligatoria", "La fecha de solicitud es obligatoria")
            
        if not datos.get("tipo_comida"):
            return error_response("El tipo de comida es obligatorio", "El tipo de comida es obligatorio")
            
        if not datos.get("raciones_asignadas"):
            return error_response("Las raciones asignadas son obligatorias", "Las raciones asignadas son obligatorias")
        
        # Crear registro de comedor
        result = service.create_comedor(datos)
        
        return success_response(result, "Registro de comedor universitario creado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear registro de comedor universitario")

# Endpoints para Apoyos Socioeconómicos

@router.get("/socioeconomico", 
          summary="Obtener todos los apoyos socioeconómicos",
          description="Retorna una lista de todos los apoyos socioeconómicos registrados",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_apoyos_socioeconomicos():
    """Obtiene todos los apoyos socioeconómicos."""
    try:
        apoyos = service.get_all_apoyos()
        return success_response(apoyos, "Apoyos socioeconómicos obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener apoyos socioeconómicos")

@router.post("/socioeconomico", 
           summary="Crear un nuevo apoyo socioeconómico",
           description="Registra un nuevo apoyo socioeconómico",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_apoyo_socioeconomico(datos: Dict[str, Any]):
    """Crea un nuevo apoyo socioeconómico."""
    try:
        print(f"Recibiendo datos de apoyo socioeconómico: {datos}")
        
        # Validar campos requeridos
        if not datos.get("tipo_vulnerabilidad"):
            return error_response("El tipo de vulnerabilidad es obligatorio", "El tipo de vulnerabilidad es obligatorio")
        
        # Crear apoyo
        result = service.create_apoyo(datos)
        
        return success_response(result, "Apoyo socioeconómico registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear apoyo socioeconómico")

# Endpoints para Talleres de Habilidades

@router.get("/talleres", 
          summary="Obtener todos los talleres de habilidades",
          description="Retorna una lista de todos los talleres de habilidades registrados",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_talleres_habilidades():
    """Obtiene todos los talleres de habilidades."""
    try:
        talleres = service.get_all_talleres()
        return success_response(talleres, "Talleres de habilidades obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener talleres de habilidades")

@router.post("/talleres", 
           summary="Crear un nuevo taller de habilidades",
           description="Registra un nuevo taller de habilidades",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_taller_habilidades(datos: Dict[str, Any]):
    """Crea un nuevo taller de habilidades."""
    try:
        print(f"Recibiendo datos de taller de habilidades: {datos}")
        
        # Validar campos requeridos
        if not datos.get("nombre_taller"):
            return error_response("El nombre del taller es obligatorio", "El nombre del taller es obligatorio")
            
        if not datos.get("fecha_taller"):
            return error_response("La fecha del taller es obligatoria", "La fecha del taller es obligatoria")
        
        # Crear taller
        result = service.create_taller(datos)
        
        return success_response(result, "Taller de habilidades registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear taller de habilidades")

# Endpoints para Seguimiento Académico

@router.get("/seguimiento", 
          summary="Obtener todos los seguimientos académicos",
          description="Retorna una lista de todos los seguimientos académicos registrados",
          response_model=Dict[str, Any],
          tags=["Servicios de Permanencia"])
async def get_seguimientos_academicos():
    """Obtiene todos los seguimientos académicos."""
    try:
        seguimientos = service.get_all_seguimientos()
        return success_response(seguimientos, "Seguimientos académicos obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener seguimientos académicos")

@router.post("/seguimiento", 
           summary="Crear un nuevo seguimiento académico",
           description="Registra un nuevo seguimiento académico",
           response_model=Dict[str, Any],
           tags=["Servicios de Permanencia"])
async def create_seguimiento_academico(datos: Dict[str, Any]):
    """Crea un nuevo seguimiento académico."""
    try:
        print(f"Recibiendo datos de seguimiento académico: {datos}")
        
        # Validar campos requeridos
        if not datos.get("estado_participacion"):
            return error_response("El estado de participación es obligatorio", "El estado de participación es obligatorio")
            
        if not datos.get("observaciones_permanencia"):
            return error_response("Las observaciones de permanencia son obligatorias", "Las observaciones de permanencia son obligatorias")
        
        # Crear seguimiento
        result = service.create_seguimiento(datos)
        
        return success_response(result, "Seguimiento académico registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear seguimiento académico")
