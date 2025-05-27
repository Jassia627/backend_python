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
        formats = ['%d-%m-%Y', '%d/%m/%Y', '%d-%b-%Y', '%d %b %Y', '%Y-%m-%d']
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

@router.post("/importar-remisiones",
          summary="Importar remisiones psicológicas desde CSV",
          description="Permite importar remisiones psicológicas desde un archivo CSV")
async def importar_remisiones(file: UploadFile = File(...)):
    """Importa remisiones psicológicas desde un archivo CSV."""
    try:
        print(f"Recibiendo archivo CSV para remisiones psicológicas: {file.filename}")
        
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        print(f"Columnas en el CSV: {df.columns.tolist()}")
        print(f"Primeras 2 filas: {df.head(2).to_dict('records')}")
        
        # Inicializar contadores
        registros_creados = 0
        errores = 0
        
        # Procesar cada fila del CSV
        for index, row in df.iterrows():
            try:
                # Buscar estudiante por número de documento
                estudiante_id = None
                if pd.notna(row.get("numero_documento")):
                    estudiante = supabase.table("estudiantes").select("id").eq("documento", str(row["numero_documento"])).execute()
                    if estudiante.data and len(estudiante.data) > 0:
                        estudiante_id = estudiante.data[0]["id"]
                        print(f"Estudiante encontrado con ID: {estudiante_id}")
                
                # Mapear programa académico correctamente
                programa_academico = ""
                if pd.notna(row.get("programa_academico")):
                    programa_academico = str(row["programa_academico"])
                elif pd.notna(row.get("estudiante_programa_academico_academico")):
                    programa_academico = str(row["estudiante_programa_academico_academico"])
                elif pd.notna(row.get("estudiante_programa_academico")):
                    programa_academico = str(row["estudiante_programa_academico"])
                else:
                    programa_academico = "No especificado"
                
                print(f"Programa académico mapeado: {programa_academico}")
                
                # Verificar y completar campos obligatorios que podrían faltar
                nombre_estudiante = str(row["nombre_estudiante"]) if pd.notna(row.get("nombre_estudiante")) else "Estudiante sin nombre"
                numero_documento = str(row["numero_documento"]) if pd.notna(row.get("numero_documento")) else "0000000000"
                docente_remite = str(row["docente_remite"]) if pd.notna(row.get("docente_remite")) else "Docente por defecto"
                correo_docente = str(row["correo_docente"]) if pd.notna(row.get("correo_docente")) else "docente@ejemplo.com"
                telefono_docente = str(row["telefono_docente"]) if pd.notna(row.get("telefono_docente")) else "0000000000"
                
                # Obtener la fecha de remisión del CSV o usar la fecha actual
                fecha_remision = None
                if pd.notna(row.get("fecha_remision")):
                    fecha_remision = convert_date_format(row["fecha_remision"])
                elif pd.notna(row.get("fecha")):
                    fecha_remision = convert_date_format(row["fecha"])
                else:
                    fecha_remision = datetime.now().strftime('%Y-%m-%d')
                
                # Crear remisión psicológica con todos los campos obligatorios
                remision_data = {
                    "estudiante_id": estudiante_id,
                    "nombre_estudiante": nombre_estudiante,
                    "numero_documento": numero_documento,
                    "programa_academico": programa_academico,
                    "semestre": str(row["semestre"]) if pd.notna(row.get("semestre")) else "1",
                    "motivo_remision": str(row["motivo_remision"]) if pd.notna(row.get("motivo_remision")) else "No especificado",
                    "docente_remite": docente_remite,
                    "correo_docente": correo_docente,
                    "telefono_docente": telefono_docente,
                    "fecha": convert_date_format(row["fecha"]) if pd.notna(row.get("fecha")) else datetime.now().strftime('%Y-%m-%d'),
                    "hora": str(row["hora"]) if pd.notna(row.get("hora")) else "12:00",
                    "tipo_remision": str(row["tipo_remision"]) if pd.notna(row.get("tipo_remision")) else "individual",
                    "fecha_remision": fecha_remision,  # Campo adicional necesario
                    "observaciones": str(row["observaciones"]) if pd.notna(row.get("observaciones")) else "Importado desde CSV",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                print(f"Insertando remisión psicológica: {remision_data}")
                
                # Insertar en la base de datos
                response = supabase.table("remisiones_psicologicas").insert(remision_data).execute()
                if response.data:
                    registros_creados += 1
                    print(f"Remisión psicológica creada exitosamente: {response.data[0]['id']}")
                else:
                    errores += 1
                    print("No se pudo crear la remisión psicológica")
            except Exception as e:
                print(f"Error al procesar remisión psicológica en fila {index+2}: {str(e)}")
                traceback.print_exc()
                errores += 1
        
        # Retornar respuesta
        return {
            "success": True,
            "message": f"Proceso completado. Se crearon {registros_creados} remisiones psicológicas. Hubo {errores} errores.",
            "registros_creados": registros_creados,
            "errores": errores
        }
    except Exception as e:
        print(f"Error al importar remisiones psicológicas: {str(e)}")
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error al importar remisiones psicológicas: {str(e)}",
            "registros_creados": 0,
            "errores": 1
        }
