from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from data.servicios_data import ServiciosData, AsistenciasData
from models.servicios import ServicioCreate, ServicioResponse, ServicioUpdate

class ServiciosService:
    """Servicio para la gestión de servicios."""
    
    def __init__(self):
        """Inicializa el servicio con acceso a datos de servicios."""
        self.data = ServiciosData()
        self.asistencias_data = AsistenciasData()
    
    def get_all_servicios(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los servicios.
        
        Returns:
            Lista de servicios
        """
        return self.data.get_all()
    
    def get_servicio_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un servicio por su ID.
        
        Args:
            id: ID del servicio
            
        Returns:
            Servicio encontrado o None si no existe
        """
        return self.data.get_by_id(id)
    
    def get_servicios_by_tipo(self, tipo: str) -> List[Dict[str, Any]]:
        """
        Obtiene servicios por tipo.
        
        Args:
            tipo: Tipo de servicio (Psicología, Tutoría, etc.)
            
        Returns:
            Lista de servicios del tipo especificado
        """
        return self.data.get_by_tipo(tipo)
    
    def get_servicios_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los servicios activos.
        
        Returns:
            Lista de servicios activos
        """
        return self.data.get_activos()
    
    def create_servicio(self, servicio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo servicio.
        
        Args:
            servicio_data: Datos del servicio
            
        Returns:
            Servicio creado
        """
        return self.data.create(servicio_data)
    
    def update_servicio(self, id: str, servicio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un servicio existente.
        
        Args:
            id: ID del servicio
            servicio_data: Datos a actualizar
            
        Returns:
            Servicio actualizado
        """
        # Verificar si el servicio existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un servicio con el ID {id}")
        
        return self.data.update(id, servicio_data)
    
    def delete_servicio(self, id: str) -> bool:
        """
        Elimina un servicio.
        
        Args:
            id: ID del servicio
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar si el servicio existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un servicio con el ID {id}")
        
        return self.data.delete(id)
    
    # Métodos para asistencias
    
    def get_asistencias_by_estudiante(self, estudiante_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por estudiante.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de asistencias del estudiante
        """
        return self.asistencias_data.get_by_estudiante(estudiante_id)
    
    def get_asistencias_by_servicio(self, servicio_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por servicio.
        
        Args:
            servicio_id: ID del servicio
            
        Returns:
            Lista de asistencias al servicio
        """
        return self.asistencias_data.get_by_servicio(servicio_id)
    
    def get_asistencias_by_fecha(self, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """
        Obtiene asistencias por rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio (formato ISO)
            fecha_fin: Fecha de fin (formato ISO)
            
        Returns:
            Lista de asistencias en el rango de fechas
        """
        return self.asistencias_data.get_by_fecha(fecha_inicio, fecha_fin)
    
    def create_asistencia(self, asistencia_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva asistencia.
        
        Args:
            asistencia_data: Datos de la asistencia
            
        Returns:
            Asistencia creada
        """
        return self.asistencias_data.create(asistencia_data)
    
    def update_asistencia(self, id: str, asistencia_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una asistencia existente.
        
        Args:
            id: ID de la asistencia
            asistencia_data: Datos a actualizar
            
        Returns:
            Asistencia actualizada
        """
        # Verificar si la asistencia existe
        existing = self.asistencias_data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe una asistencia con el ID {id}")
        
        return self.asistencias_data.update(id, asistencia_data)
    
    def delete_asistencia(self, id: str) -> bool:
        """
        Elimina una asistencia.
        
        Args:
            id: ID de la asistencia
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar si la asistencia existe
        existing = self.asistencias_data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe una asistencia con el ID {id}")
        
        return self.asistencias_data.delete(id)
