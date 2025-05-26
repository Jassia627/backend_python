from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any, List
import io
import pandas as pd
import uuid
import traceback
from datetime import datetime

from config import supabase
from utils.responses import success_response, error_response, handle_exception

router = APIRouter()

# Función para convertir fechas de formato DD-MM-YYYY a YYYY-MM-DD
def convert_date_format(date_str):
    if not date_str or pd.isna(date_str):
        return None
    try:
        # Intentar varios formatos de fecha
        formats = ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%d-%b-%Y', '%d %b %Y']
        for fmt in formats:
            try:
                date_obj = datetime.strptime(str(date_str), fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        # Si ninguno funciona, devolver None
        print(f"No se pudo convertir la fecha: {date_str}")
        return None
    except Exception as e:
        print(f"Error al convertir fecha {date_str}: {str(e)}")
        return None

@router.post("/importar-intervenciones",
          summary="Importar intervenciones grupales desde CSV",
          description="Permite cargar intervenciones grupales masivamente desde un archivo CSV")
async def importar_intervenciones(file: UploadFile = File(...)):
    """Importa intervenciones grupales desde un archivo CSV."""
    try:
        print(f"Recibiendo archivo CSV de intervenciones: {file.filename}")
        
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        print(f"Columnas en el CSV: {df.columns.tolist()}")
        print(f"Primeras 2 filas: {df.head(2).to_dict('records')}")
        
        # Inicializar contadores
        inserted = 0
        errors = []
        processed_data = []
        
        # Mapeo de columnas del CSV a campos de la base de datos
        # Este mapeo debe ajustarse según las columnas exactas de tu CSV
        column_mapping = {
            "fecha_solicitud": "fecha_solicitud",
            "nombre_docente_permanencia": "nombre_docente_permanencia",
            "celular_permanencia": "celular_permanencia",
            "correo_permanencia": "correo_permanencia",
            "programa_permanencia": "estudiante_programa_academico_permanencia",
            "tipo_poblacion": "tipo_poblacion",
            "nombre_docente_asignatura": "nombre_docente_asignatura",
            "celular_docente_asignatura": "celular_docente_asignatura",
            "correo_docente_asignatura": "correo_docente_asignatura",
            "programa_docente_asignatura": "estudiante_programa_academico_docente_asignatura",
            "asignatura_intervenir": "asignatura_intervenir",
            "grupo": "grupo",
            "semestre": "semestre",
            "numero_estudiantes": "numero_estudiantes",
            "tematica_sugerida": "tematica_sugerida",
            "fecha_programada": "fecha_estudiante_programa_academicoda",
            "hora": "hora",
            "aula": "aula",
            "bloque": "bloque",
            "sede": "sede",
            "estado": "estado",
            "motivo": "motivo",
            "efectividad": "efectividad"
        }
        
        # Procesar cada fila del CSV
        for index, row in df.iterrows():
            try:
                # Crear diccionario para la intervención grupal
                intervencion_data = {}
                
                # Mapear columnas del CSV a campos de la base de datos
                for csv_col, db_col in column_mapping.items():
                    if csv_col in row:
                        # Manejar fechas
                        if db_col in ["fecha_solicitud", "fecha_estudiante_programa_academicoda"]:
                            intervencion_data[db_col] = convert_date_format(row[csv_col])
                        # Manejar campos numéricos
                        elif db_col in ["grupo", "semestre", "numero_estudiantes"]:
                            if pd.notna(row[csv_col]):
                                intervencion_data[db_col] = str(int(row[csv_col]))
                            else:
                                intervencion_data[db_col] = "1"  # Valor por defecto
                        # Manejar otros campos
                        else:
                            if pd.notna(row[csv_col]):
                                intervencion_data[db_col] = str(row[csv_col])
                
                # Establecer valores por defecto para campos obligatorios que podrían faltar
                required_fields = [
                    "fecha_solicitud", "nombre_docente_permanencia", "celular_permanencia",
                    "correo_permanencia", "estudiante_programa_academico_permanencia", "tipo_poblacion",
                    "nombre_docente_asignatura", "celular_docente_asignatura", "correo_docente_asignatura",
                    "estudiante_programa_academico_docente_asignatura", "asignatura_intervenir",
                    "grupo", "semestre", "numero_estudiantes", "fecha_estudiante_programa_academicoda",
                    "hora", "aula", "bloque", "sede", "estado"
                ]
                
                for field in required_fields:
                    if field not in intervencion_data or not intervencion_data[field]:
                        if field == "fecha_solicitud" or field == "fecha_estudiante_programa_academicoda":
                            intervencion_data[field] = datetime.now().strftime('%Y-%m-%d')
                        elif field == "celular_permanencia" or field == "celular_docente_asignatura":
                            intervencion_data[field] = "0000000000"
                        elif field == "correo_permanencia":
                            intervencion_data[field] = f"permanencia_{index}@ejemplo.com"
                        elif field == "correo_docente_asignatura":
                            intervencion_data[field] = f"docente_{index}@ejemplo.com"
                        elif field == "grupo" or field == "semestre" or field == "numero_estudiantes":
                            intervencion_data[field] = "1"
                        elif field == "hora":
                            intervencion_data[field] = "08:00"
                        elif field == "estado":
                            intervencion_data[field] = "espera"
                        else:
                            intervencion_data[field] = f"Valor por defecto {field}"
                
                # Si el estado no es "se hizo" y no hay motivo, establecer un motivo por defecto
                if intervencion_data.get("estado") != "se hizo" and not intervencion_data.get("motivo"):
                    intervencion_data["motivo"] = "Importado desde CSV"
                
                # Establecer efectividad según el estado
                if intervencion_data.get("estado") == "se hizo":
                    if not intervencion_data.get("efectividad"):
                        intervencion_data["efectividad"] = "Pendiente evaluación"
                else:
                    intervencion_data["efectividad"] = "N/A"
                
                print(f"Creando intervención grupal: {intervencion_data}")
                
                # Insertar en la base de datos
                response = supabase.table("intervenciones_grupales").insert(intervencion_data).execute()
                
                if response.data:
                    inserted += 1
                    processed_data.append({
                        "fila": index + 1,
                        "asignatura": intervencion_data.get("asignatura_intervenir", ""),
                        "docente": intervencion_data.get("nombre_docente_asignatura", ""),
                        "procesado": True
                    })
                else:
                    raise Exception("No se pudo crear la intervención grupal, respuesta vacía")
                
            except Exception as e:
                error_msg = f"Error en fila {index+1}: {str(e)}"
                print(error_msg)
                print(f"Traceback: {traceback.format_exc()}")
                errors.append(error_msg)
                
                # Añadir a los datos procesados con error
                processed_data.append({
                    "fila": index + 1,
                    "asignatura": row.get("asignatura_intervenir", "") if "asignatura_intervenir" in row else "",
                    "error": str(e),
                    "procesado": False
                })
        
        # Retornar respuesta
        return {
            "success": True,
            "data": processed_data,
            "inserted": inserted,
            "errors": errors,
            "message": f"Se procesaron {inserted} intervenciones grupales correctamente."
        }
            
    except Exception as e:
        error_msg = f"Error al procesar el archivo CSV: {str(e)}"
        print(error_msg)
        print(f"Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "inserted": 0,
            "errors": [error_msg],
            "message": "Ocurrió un error al procesar el archivo CSV. Por favor, verifica el formato e intenta nuevamente."
        }
