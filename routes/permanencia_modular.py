from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime
import services.Funciones_validar as fv

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
        
        # Preprocesamiento de datos para asegurar compatibilidad
        # Convertir semestre a entero si es posible
        if "semestre" in datos and datos["semestre"] and not isinstance(datos["semestre"], int):
            try:
                datos["semestre"] = int(datos["semestre"])
            except (ValueError, TypeError):
                datos["semestre"] = 1
                print(f"Semestre convertido a valor por defecto: {datos['semestre']}")
        elif "semestre" not in datos or not datos.get("semestre"):
            datos["semestre"] = 1
            print(f"Semestre establecido a valor por defecto: {datos['semestre']}")
        
        # Convertir estrato a entero si es posible
        if "estrato" in datos and datos["estrato"] and not isinstance(datos["estrato"], int):
            try:
                datos["estrato"] = int(datos["estrato"])
            except (ValueError, TypeError):
                datos["estrato"] = 1
                print(f"Estrato convertido a valor por defecto: {datos['estrato']}")
        elif "estrato" not in datos or not datos.get("estrato"):
            datos["estrato"] = 1
            print(f"Estrato establecido a valor por defecto: {datos['estrato']}")
        
        # Establecer valores por defecto para campos obligatorios
        if "riesgo_desercion" not in datos or not datos.get("riesgo_desercion"):
            datos["riesgo_desercion"] = "Bajo"
            print(f"Riesgo deserción establecido a valor por defecto: {datos['riesgo_desercion']}")
            
        if "nivel_riesgo" not in datos or not datos.get("nivel_riesgo"):
            datos["nivel_riesgo"] = "Bajo"
            print(f"Nivel riesgo establecido a valor por defecto: {datos['nivel_riesgo']}")
            
        if "requiere_tutoria" not in datos:
            datos["requiere_tutoria"] = True
            print(f"Requiere tutoría establecido a valor por defecto: {datos['requiere_tutoria']}")
            
        if "fecha_asignacion" not in datos or not datos.get("fecha_asignacion"):
            from datetime import datetime
            datos["fecha_asignacion"] = datetime.now().strftime('%Y-%m-%d')
            print(f"Fecha asignación establecida a valor por defecto: {datos['fecha_asignacion']}")
        
        # Validación flexible - solo validamos si hay errores críticos
        errores_criticos = {}
        if not datos.get("numero_documento"):
            errores_criticos["numero_documento"] = "El número de documento es obligatorio"
        if not datos.get("nombres"):
            errores_criticos["nombres"] = "El nombre es obligatorio"
        if not datos.get("apellidos"):
            errores_criticos["apellidos"] = "Los apellidos son obligatorios"
        if not datos.get("correo"):
            errores_criticos["correo"] = "El correo es obligatorio"
        if not datos.get("programa_academico"):
            errores_criticos["programa_academico"] = "El programa académico es obligatorio"
            
        if errores_criticos:
            return error_response("Faltan datos obligatorios", errores_criticos)

        # Crear tutoría
        result = service.create_tutoria(datos)
        
        return success_response(result, "Tutoría académica registrada exitosamente")
    except Exception as e:
        print(f"Error detallado al crear tutoría: {str(e)}")
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
        
        errores = fv.validar_pops(datos)
        if errores:
            return error_response("Datos inválidos", errores)

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
        
        errores = fv.validar_povau(datos)
        if errores:
            return error_response("Datos inválidos", errores)

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
        
        errores = fv.validar_comedor_universitario(datos)
        if errores:
            return error_response("Datos inválidos", errores)
        
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
        
        errores = fv.validar_apoyo_socioeconomico(datos)
        if errores:
            return error_response("Datos inválidos", errores)

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
        errores = fv.validar_taller_habilidades(datos)
        if errores:
            return error_response("Datos inválidos", errores)

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
        
        # Preprocesamiento de datos para asegurar compatibilidad
        # Convertir semestre a entero si es posible
        if "semestre" in datos and datos["semestre"] and not isinstance(datos["semestre"], int):
            try:
                datos["semestre"] = int(datos["semestre"])
            except (ValueError, TypeError):
                datos["semestre"] = 1
                print(f"Semestre convertido a valor por defecto: {datos['semestre']}")
        elif "semestre" not in datos or not datos.get("semestre"):
            datos["semestre"] = 1
            print(f"Semestre establecido a valor por defecto: {datos['semestre']}")
        
        # Convertir estrato a entero si es posible
        if "estrato" in datos and datos["estrato"] and not isinstance(datos["estrato"], int):
            try:
                datos["estrato"] = int(datos["estrato"])
            except (ValueError, TypeError):
                datos["estrato"] = 1
                print(f"Estrato convertido a valor por defecto: {datos['estrato']}")
        elif "estrato" not in datos or not datos.get("estrato"):
            datos["estrato"] = 1
            print(f"Estrato establecido a valor por defecto: {datos['estrato']}")
        
        # Establecer valores por defecto para campos obligatorios
        if "riesgo_desercion" not in datos or not datos.get("riesgo_desercion"):
            datos["riesgo_desercion"] = "Bajo"
            print(f"Riesgo deserción establecido a valor por defecto: {datos['riesgo_desercion']}")
            
        if "fecha_seguimiento" not in datos or not datos.get("fecha_seguimiento"):
            from datetime import datetime
            datos["fecha_seguimiento"] = datetime.now().strftime('%Y-%m-%d')
            print(f"Fecha seguimiento establecida a valor por defecto: {datos['fecha_seguimiento']}")
            
        if "estado_participacion" not in datos or not datos.get("estado_participacion"):
            datos["estado_participacion"] = "Activo"
            print(f"Estado participación establecido a valor por defecto: {datos['estado_participacion']}")
        
        # Validación flexible - solo validamos si hay errores críticos
        errores_criticos = {}
        if not datos.get("numero_documento"):
            errores_criticos["numero_documento"] = "El número de documento es obligatorio"
        if not datos.get("nombres"):
            errores_criticos["nombres"] = "El nombre es obligatorio"
        if not datos.get("apellidos"):
            errores_criticos["apellidos"] = "Los apellidos son obligatorios"
        if not datos.get("correo"):
            errores_criticos["correo"] = "El correo es obligatorio"
        if not datos.get("programa_academico"):
            errores_criticos["programa_academico"] = "El programa académico es obligatorio"
            
        if errores_criticos:
            return error_response("Faltan datos obligatorios", errores_criticos)
        
        # Crear seguimiento
        result = service.create_seguimiento(datos)
        
        return success_response(result, "Seguimiento académico registrado exitosamente")
    except Exception as e:
        print(f"Error detallado al crear seguimiento: {str(e)}")
        return handle_exception(e, "crear seguimiento académico")
