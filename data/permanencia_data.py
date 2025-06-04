from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_data import BaseData
import sys
import os

# Importar la configuración existente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import supabase
from utils.safe_formatting import safe_str, safe_int, safe_bool, safe_float

# Helper function to format student data
def _format_estudiante_data(estudiante_raw: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Formatea los datos del estudiante asegurando que todos los valores sean primitivos.
    """
    if not estudiante_raw or not isinstance(estudiante_raw, dict):
        return {
            "nombres": "N/A",
            "apellidos": "N/A",
            "correo1": "N/A",
            "numero_documento1": "N/A",
            "tipo_documento": "N/A",
            "telefono": "N/A",
            "direccion": "N/A",
            "programa_academico": "N/A",
            "semestre": "N/A",
            "estrato": "N/A",
            "riesgo_desercion": "N/A"
        }
    
    # Ensure all values are strings or primitive types to avoid React rendering issues
    formatted_student = {
        "nombres": safe_str(estudiante_raw.get("nombres")),
        "apellidos": safe_str(estudiante_raw.get("apellidos")),
        "correo1": safe_str(estudiante_raw.get("correo")),
        "numero_documento1": safe_str(estudiante_raw.get("documento")),
        "tipo_documento": safe_str(estudiante_raw.get("tipo_documento")),
        "telefono": safe_str(estudiante_raw.get("telefono")),
        "direccion": safe_str(estudiante_raw.get("direccion")),
        "programa_academico": safe_str(estudiante_raw.get("programa_academico")),
        "semestre": safe_str(estudiante_raw.get("semestre")),
        "estrato": safe_str(estudiante_raw.get("estrato")),
        "riesgo_desercion": safe_str(estudiante_raw.get("riesgo_desercion"))
    }
    return formatted_student


class TutoriasAcademicasData(BaseData):
    """Clase para el acceso a datos de tutorías académicas."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de tutorías académicas."""
        super().__init__("tutorias_academicas")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tutorías académicas con datos del estudiante.
        
        Returns:
            Lista de tutorías académicas con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    if not isinstance(item, dict):
                        continue
                        
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        "id": safe_str(item.get('id')),
                        "estudiante_id": safe_str(item.get('estudiante_id')),
                        "nivel_riesgo": safe_str(item.get('nivel_riesgo')),
                        "requiere_tutoria": safe_bool(item.get('requiere_tutoria')),
                        "fecha_asignacion": safe_str(item.get('fecha_asignacion')),
                        "acciones_apoyo": safe_str(item.get('acciones_apoyo'), ''),
                        "created_at": safe_str(item.get('created_at')),
                        "updated_at": safe_str(item.get('updated_at')),
                        "estudiante": _format_estudiante_data(estudiante_raw),
                        "riesgo": safe_str(_estudiante_data_for_top_level.get('riesgo_desercion')),
                        "fecha": safe_str(item.get('fecha_tutoria'))
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de tutorías académicas con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tutorías académicas de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de tutorías académicas del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class AsesoriasPsicologicasData(BaseData):
    """Clase para el acceso a datos de asesorías psicológicas."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de asesorías psicológicas."""
        super().__init__("asesorias_psicologicas")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las asesorías psicológicas con datos del estudiante.
        
        Returns:
            Lista de asesorías psicológicas con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        **item,
                        'estudiante': _format_estudiante_data(estudiante_raw),
                        'riesgo': _estudiante_data_for_top_level.get('riesgo_desercion', 'N/A'),
                        'fecha': item.get('fecha_asesoria', 'N/A') # Specific date field
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de asesorías psicológicas con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las asesorías psicológicas de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de asesorías psicológicas del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class OrientacionesVocacionalesData(BaseData):
    """Clase para el acceso a datos de orientaciones vocacionales."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de orientaciones vocacionales."""
        super().__init__("orientaciones_vocacionales")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las orientaciones vocacionales con datos del estudiante.
        
        Returns:
            Lista de orientaciones vocacionales con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        **item,
                        'estudiante': _format_estudiante_data(estudiante_raw),
                        'riesgo': _estudiante_data_for_top_level.get('riesgo_desercion', 'N/A'),
                        'fecha': item.get('fecha_orientacion', 'N/A') # Specific date field
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de orientaciones vocacionales con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las orientaciones vocacionales de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de orientaciones vocacionales del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class ComedoresUniversitariosData(BaseData):
    """Clase para el acceso a datos de comedores universitarios."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de comedores universitarios."""
        super().__init__("comedor_universitario")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de comedor universitario con datos del estudiante.
        
        Returns:
            Lista de registros de comedor universitario con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    if not isinstance(item, dict):
                        continue
                        
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    
                    # Ensure all values are properly formatted and serializable
                    formatted_item = {
                        "id": safe_str(item.get('id')),
                        "estudiante_id": safe_str(item.get('estudiante_id')),
                        "condicion_socioeconomica": safe_str(item.get('condicion_socioeconomica')),
                        "fecha_solicitud": safe_str(item.get('fecha_solicitud')),
                        "aprobado": safe_bool(item.get('aprobado')),
                        "tipo_comida": safe_str(item.get('tipo_comida'), 'Almuerzo'),
                        "raciones_asignadas": safe_int(item.get('raciones_asignadas'), 1),
                        "observaciones": safe_str(item.get('observaciones'), ''),
                        "tipo_subsidio": safe_str(item.get('tipo_subsidio'), ''),
                        "periodo_academico": safe_str(item.get('periodo_academico'), ''),
                        "estrato": safe_int(item.get('estrato'), 1),
                        "created_at": safe_str(item.get('created_at')),
                        "updated_at": safe_str(item.get('updated_at')),
                        "estudiante": _format_estudiante_data(estudiante_raw),
                        "riesgo": safe_str(_estudiante_data_for_top_level.get('riesgo_desercion')),
                        "fecha": safe_str(item.get('fecha_solicitud'))
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de comedor universitario con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de comedor universitario de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de registros de comedor universitario del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class ApoyosSocioeconomicosData(BaseData):
    """Clase para el acceso a datos de apoyos socioeconómicos."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de apoyos socioeconómicos."""
        super().__init__("apoyos_socioeconomicos")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los apoyos socioeconómicos con datos del estudiante.
        
        Returns:
            Lista de apoyos socioeconómicos con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        **item, 
                        'estudiante': _format_estudiante_data(estudiante_raw),
                        'riesgo': _estudiante_data_for_top_level.get('riesgo_desercion', 'N/A'),
                        'fecha': item.get('fecha_solicitud', 'N/A') # Specific date field
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de apoyos socioeconómicos con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los apoyos socioeconómicos de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de apoyos socioeconómicos del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class TalleresHabilidadesData(BaseData):
    """Clase para el acceso a datos de talleres de habilidades."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de talleres de habilidades."""
        super().__init__("talleres_habilidades")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los talleres de habilidades con datos del estudiante.
        
        Returns:
            Lista de talleres de habilidades con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        **item, 
                        'estudiante': _format_estudiante_data(estudiante_raw),
                        'riesgo': _estudiante_data_for_top_level.get('riesgo_desercion', 'N/A'),
                        'fecha': item.get('fecha_realizacion', 'N/A') # Specific date field
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de talleres de habilidades con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los talleres de habilidades de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de talleres de habilidades del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data

class SeguimientosAcademicosData(BaseData):
    """Clase para el acceso a datos de seguimientos académicos."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de seguimientos académicos."""
        super().__init__("seguimientos_academicos")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los seguimientos académicos con datos del estudiante.
        
        Returns:
            Lista de seguimientos académicos con datos del estudiante, formateada para el frontend.
        """
        try:
            response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
            formatted_data = []
            if response.data:
                for item in response.data:
                    estudiante_raw = item.pop('estudiantes', None)
                    _estudiante_data_for_top_level = estudiante_raw if isinstance(estudiante_raw, dict) else {}
                    formatted_item = {
                        **item, 
                        'estudiante': _format_estudiante_data(estudiante_raw),
                        'riesgo': _estudiante_data_for_top_level.get('riesgo_desercion', 'N/A'),
                        'fecha': item.get('fecha_seguimiento', 'N/A') # Specific date field
                    }
                    formatted_data.append(formatted_item)
            return formatted_data
        except Exception as e:
            print(f"Error al obtener registros de seguimientos académicos con estudiante: {str(e)}")
            return []
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los seguimientos académicos de un estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de seguimientos académicos del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data
