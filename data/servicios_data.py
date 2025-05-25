from typing import Dict, List, Any, Optional
from .base_data import BaseData
from config import supabase

class ServiciosData(BaseData):
    """Clase para el acceso a datos de servicios."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de servicios."""
        super().__init__("servicios")
    
    def get_by_tipo(self, tipo: str) -> List[Dict[str, Any]]:
        """
        Obtiene servicios por tipo.
        
        Args:
            tipo: Tipo de servicio (Psicología, Tutoría, etc.)
            
        Returns:
            Lista de servicios del tipo especificado
        """
        response = supabase.table(self.table_name).select("*").eq("tipo", tipo).execute()
        return response.data
    
    def get_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los servicios activos.
        
        Returns:
            Lista de servicios activos
        """
        response = supabase.table(self.table_name).select("*").eq("estado", True).execute()
        return response.data


class AsistenciasData(BaseData):
    """Clase para el acceso a datos de asistencias a servicios."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de asistencias."""
        super().__init__("asistencias")
    
    def get_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de asistencias del estudiante
        """
        response = supabase.table(self.table_name).select("*").eq("estudiante_id", estudiante_id).execute()
        return response.data
    
    def get_by_servicio(self, servicio_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por servicio.
        
        Args:
            servicio_id: ID del servicio
            
        Returns:
            Lista de asistencias al servicio
        """
        response = supabase.table(self.table_name).select("*").eq("servicio_id", servicio_id).execute()
        return response.data
    
    def get_by_fecha(self, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio (formato ISO)
            fecha_fin: Fecha de fin (formato ISO)
            
        Returns:
            Lista de asistencias en el rango de fechas
        """
        response = supabase.table(self.table_name).select("*")\
            .gte("fecha", fecha_inicio)\
            .lte("fecha", fecha_fin)\
            .execute()
        return response.data
