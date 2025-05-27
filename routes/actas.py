from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from config import supabase

router = APIRouter()

class ActaNegacion(BaseModel):
    """Modelo para representar un acta de negación de servicio."""
    estudiante_id: Optional[uuid.UUID] = Field(None, description="ID del estudiante que niega el servicio")
    nombre_estudiante: str = Field(..., description="Nombre completo del estudiante")
    documento_tipo: str = Field(..., description="Tipo de documento del estudiante")
    documento_numero: str = Field(..., description="Número de documento del estudiante")
    documento_expedido_en: str = Field(..., description="Lugar de expedición del documento")
    estudiante_programa_academico: str = Field(..., description="Programa académico del estudiante")
    semestre: str = Field(..., description="Semestre actual del estudiante")
    fecha_firma_dia: str = Field(..., description="Día de la firma del acta")
    fecha_firma_mes: str = Field(..., description="Mes de la firma del acta")
    fecha_firma_anio: str = Field(..., description="Año de la firma del acta")
    firma_estudiante: str = Field(..., description="Firma del estudiante (texto)")
    documento_firma_estudiante: str = Field(..., description="Documento de la persona que firma")
    docente_permanencia: str = Field(..., description="Docente de permanencia")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales sobre la negación")
    created_at: Optional[str] = Field(None, description="Fecha de creación del acta")

@router.get("/actas-negacion", 
          summary="Obtener todas las actas de negación",
          description="Retorna una lista de todas las actas de negación registradas",
          response_model=List[Dict[str, Any]])
async def get_actas_negacion():
    """Obtiene todas las actas de negación."""
    try:
        response = supabase.table("actas_negacion").select("*").execute()
        
        # Formatear las fechas para evitar el problema de "Invalid Date" en el frontend
        for acta in response.data:
            # Crear una fecha completa a partir de los componentes
            if all(k in acta for k in ["fecha_firma_anio", "fecha_firma_mes", "fecha_firma_dia"]):
                try:
                    # Asegurarse de que los componentes sean números
                    anio = int(acta["fecha_firma_anio"])
                    mes = int(acta["fecha_firma_mes"])
                    dia = int(acta["fecha_firma_dia"])
                    
                    # Crear una fecha ISO formateada
                    fecha_iso = f"{anio:04d}-{mes:02d}-{dia:02d}T00:00:00Z"
                    acta["fecha_completa"] = fecha_iso
                    
                    # Formato legible para mostrar
                    acta["fecha_legible"] = f"{dia:02d}/{mes:02d}/{anio:04d}"
                except (ValueError, TypeError) as e:
                    print(f"Error al formatear fecha: {e}")
                    acta["fecha_completa"] = None
                    acta["fecha_legible"] = "Fecha inválida"
            
            # Formatear created_at para asegurar compatibilidad con el frontend
            if "created_at" in acta and acta["created_at"]:
                try:
                    # Si es string, convertir a datetime y luego formatear
                    if isinstance(acta["created_at"], str):
                        dt = datetime.fromisoformat(acta["created_at"].replace('Z', '+00:00'))
                        acta["created_at"] = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                except Exception as e:
                    print(f"Error al formatear created_at: {e}")
        
        return response.data
    except Exception as e:
        print(f"Error al obtener actas de negación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener actas de negación: {str(e)}")

@router.post("/actas-negacion", 
           summary="Crear una nueva acta de negación",
           description="Registra una nueva acta de negación de servicio",
           response_model=Dict[str, Any])
