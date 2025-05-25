from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from config import supabase

router = APIRouter()

# Modelos para los diferentes servicios de permanencia

class EstudianteBase(BaseModel):
    """Modelo base para datos de estudiante en servicios de permanencia."""
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class TutoriaAcademica(BaseModel):
    """Modelo para el servicio de Tutoría Académica (POA)."""
    estudiante_id: Optional[uuid.UUID] = None
    nivel_riesgo: str
    requiere_tutoria: bool
    fecha_asignacion: str
    acciones_apoyo: Optional[str] = None
    
class AsesoriaPsicologica(BaseModel):
    """Modelo para el servicio de Asesoría Psicológica (POPS)."""
    estudiante_id: Optional[uuid.UUID] = None
    motivo_intervencion: str
    tipo_intervencion: str
    fecha_atencion: str
    seguimiento: Optional[str] = None

class OrientacionVocacional(BaseModel):
    """Modelo para el servicio de Orientación Vocacional (POVAU)."""
    estudiante_id: Optional[uuid.UUID] = None
    tipo_participante: str
    riesgo_spadies: str
    fecha_ingreso_programa: str
    observaciones: Optional[str] = None

class ComedorUniversitario(BaseModel):
    """Modelo para el servicio de Comedor Universitario."""
    estudiante_id: Optional[uuid.UUID] = None
    condicion_socioeconomica: str
    fecha_solicitud: str
    aprobado: bool
    tipo_comida: str
    raciones_asignadas: int
    observaciones: Optional[str] = None

class ApoyoSocioeconomico(BaseModel):
    """Modelo para el servicio de Apoyo Socioeconómico."""
    estudiante_id: Optional[uuid.UUID] = None
    tipo_vulnerabilidad: Optional[str] = None
    observaciones: Optional[str] = None

class TallerHabilidades(BaseModel):
    """Modelo para el servicio de Talleres de Habilidades."""
    estudiante_id: Optional[uuid.UUID] = None
    nombre_taller: str
    fecha_taller: str
    observaciones: Optional[str] = None

class SeguimientoAcademico(BaseModel):
    """Modelo para el servicio de Seguimiento Académico."""
    estudiante_id: Optional[uuid.UUID] = None
    estado_participacion: str
    observaciones_permanencia: str

# Función auxiliar para buscar o crear un estudiante
async def buscar_o_crear_estudiante(datos_estudiante: Dict[str, Any]) -> str:
    """
    Busca un estudiante por número de documento o crea uno nuevo si no existe.
    Retorna el ID del estudiante.
    """
    try:
        # Verificar que tenemos los datos necesarios
        if not datos_estudiante.get("numero_documento"):
            raise ValueError("El número de documento es obligatorio")
            
        if not datos_estudiante.get("nombres") or not datos_estudiante.get("apellidos"):
            raise ValueError("Los nombres y apellidos son obligatorios")
            
        if not datos_estudiante.get("tipo_documento"):
            raise ValueError("El tipo de documento es obligatorio")
            
        if not datos_estudiante.get("correo"):
            raise ValueError("El correo es obligatorio")
            
        if not datos_estudiante.get("programa_academico"):
            raise ValueError("El programa académico es obligatorio")
            
        if not datos_estudiante.get("semestre"):
            raise ValueError("El semestre es obligatorio")
            
        # Buscar estudiante por número de documento
        print(f"Buscando estudiante con documento: {datos_estudiante['numero_documento']}")
        estudiante = supabase.table("estudiantes").select("id").eq("documento", datos_estudiante["numero_documento"]).execute()
        print(f"Resultado de búsqueda: {estudiante.data}")
        
        if estudiante.data and len(estudiante.data) > 0:
            # Estudiante encontrado, retornar su ID
            print(f"Estudiante encontrado con ID: {estudiante.data[0]['id']}")
            return estudiante.data[0]["id"]
        else:
            # Crear nuevo estudiante
            nuevo_estudiante = {
                "documento": datos_estudiante["numero_documento"],
                "tipo_documento": datos_estudiante["tipo_documento"],
                "nombres": datos_estudiante["nombres"],
                "apellidos": datos_estudiante["apellidos"],
                "correo": datos_estudiante["correo"],
                "telefono": datos_estudiante.get("telefono") or "",
                "direccion": datos_estudiante.get("direccion") or "",
                "programa_academico": datos_estudiante["programa_academico"],
                "semestre": datos_estudiante["semestre"],
                "estrato": datos_estudiante.get("estrato") or 1,  # Valor por defecto
                "created_at": datetime.now().isoformat()
            }
            
            print(f"Creando nuevo estudiante: {nuevo_estudiante}")
            response = supabase.table("estudiantes").insert(nuevo_estudiante).execute()
            print(f"Respuesta de creación: {response.data}")
            
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            else:
                raise ValueError("No se pudo crear el estudiante")
    except Exception as e:
        print(f"Error al buscar o crear estudiante: {e}")
        raise HTTPException(status_code=500, detail=f"Error al buscar o crear estudiante: {str(e)}")

