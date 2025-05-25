from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.servicios_service import ServiciosService
from models.servicios import (
    ServicioCreate, ServicioResponse, ServicioUpdate,
    AsistenciaBase, AsistenciaCreate, AsistenciaResponse
)
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()
service = ServiciosService()

# Endpoints para Servicios
@router.get("/servicios", 
          summary="Obtener todos los servicios",
          description="Retorna una lista de todos los servicios registrados",
          response_model=Dict[str, Any],
          tags=["Servicios"])
async def get_servicios():
    """Obtiene todos los servicios."""
    try:
        servicios = service.get_all_servicios()
        return success_response(servicios, "Servicios obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener servicios")

@router.get("/servicios/{id}", 
          summary="Obtener un servicio por ID",
          description="Retorna un servicio específico según su ID",
          response_model=Dict[str, Any],
          tags=["Servicios"])
async def get_servicio(id: str):
    """Obtiene un servicio por su ID."""
    try:
        servicio = service.get_servicio_by_id(id)
        if not servicio:
            return error_response(f"Servicio con ID {id} no encontrado", "Servicio no encontrado", 404)
        
        return success_response(servicio, "Servicio obtenido exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener servicio")

@router.post("/servicios", 
           summary="Crear un nuevo servicio",
           description="Registra un nuevo servicio",
           response_model=Dict[str, Any],
           tags=["Servicios"])
async def create_servicio(datos: Dict[str, Any]):
    """Crea un nuevo servicio."""
    try:
        # Validar campos requeridos
        if not datos.get("nombre"):
            return error_response("El nombre es obligatorio", "El nombre es obligatorio")
            
        if not datos.get("descripcion"):
            return error_response("La descripción es obligatoria", "La descripción es obligatoria")
            
        if not datos.get("tipo"):
            return error_response("El tipo es obligatorio", "El tipo es obligatorio")
        
        # Crear servicio
        result = service.create_servicio(datos)
        
        return success_response(result, "Servicio registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear servicio")

@router.put("/servicios/{id}", 
          summary="Actualizar un servicio",
          description="Actualiza los datos de un servicio existente",
          response_model=Dict[str, Any],
          tags=["Servicios"])
async def update_servicio(id: str, datos: Dict[str, Any]):
    """Actualiza un servicio existente."""
    try:
        # Verificar si el servicio existe
        servicio_existente = service.get_servicio_by_id(id)
        if not servicio_existente:
            return error_response(f"Servicio con ID {id} no encontrado", "Servicio no encontrado", 404)
        
        # Actualizar servicio
        result = service.update_servicio(id, datos)
        
        return success_response(result, "Servicio actualizado exitosamente")
    except Exception as e:
        return handle_exception(e, "actualizar servicio")

@router.delete("/servicios/{id}", 
             summary="Eliminar un servicio",
             description="Elimina un servicio existente",
             response_model=Dict[str, Any],
             tags=["Servicios"])
async def delete_servicio(id: str):
    """Elimina un servicio existente."""
    try:
        # Verificar si el servicio existe
        servicio_existente = service.get_servicio_by_id(id)
        if not servicio_existente:
            return error_response(f"Servicio con ID {id} no encontrado", "Servicio no encontrado", 404)
        
        # Eliminar servicio
        result = service.delete_servicio(id)
        
        return success_response(result, "Servicio eliminado exitosamente")
    except Exception as e:
        return handle_exception(e, "eliminar servicio")

@router.get("/servicios/tipo/{tipo}", 
          summary="Buscar servicios por tipo",
          description="Busca servicios por tipo",
          response_model=Dict[str, Any],
          tags=["Servicios"])
async def get_servicios_by_tipo(tipo: str):
    """Busca servicios por tipo."""
    try:
        servicios = service.get_servicios_by_tipo(tipo)
        return success_response(servicios, "Servicios encontrados exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar servicios por tipo")

@router.get("/servicios/activos", 
          summary="Obtener servicios activos",
          description="Retorna una lista de todos los servicios activos",
          response_model=Dict[str, Any],
          tags=["Servicios"])
