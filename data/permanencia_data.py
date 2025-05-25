from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_data import BaseData
import sys
import os

# Importar la configuración existente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import supabase

class TutoriasAcademicasData(BaseData):
    """Clase para el acceso a datos de tutorías académicas."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de tutorías académicas."""
        super().__init__("tutorias_academicas")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tutorías académicas con datos del estudiante.
        
        Returns:
            Lista de tutorías académicas con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
            Lista de asesorías psicológicas con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
            Lista de orientaciones vocacionales con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
        super().__init__("comedores_universitarios")
    
    def get_with_estudiante(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de comedor universitario con datos del estudiante.
        
        Returns:
            Lista de registros de comedor universitario con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
            Lista de apoyos socioeconómicos con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
            Lista de talleres de habilidades con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
            Lista de seguimientos académicos con datos del estudiante
        """
        response = supabase.table(self.table_name).select("*, estudiantes(*)").execute()
        return response.data
    
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
