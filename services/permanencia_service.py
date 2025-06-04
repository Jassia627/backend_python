from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from data.permanencia_data import (
    TutoriasAcademicasData,
    AsesoriasPsicologicasData,
    OrientacionesVocacionalesData,
    ComedoresUniversitariosData,
    ApoyosSocioeconomicosData,
    TalleresHabilidadesData,
    SeguimientosAcademicosData
)
from data.estudiantes_data import EstudiantesData
from models.permanencia import (
    TutoriaAcademicaCreate,
    AsesoriaPsicologicaCreate,
    OrientacionVocacionalCreate,
    ComedorUniversitarioCreate,
    ApoyoSocioeconomicoCreate,
    TallerHabilidadesCreate,
    SeguimientoAcademicoCreate
)

class PermanenciaService:
    """Servicio para la gestión de servicios de permanencia."""
    
    def __init__(self):
        """Inicializa el servicio de permanencia."""
        self.tutorias_data = TutoriasAcademicasData()
        self.asesorias_data = AsesoriasPsicologicasData()
        self.orientaciones_data = OrientacionesVocacionalesData()
        self.comedores_data = ComedoresUniversitariosData()
        self.apoyos_data = ApoyosSocioeconomicosData()
        self.talleres_data = TalleresHabilidadesData()
        self.seguimientos_data = SeguimientosAcademicosData()
        self.estudiantes_data = EstudiantesData()
    
    # Métodos para Tutorías Académicas
    
    def get_all_tutorias(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tutorías académicas con datos del estudiante.
        
        Returns:
            Lista de tutorías académicas
        """
        return self.tutorias_data.get_with_estudiante()
    
    def create_tutoria(self, tutoria_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva tutoría académica.
        
        Args:
            tutoria_data: Datos de la tutoría
            
        Returns:
            Tutoría creada
        """
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": tutoria_data.get("numero_documento"),
            "tipo_documento": tutoria_data.get("tipo_documento"),
            "nombres": tutoria_data.get("nombres"),
            "apellidos": tutoria_data.get("apellidos"),
            "correo": tutoria_data.get("correo"),
            "telefono": tutoria_data.get("telefono"),
            "direccion": tutoria_data.get("direccion"),
            "programa_academico": tutoria_data.get("programa_academico"),
            "semestre": tutoria_data.get("semestre"),
            "estrato": tutoria_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear tutoría académica
        tutoria = {
            "estudiante_id": estudiante_id,
            "nivel_riesgo": tutoria_data.get("nivel_riesgo"),
            "requiere_tutoria": tutoria_data.get("requiere_tutoria", False),
            "fecha_asignacion": tutoria_data.get("fecha_asignacion"),
            "acciones_apoyo": tutoria_data.get("acciones_apoyo") or ""
        }
        
        result = self.tutorias_data.create(tutoria)
        result["estudiante"] = datos_estudiante
        
        return result
    
    # Métodos para Asesorías Psicológicas
    
    def get_all_asesorias(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las asesorías psicológicas con datos del estudiante.
        
        Returns:
            Lista de asesorías psicológicas
        """
        return self.asesorias_data.get_with_estudiante()
    
    def create_asesoria(self, asesoria_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva asesoría psicológica.
        
        Args:
            asesoria_data: Datos de la asesoría
            
        Returns:
            Asesoría creada
        """
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": asesoria_data.get("numero_documento"),
            "tipo_documento": asesoria_data.get("tipo_documento"),
            "nombres": asesoria_data.get("nombres"),
            "apellidos": asesoria_data.get("apellidos"),
            "correo": asesoria_data.get("correo"),
            "telefono": asesoria_data.get("telefono"),
            "direccion": asesoria_data.get("direccion"),
            "programa_academico": asesoria_data.get("programa_academico"),
            "semestre": asesoria_data.get("semestre"),
            "estrato": asesoria_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear asesoría psicológica
        asesoria = {
            "estudiante_id": estudiante_id,
            "motivo_intervencion": asesoria_data.get("motivo_intervencion"),
            "tipo_intervencion": asesoria_data.get("tipo_intervencion"),
            "fecha_atencion": asesoria_data.get("fecha_atencion"),
            "seguimiento": asesoria_data.get("seguimiento") or ""
        }
        
        result = self.asesorias_data.create(asesoria)
        result["estudiante"] = datos_estudiante
        
        return result
    
    # Métodos para Orientaciones Vocacionales
    
    def get_all_orientaciones(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las orientaciones vocacionales con datos del estudiante.
        
        Returns:
            Lista de orientaciones vocacionales
        """
        return self.orientaciones_data.get_with_estudiante()
    
    def create_orientacion(self, orientacion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva orientación vocacional.
        
        Args:
            orientacion_data: Datos de la orientación
            
        Returns:
            Orientación creada
        """
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": orientacion_data.get("numero_documento"),
            "tipo_documento": orientacion_data.get("tipo_documento"),
            "nombres": orientacion_data.get("nombres"),
            "apellidos": orientacion_data.get("apellidos"),
            "correo": orientacion_data.get("correo"),
            "telefono": orientacion_data.get("telefono"),
            "direccion": orientacion_data.get("direccion"),
            "programa_academico": orientacion_data.get("programa_academico"),
            "semestre": orientacion_data.get("semestre"),
            "estrato": orientacion_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear orientación vocacional
        orientacion = {
            "estudiante_id": estudiante_id,
            "tipo_participante": orientacion_data.get("tipo_participante"),
            "riesgo_spadies": orientacion_data.get("riesgo_spadies"),
            "fecha_ingreso_programa": orientacion_data.get("fecha_ingreso_programa"),
            "observaciones": orientacion_data.get("observaciones") or ""
        }
        
        result = self.orientaciones_data.create(orientacion)
        result["estudiante"] = datos_estudiante
        
        return result
    
    # Métodos para Comedor Universitario
    
    def get_all_comedores(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de comedor universitario con datos del estudiante.
        
        Returns:
            Lista de registros de comedor universitario
        """
        return self.comedores_data.get_with_estudiante()
    
    def create_comedor(self, comedor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo registro de comedor universitario.
        
        Args:
            comedor_data: Datos del comedor
            
        Returns:
            Registro de comedor creado
        """
        try:
            print(f"Procesando datos para comedor universitario: {comedor_data}")
            
            # Normalizar campos: si existen las versiones con sufijo '1', usarlas como versiones normales
            if "numero_documento1" in comedor_data and "numero_documento" not in comedor_data:
                comedor_data["numero_documento"] = comedor_data["numero_documento1"]
                print(f"Normalizado numero_documento1 a numero_documento: {comedor_data['numero_documento']}")
            
            if "correo1" in comedor_data and "correo" not in comedor_data:
                comedor_data["correo"] = comedor_data["correo1"]
                print(f"Normalizado correo1 a correo: {comedor_data['correo']}")
                
            # Extraer datos del estudiante
            datos_estudiante = {
                "documento": comedor_data.get("numero_documento"),
                "tipo_documento": comedor_data.get("tipo_documento"),
                "nombres": comedor_data.get("nombres"),
                "apellidos": comedor_data.get("apellidos"),
                "correo": comedor_data.get("correo"),
                "telefono": comedor_data.get("telefono"),
                "direccion": comedor_data.get("direccion"),
                "programa_academico": comedor_data.get("programa_academico"),
                "semestre": comedor_data.get("semestre"),
                "estrato": comedor_data.get("estrato"),
                "riesgo_desercion": comedor_data.get("riesgo_desercion")
            }
            
            print(f"Datos de estudiante extraídos: {datos_estudiante}")
            
            # Buscar o crear estudiante
            estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
            print(f"ID de estudiante obtenido: {estudiante_id}")
            
            # Crear registro de comedor universitario
            comedor = {
                "estudiante_id": estudiante_id,
                "condicion_socioeconomica": comedor_data.get("condicion_socioeconomica"),
                "fecha_solicitud": comedor_data.get("fecha_solicitud"),
                "aprobado": comedor_data.get("aprobado", False),
                "tipo_comida": comedor_data.get("tipo_comida", "Almuerzo"),  # Valor por defecto
                "raciones_asignadas": comedor_data.get("raciones_asignadas", 1),  # Valor por defecto
                "observaciones": comedor_data.get("observaciones") or "",
                "tipo_subsidio": comedor_data.get("tipo_subsidio"),
                "periodo_academico": comedor_data.get("periodo_academico"),
                "estrato": comedor_data.get("estrato") or datos_estudiante.get("estrato")
            }
            
            print(f"Datos de comedor a insertar: {comedor}")
            
            # Intentar crear el registro
            try:
                result = self.comedores_data.create(comedor)
                print(f"Resultado de la creación: {result}")
                result["estudiante"] = datos_estudiante
                return result
            except Exception as e:
                print(f"Error al insertar en comedores_universitarios: {str(e)}")
                raise Exception(f"Error al insertar en comedores_universitarios: {str(e)}")
                
        except Exception as e:
            print(f"Error en create_comedor: {str(e)}")
            raise Exception(f"Error en create_comedor: {str(e)}")
    
    # Métodos para Apoyos Socioeconómicos
    
    def get_all_apoyos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los apoyos socioeconómicos con datos del estudiante.
        
        Returns:
            Lista de apoyos socioeconómicos
        """
        return self.apoyos_data.get_with_estudiante()
    
    def create_apoyo(self, apoyo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo apoyo socioeconómico.
        
        Args:
            apoyo_data: Datos del apoyo
            
        Returns:
            Apoyo creado
        """
        # Normalizar campos: si existen las versiones con sufijo '1', usarlas como versiones normales
        if "numero_documento1" in apoyo_data and "numero_documento" not in apoyo_data:
            apoyo_data["numero_documento"] = apoyo_data["numero_documento1"]
        
        if "correo1" in apoyo_data and "correo" not in apoyo_data:
            apoyo_data["correo"] = apoyo_data["correo1"]
            
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": apoyo_data.get("numero_documento"),
            "tipo_documento": apoyo_data.get("tipo_documento"),
            "nombres": apoyo_data.get("nombres"),
            "apellidos": apoyo_data.get("apellidos"),
            "correo": apoyo_data.get("correo"),
            "telefono": apoyo_data.get("telefono"),
            "direccion": apoyo_data.get("direccion"),
            "programa_academico": apoyo_data.get("programa_academico"),
            "semestre": apoyo_data.get("semestre"),
            "estrato": apoyo_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear apoyo socioeconómico
        apoyo = {
            "estudiante_id": estudiante_id,
            "tipo_vulnerabilidad": apoyo_data.get("tipo_vulnerabilidad"),
            "observaciones": apoyo_data.get("observaciones") or ""
        }
        
        result = self.apoyos_data.create(apoyo)
        result["estudiante"] = datos_estudiante
        
        return result
    
    # Métodos para Talleres de Habilidades
    
    def get_all_talleres(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los talleres de habilidades con datos del estudiante.
        
        Returns:
            Lista de talleres de habilidades
        """
        return self.talleres_data.get_with_estudiante()
    
    def create_taller(self, taller_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo taller de habilidades.
        
        Args:
            taller_data: Datos del taller
            
        Returns:
            Taller creado
        """
        # Normalizar campos: si existen las versiones con sufijo '1', usarlas como versiones normales
        if "numero_documento1" in taller_data and "numero_documento" not in taller_data:
            taller_data["numero_documento"] = taller_data["numero_documento1"]
        
        if "correo1" in taller_data and "correo" not in taller_data:
            taller_data["correo"] = taller_data["correo1"]
            
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": taller_data.get("numero_documento"),
            "tipo_documento": taller_data.get("tipo_documento"),
            "nombres": taller_data.get("nombres"),
            "apellidos": taller_data.get("apellidos"),
            "correo": taller_data.get("correo"),
            "telefono": taller_data.get("telefono"),
            "direccion": taller_data.get("direccion"),
            "programa_academico": taller_data.get("programa_academico"),
            "semestre": taller_data.get("semestre"),
            "estrato": taller_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear taller de habilidades
        taller = {
            "estudiante_id": estudiante_id,
            "nombre_taller": taller_data.get("nombre_taller"),
            "fecha_taller": taller_data.get("fecha_taller"),
            "observaciones": taller_data.get("observaciones") or ""
        }
        
        result = self.talleres_data.create(taller)
        result["estudiante"] = datos_estudiante
        
        return result
    
    # Métodos para Seguimientos Académicos
    
    def get_all_seguimientos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los seguimientos académicos con datos del estudiante.
        
        Returns:
            Lista de seguimientos académicos
        """
        return self.seguimientos_data.get_with_estudiante()
    
    def create_seguimiento(self, seguimiento_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo seguimiento académico.
        
        Args:
            seguimiento_data: Datos del seguimiento
            
        Returns:
            Seguimiento creado
        """
        # Normalizar campos: si existen las versiones con sufijo '1', usarlas como versiones normales
        if "numero_documento1" in seguimiento_data and "numero_documento" not in seguimiento_data:
            seguimiento_data["numero_documento"] = seguimiento_data["numero_documento1"]
        
        if "correo1" in seguimiento_data and "correo" not in seguimiento_data:
            seguimiento_data["correo"] = seguimiento_data["correo1"]
            
        # Extraer datos del estudiante
        datos_estudiante = {
            "documento": seguimiento_data.get("numero_documento"),
            "tipo_documento": seguimiento_data.get("tipo_documento"),
            "nombres": seguimiento_data.get("nombres"),
            "apellidos": seguimiento_data.get("apellidos"),
            "correo": seguimiento_data.get("correo"),
            "telefono": seguimiento_data.get("telefono"),
            "direccion": seguimiento_data.get("direccion"),
            "programa_academico": seguimiento_data.get("programa_academico"),
            "semestre": seguimiento_data.get("semestre"),
            "estrato": seguimiento_data.get("estrato")
        }
        
        # Buscar o crear estudiante
        estudiante_id = self.estudiantes_data.buscar_o_crear(datos_estudiante)
        
        # Crear seguimiento académico
        seguimiento = {
            "estudiante_id": estudiante_id,
            "estado_participacion": seguimiento_data.get("estado_participacion"),
            "observaciones_permanencia": seguimiento_data.get("observaciones_permanencia")
        }
        
        result = self.seguimientos_data.create(seguimiento)
        result["estudiante"] = datos_estudiante
        
        return result