async def get_servicios_activos():
    """Obtiene todos los servicios activos."""
    try:
        servicios = service.get_servicios_activos()
        return success_response(servicios, "Servicios activos obtenidos exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener servicios activos")

# Endpoints para Asistencias
@router.get("/asistencias", 
          summary="Obtener todas las asistencias",
          description="Retorna una lista de todas las asistencias registradas",
          response_model=Dict[str, Any],
          tags=["Asistencias"])
async def get_asistencias():
    """Obtiene todas las asistencias."""
    try:
        asistencias = service.asistencias_data.get_all()
        return success_response(asistencias, "Asistencias obtenidas exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener asistencias")

@router.get("/asistencias/{id}", 
          summary="Obtener una asistencia por ID",
          description="Retorna una asistencia específica según su ID",
          response_model=Dict[str, Any],
          tags=["Asistencias"])
async def get_asistencia(id: str):
    """Obtiene una asistencia por su ID."""
    try:
        asistencia = service.asistencias_data.get_by_id(id)
        if not asistencia:
            return error_response(f"Asistencia con ID {id} no encontrada", "Asistencia no encontrada", 404)
        
        return success_response(asistencia, "Asistencia obtenida exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener asistencia")

@router.post("/asistencias", 
           summary="Crear una nueva asistencia",
           description="Registra una nueva asistencia",
           response_model=Dict[str, Any],
           tags=["Asistencias"])
async def create_asistencia(datos: Dict[str, Any]):
    """Crea una nueva asistencia."""
    try:
        # Validar campos requeridos
        if not datos.get("estudiante_id"):
            return error_response("El ID del estudiante es obligatorio", "El ID del estudiante es obligatorio")
            
        if not datos.get("servicio_id"):
            return error_response("El ID del servicio es obligatorio", "El ID del servicio es obligatorio")
            
        if not datos.get("fecha"):
            return error_response("La fecha es obligatoria", "La fecha es obligatoria")
        
        # Crear asistencia
        result = service.create_asistencia(datos)
        
        return success_response(result, "Asistencia registrada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear asistencia")

@router.get("/asistencias/estudiante/{estudiante_id}", 
          summary="Buscar asistencias por estudiante",
          description="Busca asistencias por estudiante",
          response_model=Dict[str, Any],
          tags=["Asistencias"])
async def get_asistencias_by_estudiante(estudiante_id: str):
    """Busca asistencias por estudiante."""
    try:
        asistencias = service.get_asistencias_by_estudiante(estudiante_id)
        return success_response(asistencias, "Asistencias encontradas exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar asistencias por estudiante")

@router.get("/asistencias/servicio/{servicio_id}", 
          summary="Buscar asistencias por servicio",
          description="Busca asistencias por servicio",
          response_model=Dict[str, Any],
          tags=["Asistencias"])
async def get_asistencias_by_servicio(servicio_id: str):
    """Busca asistencias por servicio."""
    try:
        asistencias = service.get_asistencias_by_servicio(servicio_id)
        return success_response(asistencias, "Asistencias encontradas exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar asistencias por servicio")

@router.get("/asistencias/fecha", 
          summary="Buscar asistencias por rango de fechas",
          description="Busca asistencias por rango de fechas",
          response_model=Dict[str, Any],
          tags=["Asistencias"])
async def get_asistencias_by_fecha(fecha_inicio: str, fecha_fin: str):
    """Busca asistencias por rango de fechas."""
    try:
        asistencias = service.get_asistencias_by_fecha(fecha_inicio, fecha_fin)
        return success_response(asistencias, "Asistencias encontradas exitosamente")
    except Exception as e:
        return handle_exception(e, "buscar asistencias por fecha")

# Endpoints para Software Solicitudes
@router.get("/software-solicitudes", 
          summary="Obtener todas las solicitudes de software",
          description="Retorna una lista de todas las solicitudes de software registradas",
          response_model=List[Dict[str, Any]],
          tags=["Software Solicitudes"])
