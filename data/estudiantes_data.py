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
        try:
            print(f"Buscando o creando estudiante con datos: {datos_estudiante}")
            
            # Verificar que tenemos los datos necesarios
            if not datos_estudiante.get("documento"):
                raise ValueError("El número de documento es obligatorio")
                
            # Buscar estudiante por número de documento
            estudiante = self.get_by_documento(datos_estudiante["documento"])
            
            if estudiante:
                # Estudiante encontrado, retornar su ID
                print(f"Estudiante encontrado con ID: {estudiante['id']}")
                return estudiante["id"]
            else:
                # Crear nuevo estudiante con valores por defecto para campos obligatorios
                nuevo_estudiante = {
                    "documento": datos_estudiante["documento"],
                    "tipo_documento": datos_estudiante.get("tipo_documento") or "CC",
                    "nombres": datos_estudiante.get("nombres") or "Sin nombre",
                    "apellidos": datos_estudiante.get("apellidos") or "Sin apellido",
                    "correo": datos_estudiante.get("correo") or f"{datos_estudiante['documento']}@example.com",
                    "telefono": datos_estudiante.get("telefono") or "",
                    "direccion": datos_estudiante.get("direccion") or "",
                    "programa_academico": datos_estudiante.get("programa_academico") or "No especificado",
                    "semestre": datos_estudiante.get("semestre") or 1,
                    "estrato": datos_estudiante.get("estrato") or 1
                }
                
                # Solo agregar riesgo_desercion si está en los datos
                if datos_estudiante.get("riesgo_desercion"):
                    nuevo_estudiante["riesgo_desercion"] = datos_estudiante["riesgo_desercion"]
                
                print(f"Creando nuevo estudiante con datos: {nuevo_estudiante}")
                
                try:
                    result = self.create(nuevo_estudiante)
                    
                    if result and "id" in result:
                        print(f"Estudiante creado con ID: {result['id']}")
                        return result["id"]
                    else:
                        print(f"Error al crear estudiante: resultado sin ID")
                        raise ValueError("No se pudo crear el estudiante: resultado sin ID")
                except Exception as e:
                    error_str = str(e)
                    if "riesgo_desercion" in error_str and "column" in error_str:
                        # Si el error es por la columna riesgo_desercion, intentar crear sin ella
                        print(f"Campo riesgo_desercion no existe en la tabla, creando sin él...")
                        nuevo_estudiante_sin_riesgo = {k: v for k, v in nuevo_estudiante.items() if k != "riesgo_desercion"}
                        try:
                            result = self.create(nuevo_estudiante_sin_riesgo)
                            if result and "id" in result:
                                print(f"Estudiante creado sin riesgo_desercion con ID: {result['id']}")
                                return result["id"]
                        except Exception as e2:
                            print(f"Error al crear estudiante sin riesgo_desercion: {str(e2)}")
                            raise ValueError(f"No se pudo crear el estudiante: {str(e2)}")
                    
                    print(f"Error al crear estudiante en Supabase: {str(e)}")
                    raise ValueError(f"No se pudo crear el estudiante: {str(e)}")
        except Exception as e:
            print(f"Error en buscar_o_crear: {str(e)}")
            raise ValueError(f"Error en buscar_o_crear: {str(e)}")
