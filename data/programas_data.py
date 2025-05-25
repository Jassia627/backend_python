from typing import Dict, List, Any, Optional
from .base_data import BaseData
from config import supabase

class ProgramasData(BaseData):
    """Clase para el acceso a datos de programas académicos."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de programas."""
        super().__init__("programas")
    
    def get_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un programa por su código.
        
        Args:
            codigo: Código del programa
            
        Returns:
            Programa encontrado o None si no existe
        """
        response = supabase.table(self.table_name).select("*").eq("codigo", codigo).execute()
        return response.data[0] if response.data else None
    
    def get_by_facultad(self, facultad: str) -> List[Dict[str, Any]]:
        """
        Obtiene programas por facultad.
        
        Args:
            facultad: Nombre de la facultad
            
        Returns:
            Lista de programas de la facultad
        """
        response = supabase.table(self.table_name).select("*").eq("facultad", facultad).execute()
        return response.data
    
    def get_by_nivel(self, nivel: str) -> List[Dict[str, Any]]:
        """
        Obtiene programas por nivel.
        
        Args:
            nivel: Nivel académico (Pregrado, Posgrado, etc.)
            
        Returns:
            Lista de programas del nivel especificado
        """
        response = supabase.table(self.table_name).select("*").eq("nivel", nivel).execute()
        return response.data
    
    def get_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los programas activos.
        
        Returns:
            Lista de programas activos
        """
        response = supabase.table(self.table_name).select("*").eq("estado", True).execute()
        return response.data