async def get_software_solicitudes():
    """Obtiene todas las solicitudes de software."""
    try:
        from config import supabase
        response = supabase.table("software_solicitudes").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener solicitudes de software: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes de software: {str(e)}")

@router.get("/software-solicitudes/{id}", 
          summary="Obtener una solicitud de software por ID",
          description="Retorna una solicitud de software específica según su ID",
          response_model=Dict[str, Any],
          tags=["Software Solicitudes"])
async def get_software_solicitud(id: str):
    """Obtiene una solicitud de software por su ID."""
    try:
        from config import supabase
        response = supabase.table("software_solicitudes").select("*").eq("id", id).execute()
        if not response.data:
            return error_response(f"Solicitud de software con ID {id} no encontrada", "Solicitud no encontrada", 404)
        
        return success_response(response.data[0], "Solicitud de software obtenida exitosamente")
    except Exception as e:
        return handle_exception(e, "obtener solicitud de software")

@router.post("/software-solicitudes", 
           summary="Crear una nueva solicitud de software",
           description="Registra una nueva solicitud de software",
           response_model=Dict[str, Any],
           tags=["Software Solicitudes"])
async def create_software_solicitud(datos: Dict[str, Any]):
    """Crea una nueva solicitud de software."""
    try:
        from config import supabase
        
        # Validar campos requeridos
        if not datos.get("nombre_software"):
            return error_response("El nombre del software es obligatorio", "El nombre del software es obligatorio")
            
        if not datos.get("descripcion"):
            return error_response("La descripción es obligatoria", "La descripción es obligatoria")
            
        if not datos.get("justificacion"):
            return error_response("La justificación es obligatoria", "La justificación es obligatoria")
        
        # Añadir timestamps
        datos["created_at"] = datetime.now().isoformat()
        datos["updated_at"] = datetime.now().isoformat()
        
        # Crear solicitud
        response = supabase.table("software_solicitudes").insert(datos).execute()
        
        return success_response(response.data[0], "Solicitud de software registrada exitosamente")
    except Exception as e:
        return handle_exception(e, "crear solicitud de software")

@router.put("/software-solicitudes/{id}", 
          summary="Actualizar una solicitud de software",
          description="Actualiza los datos de una solicitud de software existente",
          response_model=Dict[str, Any],
          tags=["Software Solicitudes"])
async def update_software_solicitud(id: str, datos: Dict[str, Any]):
    """Actualiza una solicitud de software existente."""
    try:
        from config import supabase
        
        # Verificar si la solicitud existe
        check_response = supabase.table("software_solicitudes").select("*").eq("id", id).execute()
        if not check_response.data:
            return error_response(f"Solicitud de software con ID {id} no encontrada", "Solicitud no encontrada", 404)
        
        # Actualizar timestamp
        datos["updated_at"] = datetime.now().isoformat()
        
        # Actualizar solicitud
        response = supabase.table("software_solicitudes").update(datos).eq("id", id).execute()
        
        return success_response(response.data[0], "Solicitud de software actualizada exitosamente")
    except Exception as e:
        return handle_exception(e, "actualizar solicitud de software")

@router.delete("/software-solicitudes/{id}", 
             summary="Eliminar una solicitud de software",
             description="Elimina una solicitud de software existente",
             response_model=Dict[str, Any],
             tags=["Software Solicitudes"])
async def delete_software_solicitud(id: str):
    """Elimina una solicitud de software existente."""
    try:
        from config import supabase
        
        # Verificar si la solicitud existe
        check_response = supabase.table("software_solicitudes").select("*").eq("id", id).execute()
        if not check_response.data:
            return error_response(f"Solicitud de software con ID {id} no encontrada", "Solicitud no encontrada", 404)
        
        # Eliminar solicitud
        response = supabase.table("software_solicitudes").delete().eq("id", id).execute()
        
        return success_response({"id": id}, "Solicitud de software eliminada exitosamente")
    except Exception as e:
        return handle_exception(e, "eliminar solicitud de software")

