from typing import Dict, List, Any, Optional, Type
from datetime import datetime

import sys
import os

# Importar la configuración existente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import supabase

class BaseData:
    """Clase base para el acceso a datos."""
    
    def __init__(self, table_name: str):
        """
        Inicializa el acceso a datos para una tabla específica.
        
        Args:
            table_name: Nombre de la tabla en Supabase
        """
        self.table_name = table_name
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de la tabla.
        
        Returns:
            Lista de registros
        """
        response = supabase.table(self.table_name).select("*").execute()
        return response.data
    
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un registro por su ID.
        
        Args:
            id: ID del registro
            
        Returns:
            Registro encontrado o None si no existe
        """
        response = supabase.table(self.table_name).select("*").eq("id", id).execute()
        return response.data[0] if response.data else None
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo registro en la tabla.
        
        Args:
            data: Datos del nuevo registro
            
        Returns:
            El registro creado
        """
        try:
            response = supabase.table(self.table_name).insert(data).execute()
            
            # Verificar si la respuesta tiene datos
            if hasattr(response, 'data') and response.data:
                return response.data[0]
            
            # Si no hay datos pero tampoco hay error explícito
            error_msg = "No se recibió respuesta de la base de datos"
            if hasattr(response, 'error') and response.error:
                error_msg = str(response.error)
            elif hasattr(response, 'status_code') and response.status_code >= 400:
                error_msg = f"Error HTTP {response.status_code}"
            
            print(f"Error en create: {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            print(f"Error en método create de {self.table_name}: {str(e)}")
            raise
    
    def update(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un registro existente.
        
        Args:
            id: ID del registro
            data: Datos a actualizar
            
        Returns:
            Registro actualizado
        """
        # Actualizar timestamp
        data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table(self.table_name).update(data).eq("id", id).execute()
        return response.data[0] if response.data else {}
    
    def delete(self, id: str) -> bool:
        """
        Elimina un registro.
        
        Args:
            id: ID del registro
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        response = supabase.table(self.table_name).delete().eq("id", id).execute()
        return len(response.data) > 0