# Endpoints para Tutoría Académica (POA)
@router.get("/tutoria-academica", 
          summary="Obtener todas las tutorías académicas",
          description="Retorna una lista de todas las tutorías académicas registradas",
          response_model=List[Dict[str, Any]])
async def get_tutorias_academicas():
    """Obtiene todas las tutorías académicas."""
    try:
        response = supabase.table("tutorias_academicas").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener tutorías académicas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener tutorías académicas: {str(e)}")

@router.post("/tutoria", 
           summary="Crear una nueva tutoría académica",
           description="Registra una nueva tutoría académica",
           response_model=Dict[str, Any])
async def create_tutoria_academica(datos: Dict[str, Any]):
    """Crea una nueva tutoría académica."""
    try:
        print(f"Recibiendo datos de tutoría: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        print(f"Datos del estudiante: {datos_estudiante}")
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        print(f"ID del estudiante: {estudiante_id}")
        
        # Crear tutoría académica
        tutoria = {
            "estudiante_id": estudiante_id,
            "nivel_riesgo": datos.get("nivel_riesgo"),
            "requiere_tutoria": datos.get("requiere_tutoria", False),
            "fecha_asignacion": datos.get("fecha_asignacion"),  # Ya viene en formato YYYY-MM-DD del input date
            "acciones_apoyo": datos.get("acciones_apoyo") or "",  # Aseguramos que no sea None
            "created_at": datetime.now().isoformat()
        }
        
        # Validar campos requeridos
        if not tutoria["nivel_riesgo"]:
            return {
                "success": False,
                "message": "El nivel de riesgo es obligatorio"
            }
            
        if not tutoria["fecha_asignacion"]:
            return {
                "success": False,
                "message": "La fecha de asignación es obligatoria"
            }
        
        print(f"Insertando tutoría: {tutoria}")
        response = supabase.table("tutorias_academicas").insert(tutoria).execute()
        print(f"Respuesta de Supabase: {response.data}")
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Tutoría académica registrada exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear tutoría académica: {e}")
        return {
            "success": False,
            "error": f"Error al crear tutoría académica: {str(e)}",
            "message": "Hubo un problema al procesar la tutoría académica. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Asesoría Psicológica (POPS)
@router.get("/psicologia", 
          summary="Obtener todas las asesorías psicológicas",
          description="Retorna una lista de todas las asesorías psicológicas registradas",
          response_model=List[Dict[str, Any]])
async def get_asesorias_psicologicas():
    """Obtiene todas las asesorías psicológicas."""
    try:
        response = supabase.table("asesorias_psicologicas").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener asesorías psicológicas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener asesorías psicológicas: {str(e)}")

@router.post("/psicologia", 
           summary="Crear una nueva asesoría psicológica",
           description="Registra una nueva asesoría psicológica",
           response_model=Dict[str, Any])
async def create_asesoria_psicologica(datos: Dict[str, Any]):
    """Crea una nueva asesoría psicológica."""
    try:
        print(f"Recibiendo datos de asesoría psicológica: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear asesoría psicológica
        asesoria = {
            "estudiante_id": estudiante_id,
            "motivo_intervencion": datos.get("motivo_intervencion"),
            "tipo_intervencion": datos.get("tipo_intervencion"),
            "fecha_atencion": datos.get("fecha_atencion"),  # Ya viene en formato YYYY-MM-DD del input date
            "seguimiento": datos.get("seguimiento"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando asesoría psicológica: {asesoria}")
        response = supabase.table("asesorias_psicologicas").insert(asesoria).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Asesoría psicológica registrada exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear asesoría psicológica: {e}")
        return {
            "success": False,
            "error": f"Error al crear asesoría psicológica: {str(e)}",
            "message": "Hubo un problema al procesar la asesoría psicológica. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Orientación Vocacional (POVAU)
@router.get("/vocacional", 
          summary="Obtener todas las orientaciones vocacionales",
          description="Retorna una lista de todas las orientaciones vocacionales registradas",
          response_model=List[Dict[str, Any]])
async def get_orientaciones_vocacionales():
    """Obtiene todas las orientaciones vocacionales."""
    try:
        response = supabase.table("orientaciones_vocacionales").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener orientaciones vocacionales: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener orientaciones vocacionales: {str(e)}")

@router.post("/vocacional", 
           summary="Crear una nueva orientación vocacional",
           description="Registra una nueva orientación vocacional",
           response_model=Dict[str, Any])
async def create_orientacion_vocacional(datos: Dict[str, Any]):
    """Crea una nueva orientación vocacional."""
    try:
        print(f"Recibiendo datos de orientación vocacional: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear orientación vocacional
        orientacion = {
            "estudiante_id": estudiante_id,
            "tipo_participante": datos.get("tipo_participante"),
            "riesgo_spadies": datos.get("riesgo_spadies"),
            "fecha_ingreso_programa": datos.get("fecha_ingreso_programa"),  # Ya viene en formato YYYY-MM-DD del input date
            "observaciones": datos.get("observaciones"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando orientación vocacional: {orientacion}")
        response = supabase.table("orientaciones_vocacionales").insert(orientacion).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Orientación vocacional registrada exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear orientación vocacional: {e}")
        return {
            "success": False,
            "error": f"Error al crear orientación vocacional: {str(e)}",
            "message": "Hubo un problema al procesar la orientación vocacional. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Comedor Universitario
@router.get("/comedor", 
          summary="Obtener todos los registros de comedor universitario",
          description="Retorna una lista de todos los registros de comedor universitario",
          response_model=List[Dict[str, Any]])
async def get_comedores_universitarios():
    """Obtiene todos los registros de comedor universitario."""
    try:
        response = supabase.table("comedores_universitarios").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener registros de comedor universitario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener registros de comedor universitario: {str(e)}")

@router.post("/comedor", 
           summary="Crear un nuevo registro de comedor universitario",
           description="Registra un nuevo beneficiario de comedor universitario",
           response_model=Dict[str, Any])
async def create_comedor_universitario(datos: Dict[str, Any]):
    """Crea un nuevo registro de comedor universitario."""
    try:
        print(f"Recibiendo datos de comedor universitario: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear registro de comedor universitario
        comedor = {
            "estudiante_id": estudiante_id,
            "condicion_socioeconomica": datos.get("condicion_socioeconomica"),
            "fecha_solicitud": datos.get("fecha_solicitud"),  # Ya viene en formato YYYY-MM-DD del input date
            "aprobado": datos.get("aprobado", False),
            "tipo_comida": datos.get("tipo_comida"),
            "raciones_asignadas": datos.get("raciones_asignadas"),
            "observaciones": datos.get("observaciones"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando registro de comedor universitario: {comedor}")
        response = supabase.table("comedores_universitarios").insert(comedor).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Registro de comedor universitario creado exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear registro de comedor universitario: {e}")
        return {
            "success": False,
            "error": f"Error al crear registro de comedor universitario: {str(e)}",
            "message": "Hubo un problema al procesar el registro de comedor universitario. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Apoyos Socioeconómicos
@router.get("/socioeconomico", 
          summary="Obtener todos los apoyos socioeconómicos",
          description="Retorna una lista de todos los apoyos socioeconómicos registrados",
          response_model=List[Dict[str, Any]])
async def get_apoyos_socioeconomicos():
    """Obtiene todos los apoyos socioeconómicos."""
    try:
        response = supabase.table("apoyos_socioeconomicos").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener apoyos socioeconómicos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener apoyos socioeconómicos: {str(e)}")

@router.post("/socioeconomico", 
           summary="Crear un nuevo apoyo socioeconómico",
           description="Registra un nuevo apoyo socioeconómico",
           response_model=Dict[str, Any])
async def create_apoyo_socioeconomico(datos: Dict[str, Any]):
    """Crea un nuevo apoyo socioeconómico."""
    try:
        print(f"Recibiendo datos de apoyo socioeconómico: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear apoyo socioeconómico
        apoyo = {
            "estudiante_id": estudiante_id,
            "tipo_vulnerabilidad": datos.get("tipo_vulnerabilidad"),
            "observaciones": datos.get("observaciones"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando apoyo socioeconómico: {apoyo}")
        response = supabase.table("apoyos_socioeconomicos").insert(apoyo).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Apoyo socioeconómico registrado exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear apoyo socioeconómico: {e}")
        return {
            "success": False,
            "error": f"Error al crear apoyo socioeconómico: {str(e)}",
            "message": "Hubo un problema al procesar el apoyo socioeconómico. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Talleres de Habilidades
@router.get("/talleres", 
          summary="Obtener todos los talleres de habilidades",
          description="Retorna una lista de todos los talleres de habilidades registrados",
          response_model=List[Dict[str, Any]])
async def get_talleres_habilidades():
    """Obtiene todos los talleres de habilidades."""
    try:
        response = supabase.table("talleres_habilidades").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener talleres de habilidades: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener talleres de habilidades: {str(e)}")

@router.post("/talleres", 
           summary="Crear un nuevo taller de habilidades",
           description="Registra un nuevo taller de habilidades",
           response_model=Dict[str, Any])
async def create_taller_habilidades(datos: Dict[str, Any]):
    """Crea un nuevo taller de habilidades."""
    try:
        print(f"Recibiendo datos de taller de habilidades: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear taller de habilidades
        taller = {
            "estudiante_id": estudiante_id,
            "nombre_taller": datos.get("nombre_taller"),
            "fecha_taller": datos.get("fecha_taller"),  # Ya viene en formato YYYY-MM-DD del input date
            "observaciones": datos.get("observaciones"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando taller de habilidades: {taller}")
        response = supabase.table("talleres_habilidades").insert(taller).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Taller de habilidades registrado exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear taller de habilidades: {e}")
        return {
            "success": False,
            "error": f"Error al crear taller de habilidades: {str(e)}",
            "message": "Hubo un problema al procesar el taller de habilidades. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Seguimiento Académico
@router.get("/seguimiento", 
          summary="Obtener todos los seguimientos académicos",
          description="Retorna una lista de todos los seguimientos académicos registrados",
          response_model=List[Dict[str, Any]])
async def get_seguimientos_academicos():
    """Obtiene todos los seguimientos académicos."""
    try:
        response = supabase.table("seguimientos_academicos").select("*, estudiantes(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener seguimientos académicos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener seguimientos académicos: {str(e)}")

@router.post("/seguimiento", 
           summary="Crear un nuevo seguimiento académico",
           description="Registra un nuevo seguimiento académico",
           response_model=Dict[str, Any])
async def create_seguimiento_academico(datos: Dict[str, Any]):
    """Crea un nuevo seguimiento académico."""
    try:
        print(f"Recibiendo datos de seguimiento académico: {datos}")
        
        # Extraer datos del estudiante
        datos_estudiante = {
            "tipo_documento": datos.get("tipo_documento"),
            "numero_documento": datos.get("numero_documento"),
            "nombres": datos.get("nombres"),
            "apellidos": datos.get("apellidos"),
            "correo": datos.get("correo"),
            "telefono": datos.get("telefono"),
            "direccion": datos.get("direccion"),
            "programa_academico": datos.get("programa_academico"),
            "semestre": datos.get("semestre"),
            "estrato": datos.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = await buscar_o_crear_estudiante(datos_estudiante)
        
        # Crear seguimiento académico
        seguimiento = {
            "estudiante_id": estudiante_id,
            "estado_participacion": datos.get("estado_participacion"),
            "observaciones_permanencia": datos.get("observaciones_permanencia"),
            "created_at": datetime.now().isoformat()
        }
        
        print(f"Insertando seguimiento académico: {seguimiento}")
        response = supabase.table("seguimientos_academicos").insert(seguimiento).execute()
        
        # Retornar respuesta con datos combinados
        result = response.data[0] if response.data else {}
        result["estudiante"] = datos_estudiante
        
        return {
            "success": True,
            "message": "Seguimiento académico registrado exitosamente",
            "data": result
        }
    except Exception as e:
        print(f"Error al crear seguimiento académico: {e}")
        return {
            "success": False,
            "error": f"Error al crear seguimiento académico: {str(e)}",
            "message": "Hubo un problema al procesar el seguimiento académico. Por favor, verifique los campos e intente nuevamente."
        }
