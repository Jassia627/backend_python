from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any, List
import io
import pandas as pd
import uuid
import datetime

from config import supabase

router = APIRouter()

@router.post("/upload-csv",
          summary="Cargar datos desde archivo CSV",
          description="Permite cargar datos masivamente desde un archivo CSV para diferentes entidades del sistema")
async def upload_csv(file: UploadFile = File(...), tipo: str = None):
    """Carga datos desde un archivo CSV."""
    try:
        print(f"Recibiendo archivo CSV: {file.filename}, tipo: {tipo}")
        
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        print(f"Columnas en el CSV: {df.columns.tolist()}")
        print(f"Primeras 2 filas: {df.head(2).to_dict('records')}")
        
        # Inicializar contadores
        inserted = 0
        errors = []
        processed_data = []
        
        # Detectar el tipo de datos basado en las columnas presentes
        columnas = df.columns.tolist()
        
        # Verificar si es el formato completo que incluye todas las entidades
        if "estudiante_numero_documento" in columnas and "estudiante_programa_academico" in columnas:
            print("Procesando datos del formato completo...")
            
            # Procesar cada fila del CSV
            for index, row in df.iterrows():
                try:
                    # 1. Primero, buscar o crear el estudiante
                    documento = str(row["estudiante_numero_documento"]) if pd.notna(row["estudiante_numero_documento"]) else None
                    programa_academico = str(row["estudiante_programa_academico"]) if pd.notna(row["estudiante_programa_academico"]) else None
                    
                    if not documento:
                        raise ValueError("El número de documento del estudiante es obligatorio")
                    
                    # Buscar si el estudiante ya existe
                    estudiante_existente = supabase.table("estudiantes").select("*").eq("documento", documento).execute()
                    
                    estudiante_id = None
                    
                    if estudiante_existente.data and len(estudiante_existente.data) > 0:
                        # El estudiante ya existe, usar su ID
                        estudiante_id = estudiante_existente.data[0]["id"]
                        print(f"Estudiante encontrado con ID: {estudiante_id}")
                    else:
                        # Crear un nuevo estudiante
                        # Primero, buscar o crear el programa
                        programa_id = None
                        if programa_academico:
                            programa = supabase.table("programas").select("id").eq("nombre", programa_academico).execute()
                            if programa.data and len(programa.data) > 0:
                                programa_id = programa.data[0]["id"]
                            else:
                                # Crear un nuevo programa
                                nuevo_programa = {
                                    "nombre": programa_academico,
                                    "facultad": "Sin asignar",
                                    "codigo": f"PROG-{len(programa_academico)}-{str(uuid.uuid4())[:8]}"
                                }
                                programa_response = supabase.table("programas").insert(nuevo_programa).execute()
                                programa_id = programa_response.data[0]["id"]
                        
                        # Crear el estudiante
                        estudiante_data = {
                            "documento": documento,
                            "tipo_documento": "CC",  # Valor por defecto
                            "nombre": "Estudiante",  # Valor por defecto
                            "apellido": documento,   # Usar documento como apellido por defecto
                            "codigo": f"EST-{documento}",
                            "email": f"estudiante.{documento}@unicesar.edu.co",
                            "telefono": "0000000000"
                        }
                        
                        # Añadir campos opcionales si están presentes
                        if programa_id:
                            estudiante_data["programa_id"] = programa_id
                        
                        if "estudiante_semestre" in row and pd.notna(row["estudiante_semestre"]):
                            try:
                                estudiante_data["semestre"] = int(row["estudiante_semestre"])
                            except:
                                estudiante_data["semestre"] = 1
                        
                        if "estudiante_estrato" in row and pd.notna(row["estudiante_estrato"]):
                            try:
                                estudiante_data["estrato"] = int(row["estudiante_estrato"])
                            except:
                                estudiante_data["estrato"] = 1
                        
                        if "estudiante_riesgo_desercion" in row and pd.notna(row["estudiante_riesgo_desercion"]):
                            estudiante_data["riesgo_desercion"] = str(row["estudiante_riesgo_desercion"]).lower()
                        
                        # Insertar el estudiante
                        print(f"Creando nuevo estudiante: {estudiante_data}")
                        estudiante_response = supabase.table("estudiantes").insert(estudiante_data).execute()
                        estudiante_id = estudiante_response.data[0]["id"]
                    
                    # 2. Procesar remisiones si corresponde
                    if "tipo_remision" in row and pd.notna(row["tipo_remision"]) and estudiante_id:
                        remision_data = {
                            "estudiante_id": estudiante_id,
                            "tipo": str(row["tipo_remision"]),
                            "fecha": str(row["fecha_remision"]) if pd.notna(row["fecha_remision"]) else datetime.datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        # Insertar la remisión
                        print(f"Creando remisión: {remision_data}")
                        supabase.table("remisiones").insert(remision_data).execute()
                    
                    # 3. Procesar asistencias si corresponde
                    if "FormatoAsistencia_fecha" in row and pd.notna(row["FormatoAsistencia_fecha"]) and estudiante_id:
                        asistencia_data = {
                            "estudiante_id": estudiante_id,
                            "fecha": str(row["FormatoAsistencia_fecha"]),
                            "numero": str(row["FormatoAsistencia_numero_asistencia"]) if pd.notna(row["FormatoAsistencia_numero_asistencia"]) else "1"
                        }
                        
                        # Insertar la asistencia
                        print(f"Creando asistencia: {asistencia_data}")
                        supabase.table("asistencias_actividades").insert(asistencia_data).execute()
                    
                    # 4. Procesar intervenciones grupales si corresponde
                    if "IntervencionGrupal_fecha_solicitud" in row and pd.notna(row["IntervencionGrupal_fecha_solicitud"]) and estudiante_id:
                        intervencion_data = {
                            "estudiante_id": estudiante_id,
                            "fecha_solicitud": str(row["IntervencionGrupal_fecha_solicitud"]),
                            "fecha_recepcion": str(row["IntervencionGrupal_fecha_recepcion"]) if pd.notna(row["IntervencionGrupal_fecha_recepcion"]) else None,
                            "estado": str(row["IntervencionGrupal_estado_solicitud"]) if pd.notna(row["IntervencionGrupal_estado_solicitud"]) else "pendiente"
                        }
                        
                        # Insertar la intervención grupal
                        print(f"Creando intervención grupal: {intervencion_data}")
                        supabase.table("intervenciones_grupales").insert(intervencion_data).execute()
                    
                    # 5. Procesar remisiones psicológicas si corresponde
                    if "RemisionPsicologica_fecha_remision" in row and pd.notna(row["RemisionPsicologica_fecha_remision"]) and estudiante_id:
                        remision_psico_data = {
                            "estudiante_id": estudiante_id,
                            "fecha_remision": str(row["RemisionPsicologica_fecha_remision"]),
                            "tipo_remision": str(row["RemisionPsicologica_tipo_remision"]) if pd.notna(row["RemisionPsicologica_tipo_remision"]) else "general"
                        }
                        
                        # Insertar la remisión psicológica
                        print(f"Creando remisión psicológica: {remision_psico_data}")
                        supabase.table("remisiones_psicologicas").insert(remision_psico_data).execute()
                    
                    # Añadir a los datos procesados
                    processed_data.append({
                        "documento": documento,
                        "programa": programa_academico,
                        "estudiante_id": estudiante_id,
                        "procesado": True
                    })
                    
                    inserted += 1
                    
                except Exception as e:
                    error_msg = f"Error en fila {index+1}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)
                    
                    # Añadir a los datos procesados con error
                    processed_data.append({
                        "documento": str(row["estudiante_numero_documento"]) if pd.notna(row["estudiante_numero_documento"]) else "N/A",
                        "programa": str(row["estudiante_programa_academico"]) if pd.notna(row["estudiante_programa_academico"]) else "N/A",
                        "error": str(e),
                        "procesado": False
                    })
        else:
            # Formato no reconocido
            return {
                "success": False,
                "data": [],
                "inserted": 0,
                "error": "Formato de CSV no reconocido. Debe contener al menos las columnas: estudiante_numero_documento, estudiante_programa_academico"
            }
        
        # Retornar respuesta en el formato que espera el frontend
        return {
            "success": True,
            "data": processed_data,  # Enviar los datos procesados
            "inserted": inserted,
            "errors": errors,
            "message": f"Se procesaron {inserted} registros correctamente."
        }
            
    except Exception as e:
        error_msg = f"Error al procesar el archivo CSV: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "data": [],
            "inserted": 0,
            "errors": [error_msg],
            "message": "Ocurrió un error al procesar el archivo CSV. Por favor, verifica el formato e intenta nuevamente."
        }