# Endpoints para Software Estudiantes
@router.get("/software-estudiantes", 
          summary="Obtener todos los estudiantes de software",
          description="Retorna una lista de todos los estudiantes de software registrados",
          response_model=List[Dict[str, Any]],
          tags=["Software Estudiantes"])
async def get_software_estudiantes():
    """Obtiene todos los estudiantes de software."""
    try:
        from config import supabase
        response = supabase.table("software_estudiantes").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener estudiantes de software: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estudiantes de software: {str(e)}")

@router.post("/software-estudiantes", 
           summary="Crear un nuevo estudiante de software",
           description="Registra un nuevo estudiante de software",
           response_model=Dict[str, Any],
           tags=["Software Estudiantes"])
async def create_software_estudiante(datos: Dict[str, Any]):
    """Crea un nuevo estudiante de software."""
    try:
        from config import supabase
        
        # Validar campos requeridos
        if not datos.get("nombre"):
            return error_response("El nombre es obligatorio", "El nombre es obligatorio")
            
        if not datos.get("apellido"):
            return error_response("El apellido es obligatorio", "El apellido es obligatorio")
            
        if not datos.get("documento"):
            return error_response("El documento es obligatorio", "El documento es obligatorio")
            
        if not datos.get("programa"):
            return error_response("El programa es obligatorio", "El programa es obligatorio")
        
        # Añadir timestamps
        datos["created_at"] = datetime.now().isoformat()
        datos["updated_at"] = datetime.now().isoformat()
        
        # Crear estudiante
        response = supabase.table("software_estudiantes").insert(datos).execute()
        
        return success_response(response.data[0], "Estudiante de software registrado exitosamente")
    except Exception as e:
        return handle_exception(e, "crear estudiante de software")

# Endpoints para Asistencias a Actividades
@router.get("/asistencias-actividades", 
          summary="Obtener todas las asistencias a actividades",
          description="Retorna una lista de todas las asistencias a actividades registradas",
          response_model=List[Dict[str, Any]],
          tags=["Asistencias a Actividades"])
async def get_asistencias_actividades():
    """Obtiene todas las asistencias a actividades."""
    try:
        from config import supabase
        response = supabase.table("asistencias_actividades").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener asistencias a actividades: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener asistencias a actividades: {str(e)}")

@router.post("/asistencias-actividades", 
           summary="Crear una nueva asistencia a actividad",
           description="Registra una nueva asistencia a actividad",
           response_model=Dict[str, Any],
           tags=["Asistencias a Actividades"])
