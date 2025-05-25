from typing import Dict, List, Any, Optional
from .base_data import BaseData
import sys
import os

# Importar la configuración existente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import supabase

class EstudiantesData(BaseData):
    """Clase para el acceso a datos de estudiantes."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de estudiantes."""
        super().__init__("estudiantes")
    
    def get_by_documento(self, documento: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un estudiante por su número de documento.
        
        Args:
            documento: Número de documento del estudiante
            
        Returns:
            Estudiante encontrado o None si no existe
        """
        response = supabase.table(self.table_name).select("*").eq("documento", documento).execute()
        return response.data[0] if response.data else None
    
    def get_by_correo(self, correo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un estudiante por su correo electrónico.
        
        Args:
            correo: Correo electrónico del estudiante
            
        Returns:
            Estudiante encontrado o None si no existe
        """
        response = supabase.table(self.table_name).select("*").eq("correo", correo).execute()
        return response.data[0] if response.data else None
    
    def get_by_programa(self, programa_academico: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los estudiantes de un programa académico.
        
        Args:
            programa_academico: Nombre del programa académico
            
        Returns:
            Lista de estudiantes del programa
        """
        response = supabase.table(self.table_name).select("*").eq("programa_academico", programa_academico).execute()
        return response.data
    
    def buscar_o_crear(self, datos_estudiante: Dict[str, Any]) -> str:
        """
        Busca un estudiante por número de documento o crea uno nuevo si no existe.
        
        Args:
            datos_estudiante: Datos del estudiante
            
        Returns:
            ID del estudiante
        """
        # Verificar que tenemos los datos necesarios
        if not datos_estudiante.get("documento"):
            raise ValueError("El número de documento es obligatorio")
            
        if not datos_estudiante.get("nombres") or not datos_estudiante.get("apellidos"):
            raise ValueError("Los nombres y apellidos son obligatorios")
            
        if not datos_estudiante.get("tipo_documento"):
            raise ValueError("El tipo de documento es obligatorio")
            
        if not datos_estudiante.get("correo"):
            raise ValueError("El correo es obligatorio")
            
        if not datos_estudiante.get("programa_academico"):
            raise ValueError("El programa académico es obligatorio")
            
        if not datos_estudiante.get("semestre"):
            raise ValueError("El semestre es obligatorio")
            
        # Buscar estudiante por número de documento
        estudiante = self.get_by_documento(datos_estudiante["documento"])
        
        if estudiante:
            # Estudiante encontrado, retornar su ID
            return estudiante["id"]
        else:
            # Crear nuevo estudiante
            nuevo_estudiante = {
                "documento": datos_estudiante["documento"],
                "tipo_documento": datos_estudiante["tipo_documento"],
                "nombres": datos_estudiante["nombres"],
                "apellidos": datos_estudiante["apellidos"],
                "correo": datos_estudiante["correo"],
                "telefono": datos_estudiante.get("telefono") or "",
                "direccion": datos_estudiante.get("direccion") or "",
                "programa_academico": datos_estudiante["programa_academico"],
                "semestre": datos_estudiante["semestre"],
                "estrato": datos_estudiante.get("estrato") or 1,  # Valor por defecto
            }
            
            result = self.create(nuevo_estudiante)
            
            if result and "id" in result:
                return result["id"]
            else:
                raise ValueError("No se pudo crear el estudiante")
