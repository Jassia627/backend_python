from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from data.estudiantes_data import EstudiantesData
from models.estudiantes import EstudianteCreate, EstudianteResponse, EstudianteUpdate

class EstudiantesService:
    """Servicio para la gestión de estudiantes."""
    
    def __init__(self):
        """Inicializa el servicio de estudiantes."""
        self.data = EstudiantesData()
    
    def get_all_estudiantes(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los estudiantes.
        
        Returns:
            Lista de estudiantes
        """
        return self.data.get_all()
    
    def get_estudiante_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un estudiante por su ID.
        
        Args:
            id: ID del estudiante
            
        Returns:
            Estudiante encontrado o None si no existe
        """
        return self.data.get_by_id(id)
    
    def get_estudiante_by_documento(self, documento: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un estudiante por su número de documento.
        
        Args:
            documento: Número de documento del estudiante
            
        Returns:
            Estudiante encontrado o None si no existe
        """
        return self.data.get_by_documento(documento)
    
    def create_estudiante(self, estudiante: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo estudiante.
        
        Args:
            estudiante: Datos del estudiante
            
        Returns:
            Estudiante creado
        """
        return self.data.create(estudiante)
    
    def update_estudiante(self, id: str, estudiante: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un estudiante existente.
        
        Args:
            id: ID del estudiante
            estudiante: Datos a actualizar
            
        Returns:
            Estudiante actualizado
        """
        return self.data.update(id, estudiante)
    
    def delete_estudiante(self, id: str) -> bool:
        """
        Elimina un estudiante.
        
        Args:
            id: ID del estudiante
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        return self.data.delete(id)
    
    def buscar_o_crear_estudiante(self, datos_estudiante: Dict[str, Any]) -> str:
        """
        Busca un estudiante por número de documento o crea uno nuevo si no existe.
        
        Args:
            datos_estudiante: Datos del estudiante
            
        Returns:
            ID del estudiante
        """
        return self.data.buscar_o_crear(datos_estudiante)