async def create_asistencia_actividad(asistencia: Dict[str, Any]):
    """Crea una nueva asistencia a actividad."""
    try:
        from config import supabase
        
        # Manejar el campo estudiante_programa_academico_academico
        if "estudiante_programa_academico_academico" in asistencia:
            # Asegurarse de que también exista el campo estudiante_programa_academico
            asistencia["estudiante_programa_academico"] = asistencia["estudiante_programa_academico_academico"]
        
        # Buscar estudiante por número de documento si está disponible
        if "numero_documento" in asistencia and "estudiante_id" not in asistencia:
            estudiante = supabase.table("estudiantes").select("id").eq("documento", asistencia["numero_documento"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                asistencia["estudiante_id"] = estudiante.data[0]["id"]
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                asistencia["estudiante_id"] = None
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "estudiante_id", "nombre_estudiante", "numero_documento", 
            "estudiante_programa_academico", "estudiante_programa_academico_academico", 
            "semestre", "nombre_actividad", "modalidad", "tipo_actividad", 
            "fecha_actividad", "hora_inicio", "hora_fin", "modalidad_registro", 
            "observaciones", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        asistencia_filtrada = {k: v for k, v in asistencia.items() if k in campos_validos}
        
        # Añadir timestamps
        if "created_at" not in asistencia_filtrada:
            asistencia_filtrada["created_at"] = datetime.now().isoformat()
        if "updated_at" not in asistencia_filtrada:
            asistencia_filtrada["updated_at"] = datetime.now().isoformat()
        
        # Imprimir para depuración
        print(f"Asistencia original: {asistencia}")
        print(f"Asistencia filtrada: {asistencia_filtrada}")
        
        response = supabase.table("asistencias_actividades").insert(asistencia_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear asistencia a actividad: {e}")
        return {
            "success": False,
            "error": f"Error al crear asistencia a actividad: {str(e)}",
            "message": "Hubo un problema al procesar la asistencia. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Fichas Docente
@router.get("/fichas-docente", 
          summary="Obtener todas las fichas docente",
          description="Retorna una lista de todas las fichas docente registradas",
          response_model=List[Dict[str, Any]],
          tags=["Fichas Docente"])
async def get_fichas_docente():
    """Obtiene todas las fichas docente."""
    try:
        from config import supabase
        response = supabase.table("fichas_docente").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener fichas docente: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener fichas docente: {str(e)}")

@router.post("/fichas-docente", 
           summary="Crear una nueva ficha docente",
           description="Registra una nueva ficha docente",
           response_model=Dict[str, Any],
           tags=["Fichas Docente"])
async def create_ficha_docente(ficha: Dict[str, Any]):
    """Crea una nueva ficha docente."""
    try:
        from config import supabase
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "nombres_apellidos", "documento_identidad", "fecha_nacimiento_dia", 
            "fecha_nacimiento_mes", "fecha_nacimiento_ano", "direccion_residencia", 
            "celular", "correo_institucional", "correo_personal", "preferencia_correo", 
            "facultad", "estudiante_programa_academico", "asignaturas", "creditos_asignaturas", 
            "ciclo_formacion", "pregrado", "especializacion", "maestria", "doctorado", 
            "grupo_investigacion", "cual_grupo", "horas_semanales", "created_at", "updated_at"
        ]
        
        # Añadir timestamps si no están presentes
        if "created_at" not in ficha:
            from datetime import datetime
            ficha["created_at"] = datetime.now().isoformat()
        if "updated_at" not in ficha:
            from datetime import datetime
            ficha["updated_at"] = datetime.now().isoformat()
            
        # Filtrar solo los campos válidos
        ficha_filtrada = {k: v for k, v in ficha.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Ficha original: {ficha}")
        print(f"Ficha filtrada: {ficha_filtrada}")
        
        # Insertar la ficha filtrada
        response = supabase.table("fichas_docente").insert(ficha_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear ficha docente: {e}")
        # Devolver un error más amigable y con información útil
        return {
            "success": False,
            "error": f"Error al crear ficha docente: {str(e)}",
            "message": "Hubo un problema al procesar la ficha docente. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Intervenciones Grupales
@router.get("/intervenciones-grupales", 
          summary="Obtener todas las intervenciones grupales",
          description="Retorna una lista de todas las intervenciones grupales registradas",
          response_model=List[Dict[str, Any]],
          tags=["Intervenciones Grupales"])
async def get_intervenciones_grupales():
    """Obtiene todas las intervenciones grupales."""
    try:
        from config import supabase
        response = supabase.table("intervenciones_grupales").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener intervenciones grupales: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener intervenciones grupales: {str(e)}")

@router.post("/intervenciones-grupales", 
           summary="Crear una nueva intervención grupal",
           description="Registra una nueva intervención grupal",
           response_model=Dict[str, Any],
           tags=["Intervenciones Grupales"])
async def create_intervencion_grupal(intervencion: Dict[str, Any]):
    """Crea una nueva intervención grupal."""
    try:
        from config import supabase
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "fecha_solicitud", "nombre_docente_permanencia", "celular_permanencia", 
            "correo_permanencia", "estudiante_programa_academico_permanencia", "tipo_poblacion", 
            "nombre_docente_asignatura", "celular_docente_asignatura", "correo_docente_asignatura", 
            "estudiante_programa_academico_docente_asignatura", "asignatura_intervenir", "grupo", 
            "semestre", "numero_estudiantes", "tematica_sugerida", "fecha_estudiante_programa_academicoda", 
            "hora", "aula", "bloque", "sede", "estado", "created_at", "updated_at"
        ]
        
        # Añadir timestamps si no están presentes
        if "created_at" not in intervencion:
            from datetime import datetime
            intervencion["created_at"] = datetime.now().isoformat()
        if "updated_at" not in intervencion:
            from datetime import datetime
            intervencion["updated_at"] = datetime.now().isoformat()
            
        # Añadir estado por defecto si no está presente
        if "estado" not in intervencion or not intervencion["estado"]:
            intervencion["estado"] = "Pendiente"
            
        # Filtrar solo los campos válidos
        intervencion_filtrada = {k: v for k, v in intervencion.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Intervención original: {intervencion}")
        print(f"Intervención filtrada: {intervencion_filtrada}")
        
        # Insertar la intervención filtrada
        response = supabase.table("intervenciones_grupales").insert(intervencion_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear intervención grupal: {e}")
        # Devolver un error más amigable y con información útil
        return {
            "success": False,
            "error": f"Error al crear intervención grupal: {str(e)}",
            "message": "Hubo un problema al procesar la intervención grupal. Por favor, verifique los campos e intente nuevamente."
        }

# Endpoints para Remisiones Psicológicas
@router.get("/remisiones-psicologicas", 
          summary="Obtener todas las remisiones psicológicas",
          description="Retorna una lista de todas las remisiones psicológicas registradas",
          response_model=List[Dict[str, Any]],
          tags=["Remisiones Psicológicas"])
async def get_remisiones_psicologicas():
    """Obtiene todas las remisiones psicológicas."""
    try:
        from config import supabase
        response = supabase.table("remisiones_psicologicas").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener remisiones psicológicas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener remisiones psicológicas: {str(e)}")

@router.post("/remisiones-psicologicas", 
           summary="Crear una nueva remisión psicológica",
           description="Registra una nueva remisión psicológica",
           response_model=Dict[str, Any],
           tags=["Remisiones Psicológicas"])
async def create_remision_psicologica(remision: Dict[str, Any]):
    """Crea una nueva remisión psicológica."""
    try:
        from config import supabase
        # Manejar el campo estudiante_programa_academico_academico
        if "estudiante_programa_academico_academico" in remision:
            # Asegurarse de que también exista el campo estudiante_programa_academico
            remision["estudiante_programa_academico"] = remision["estudiante_programa_academico_academico"]
        
        # Buscar estudiante por número de documento si está disponible
        if "numero_documento" in remision and "estudiante_id" not in remision:
            estudiante = supabase.table("estudiantes").select("id").eq("documento", remision["numero_documento"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                remision["estudiante_id"] = estudiante.data[0]["id"]
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                remision["estudiante_id"] = None
        
        # Añadir timestamps si no están presentes
        if "created_at" not in remision:
            from datetime import datetime
            remision["created_at"] = datetime.now().isoformat()
        if "updated_at" not in remision:
            from datetime import datetime
            remision["updated_at"] = datetime.now().isoformat()
        
        # Filtrar los campos que existen en la tabla para evitar errores
        campos_validos = [
            "id", "estudiante_id", "nombre_estudiante", "numero_documento", 
            "estudiante_programa_academico", "estudiante_programa_academico_academico", 
            "semestre", "motivo_remision", "docente_remite", "correo_docente", 
            "telefono_docente", "fecha", "hora", "tipo_remision", "observaciones", 
            "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos
        remision_filtrada = {k: v for k, v in remision.items() if k in campos_validos}
        
        # Imprimir para depuración
        print(f"Remisión original: {remision}")
        print(f"Remisión filtrada: {remision_filtrada}")
        
        # Insertar la remisión filtrada
        response = supabase.table("remisiones_psicologicas").insert(remision_filtrada).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error al crear remisión psicológica: {e}")
        # Devolver un error más amigable y con información útil
        return {
            "success": False,
            "error": f"Error al crear remisión psicológica: {str(e)}",
            "message": "Hubo un problema al procesar la remisión psicológica. Por favor, verifique los campos e intente nuevamente."
        }
