from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from data.programas_data import ProgramasData
from models.programas import ProgramaCreate, ProgramaResponse, ProgramaUpdate

class ProgramasService:
    """Servicio para la gestión de programas académicos."""
    
    def __init__(self):
        """Inicializa el servicio con acceso a datos de programas."""
        self.data = ProgramasData()
    
    def get_all_programas(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los programas académicos.
        
        Returns:
            Lista de programas
        """
        return self.data.get_all()
    
    def get_programa_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un programa por su ID.
        
        Args:
            id: ID del programa
            
        Returns:
            Programa encontrado o None si no existe
        """
        return self.data.get_by_id(id)
    
    def get_programa_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un programa por su código.
        
        Args:
            codigo: Código del programa
            
        Returns:
            Programa encontrado o None si no existe
        """
        return self.data.get_by_codigo(codigo)
    
    def get_programas_by_facultad(self, facultad: str) -> List[Dict[str, Any]]:
        """
        Obtiene programas por facultad.
        
        Args:
            facultad: Nombre de la facultad
            
        Returns:
            Lista de programas de la facultad
        """
        return self.data.get_by_facultad(facultad)
    
    def get_programas_by_nivel(self, nivel: str) -> List[Dict[str, Any]]:
        """
        Obtiene programas por nivel.
        
        Args:
            nivel: Nivel académico (Pregrado, Posgrado, etc.)
            
        Returns:
            Lista de programas del nivel especificado
        """
        return self.data.get_by_nivel(nivel)
    
    def get_programas_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los programas activos.
        
        Returns:
            Lista de programas activos
        """
        return self.data.get_activos()
    
    def create_programa(self, programa_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo programa.
        
        Args:
            programa_data: Datos del programa
            
        Returns:
            Programa creado
        """
        # Verificar si ya existe un programa con el mismo código
        existing = self.data.get_by_codigo(programa_data.get("codigo"))
        if existing:
            raise ValueError(f"Ya existe un programa con el código {programa_data.get('codigo')}")
        
        return self.data.create(programa_data)
    
    def update_programa(self, id: str, programa_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un programa existente.
        
        Args:
            id: ID del programa
            programa_data: Datos a actualizar
            
        Returns:
            Programa actualizado
        """
        # Verificar si el programa existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un programa con el ID {id}")
        
        # Si se está actualizando el código, verificar que no exista otro programa con ese código
        if "codigo" in programa_data and programa_data["codigo"] != existing["codigo"]:
            codigo_check = self.data.get_by_codigo(programa_data["codigo"])
            if codigo_check and codigo_check["id"] != id:
                raise ValueError(f"Ya existe otro programa con el código {programa_data['codigo']}")
        
        return self.data.update(id, programa_data)
    
    def delete_programa(self, id: str) -> bool:
        """
        Elimina un programa.
        
        Args:
            id: ID del programa
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar si el programa existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un programa con el ID {id}")
        
        return self.data.delete(id)