async def create_acta_negacion(acta: Dict[str, Any]):
    """Crea una nueva acta de negación."""
    try:
        print(f"Datos recibidos para acta de negación: {acta}")
        
        # Añadir fecha de creación en formato ISO 8601 estandarizado
        now = datetime.now()
        acta["created_at"] = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        acta["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Añadir fecha_registro como timestamp completo
        acta["fecha_registro"] = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Validar y formatear los componentes de la fecha de firma
        if all(k in acta for k in ["fecha_firma_anio", "fecha_firma_mes", "fecha_firma_dia"]):
            try:
                # Limpiar y normalizar los valores de fecha
                # Para el día, necesitamos manejar casos como '050' -> '05'
                dia_str = str(acta["fecha_firma_dia"])
                if len(dia_str) > 2:
                    # Si tiene más de 2 dígitos, tomamos los últimos 2
                    dia_str = dia_str[-2:]
                dia_int = int(dia_str)
                
                # Normalizar mes y año
                mes_int = int(str(acta["fecha_firma_mes"]).strip())
                anio_int = int(str(acta["fecha_firma_anio"]).strip())
                
                # Formatear correctamente
                acta["fecha_firma_dia"] = f"{dia_int:02d}"
                acta["fecha_firma_mes"] = f"{mes_int:02d}"
                acta["fecha_firma_anio"] = f"{anio_int:04d}"
                
                print(f"Fecha normalizada: día={acta['fecha_firma_dia']}, mes={acta['fecha_firma_mes']}, año={acta['fecha_firma_anio']}")
                
                # Crear una fecha ISO formateada para referencia
                fecha_iso = f"{acta['fecha_firma_anio']}-{acta['fecha_firma_mes']}-{acta['fecha_firma_dia']}T00:00:00Z"
                acta["fecha_completa"] = fecha_iso
                
                # Formato legible para mostrar
                acta["fecha_legible"] = f"{acta['fecha_firma_dia']}/{acta['fecha_firma_mes']}/{acta['fecha_firma_anio']}"
            except Exception as e:
                print(f"Error al formatear componentes de fecha: {e}")
                # En caso de error, establecer valores por defecto
                acta["fecha_completa"] = None
                acta["fecha_legible"] = "Fecha inválida"
        
        # Buscar estudiante por número de documento si no se proporciona estudiante_id
        if "documento_numero" in acta and not acta.get("estudiante_id"):
            estudiante = supabase.table("estudiantes").select("id").eq("documento", acta["documento_numero"]).execute()
            if estudiante.data and len(estudiante.data) > 0:
                acta["estudiante_id"] = estudiante.data[0]["id"]
                print(f"Estudiante encontrado con ID: {acta['estudiante_id']}")
            else:
                # Si no se encuentra el estudiante, establecer estudiante_id como NULL
                acta["estudiante_id"] = None
                print("No se encontró estudiante con ese documento")
        
        # Definir los campos válidos para la tabla actas_negacion
        campos_validos = [
            "id", "estudiante_id", "nombre_estudiante", "documento_tipo", "documento_numero",
            "documento_expedido_en", "estudiante_programa_academico", "semestre",
            "fecha_firma_dia", "fecha_firma_mes", "fecha_firma_anio", "fecha_registro",
            "fecha_completa", "fecha_legible", "firma_estudiante", "documento_firma_estudiante",
            "docente_permanencia", "observaciones", "created_at", "updated_at"
        ]
        
        # Filtrar solo los campos válidos para evitar duplicados
        acta_filtrada = {}
        for campo in campos_validos:
            if campo in acta:
                acta_filtrada[campo] = acta[campo]
        
        print(f"Acta de negación filtrada para inserción: {acta_filtrada}")
        response = supabase.table("actas_negacion").insert(acta_filtrada).execute()
        
        if response.data and len(response.data) > 0:
            print(f"Acta de negación creada con ID: {response.data[0].get('id')}")
            return response.data[0]
        else:
            print("No se recibieron datos de respuesta al crear el acta")
            raise HTTPException(status_code=500, detail="No se pudo crear el acta de negación")
    except Exception as e:
        print(f"Error al crear acta de negación: {e}")
        # Proporcionar un mensaje de error más detallado para facilitar la depuración
        error_detail = f"Error al crear acta de negación: {str(e)}"
        if hasattr(e, '__dict__'):
            error_detail += f" | Detalles adicionales: {str(e.__dict__)}"
        raise HTTPException(status_code=500, detail=error_detail)

