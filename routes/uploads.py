from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any, List
import io
import pandas as pd
import uuid
import traceback
from datetime import datetime

from config import supabase

# Función para convertir fechas de formato DD-MM-YYYY a YYYY-MM-DD
def convert_date_format(date_str):
    if not date_str or pd.isna(date_str):
        return None
    try:
        # Intentar varios formatos de fecha
        formats = [
            '%d-%m-%Y', '%d/%m/%Y', '%d-%b-%Y', '%d %b %Y',  # Formatos estándar
            '%Y-%m-%d',  # ISO
            '%d-%B-%Y', '%d %B %Y',  # Con nombre de mes completo
            '%d-%b-%y', '%d %b %y',  # Con año de 2 dígitos
            '%B %d, %Y', '%b %d, %Y',  # Formato tipo 'January 01, 2020'
            '%d-%m-%y', '%d/%m/%y',  # Formato con año de 2 dígitos
            '%m-%d-%Y', '%m/%d/%Y',  # Formato americano
            '%Y/%m/%d',  # Formato ISO con /
            '%d-%m-%Y %H:%M:%S',  # Con hora
            '%Y-%m-%d %H:%M:%S',  # ISO con hora
        ]
        
        # Si el formato parece ser 'DD-MMM-YYYY' (ej: 25-Dec-2024)
        if isinstance(date_str, str) and len(date_str) >= 9:
            # Intentar convertir meses en inglés
            month_map = {
                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
                'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            
            parts = date_str.replace(',', '').split('-')
            if len(parts) == 3:
                day, month, year = parts
                month_lower = month.lower()
                if month_lower in month_map:
                    try:
                        new_date = f"{year}-{month_map[month_lower]}-{day.zfill(2)}"
                        return new_date
                    except:
                        pass
        
        # Probar todos los formatos estándar
        for fmt in formats:
            try:
                date_obj = datetime.strptime(str(date_str), fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # Si ninguno funciona, intentar extraer año, mes y día con expresiones regulares
        import re
        if isinstance(date_str, str):
            # Buscar patrones como DD-MM-YYYY o YYYY-MM-DD
            date_pattern = re.compile(r'(\d{1,4})[-/\s](\d{1,2}|[a-zA-Z]{3,9})[-/\s](\d{1,4})')
            match = date_pattern.search(date_str)
            
            if match:
                part1, part2, part3 = match.groups()
                
                # Determinar qué parte es el año
                if len(part1) == 4 and part1.isdigit() and int(part1) > 1900:
                    year = part1
                    month = part2
                    day = part3
                elif len(part3) == 4 and part3.isdigit() and int(part3) > 1900:
                    year = part3
                    month = part2
                    day = part1
                else:
                    # Asumir formato DD-MM-YYYY
                    day = part1
                    month = part2
                    year = part3
                    if len(year) == 2:  # Año con 2 dígitos
                        year = f"20{year}" if int(year) < 50 else f"19{year}"
                
                # Convertir mes si es texto
                if not month.isdigit():
                    month_lower = month.lower()
                    if month_lower in month_map:
                        month = month_map[month_lower]
                    else:
                        # No se pudo convertir el mes
                        return None
                
                # Asegurarse de que día y mes tengan 2 dígitos
                day = day.zfill(2)
                month = month.zfill(2)
                
                return f"{year}-{month}-{day}"
        
        # Si todo falla, devolver None
        print(f"No se pudo convertir la fecha: {date_str}")
        return None
    except Exception as e:
        print(f"Error al convertir fecha {date_str}: {str(e)}")
        return None

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
            
            # Primero verificar la estructura de la tabla estudiantes
            try:
                # Verificar si la tabla estudiantes existe y tiene las columnas necesarias
                table_info = supabase.table("estudiantes").select("*").limit(1).execute()
                
                # Si llegamos aquí, la tabla existe, pero necesitamos verificar sus columnas
                # Esto lo haremos indirectamente intentando obtener la estructura
                print("Tabla estudiantes encontrada, verificando estructura...")
                
                # Obtener un registro para ver la estructura
                if table_info.data and len(table_info.data) > 0:
                    print(f"Estructura de la tabla estudiantes: {list(table_info.data[0].keys())}")
                    
                    # Guardar las columnas disponibles para usarlas después
                    columnas_disponibles = list(table_info.data[0].keys())
                else:
                    print("No se encontraron registros en la tabla estudiantes")
                    columnas_disponibles = ["id", "documento", "tipo_documento", "nombres", "apellidos", "correo", "programa_academico", "semestre"]
            except Exception as e:
                print(f"Error al verificar la tabla estudiantes: {str(e)}")
                # Podría ser que la tabla no existe o hay otro problema
                columnas_disponibles = ["id", "documento", "tipo_documento", "nombres", "apellidos", "correo", "programa_academico", "semestre"]
            
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
                                    "codigo": f"PROG-{len(programa_academico)}-{str(uuid.uuid4())[:8]}",
                                    "nivel": "Pregrado"  # Valor por defecto para el campo obligatorio
                                }
                                programa_response = supabase.table("programas").insert(nuevo_programa).execute()
                                programa_id = programa_response.data[0]["id"]
                        
                        # Crear el estudiante - Usar solo campos que sabemos que existen
                        # Extraer el semestre si está disponible en el CSV
                        semestre = None
                        if "estudiante_semestre" in row and pd.notna(row["estudiante_semestre"]):
                            try:
                                semestre = int(row["estudiante_semestre"])
                            except:
                                semestre = 1
                        else:
                            semestre = 1  # Valor por defecto
                            
                        # Generar un nombre y apellido más realistas basados en el documento
                        nombre_generado = f"Estudiante_{documento[:4]}" if len(str(documento)) >= 4 else f"Estudiante_{documento}"
                        apellido_generado = f"Apellido_{documento[-4:]}" if len(str(documento)) >= 4 else f"Apellido_{documento}"
                        
                        estudiante_data = {
                            "documento": documento,
                            "tipo_documento": "CC",  # Valor por defecto
                            "nombres": nombre_generado,
                            "apellidos": apellido_generado,
                            "correo": f"{documento}@universidad.edu.co",
                            "programa_academico": programa_academico or "Programa no especificado",
                            "semestre": semestre,
                            "telefono": f"300{documento[-7:]}" if len(str(documento)) >= 7 else "3001234567",
                            "direccion": f"Calle {documento[:2]} # {documento[-2:]}-{documento[2:4]}" if len(str(documento)) >= 4 else "Dirección por defecto"
                        }
                        
                        # Agregar programa_id si existe la columna
                        if "programa_id" in columnas_disponibles and programa_id:
                            estudiante_data["programa_id"] = programa_id
                        
                        # Agregar campos adicionales si están disponibles en la tabla
                        if "semestre" in columnas_disponibles and "estudiante_semestre" in row and pd.notna(row["estudiante_semestre"]):
                            try:
                                estudiante_data["semestre"] = int(row["estudiante_semestre"])
                            except:
                                estudiante_data["semestre"] = 1
                        
                        if "estrato" in columnas_disponibles and "estudiante_estrato" in row and pd.notna(row["estudiante_estrato"]):
                            try:
                                estudiante_data["estrato"] = int(row["estudiante_estrato"])
                            except:
                                estudiante_data["estrato"] = 1
                        
                        if "riesgo_desercion" in columnas_disponibles and "estudiante_riesgo_desercion" in row and pd.notna(row["estudiante_riesgo_desercion"]):
                            estudiante_data["riesgo_desercion"] = str(row["estudiante_riesgo_desercion"]).lower()
                        
                        # Crear el estudiante
                        print(f"Creando nuevo estudiante: {estudiante_data}")
                        try:
                            estudiante_response = supabase.table("estudiantes").insert(estudiante_data).execute()
                            if estudiante_response.data and len(estudiante_response.data) > 0:
                                estudiante_id = estudiante_response.data[0]["id"]
                                print(f"Estudiante creado con ID: {estudiante_id}")
                            else:
                                print(f"Error al crear estudiante, respuesta vacía")
                                raise Exception("No se pudo crear el estudiante, respuesta vacía")
                        except Exception as e:
                            print(f"Error en fila {index+1}: {e}")
                            if hasattr(e, 'json'):
                                error_json = e.json()
                                print(f"Error en fila {index+1}: {error_json}")
                            raise e
                    
                    # 2. Procesar datos de POVAU si corresponde
                    if "POVAU_tipo_participante" in row and pd.notna(row["POVAU_tipo_participante"]) and estudiante_id:
                        try:
                            povau_data = {
                                "estudiante_id": estudiante_id,
                                "tipo_participante": str(row["POVAU_tipo_participante"]),
                                "fecha_ingreso": convert_date_format(row["POVAU_fecha_ingreso_programa"]) if pd.notna(row["POVAU_fecha_ingreso_programa"]) else None
                            }
                            
                            # Insertar en POVAU
                            print(f"Creando registro POVAU: {povau_data}")
                            supabase.table("povau").insert(povau_data).execute()
                            print("Registro POVAU creado correctamente")
                        except Exception as e:
                            print(f"Error al crear registro POVAU: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 3. Procesar datos de POA si corresponde
                    if "POA_ciclo_formacion" in row and pd.notna(row["POA_ciclo_formacion"]) and estudiante_id:
                        try:
                            # 1. Procesar datos de tipo_remision y fecha_remision si corresponde
                            # Estos campos están en el nivel principal del CSV, no dentro de una entidad específica
                            # Por ahora, solo los guardamos para usarlos más adelante si es necesario
                            tipo_remision = str(row["tipo_remision"]) if "tipo_remision" in row and pd.notna(row["tipo_remision"]) else None
                            fecha_remision = convert_date_format(row["fecha_remision"]) if "fecha_remision" in row and pd.notna(row["fecha_remision"]) else None
                            
                            # Guardar todos los campos del CSV para usarlos más adelante
                            csv_data = {}
                            for col in row.index:
                                if pd.notna(row[col]):
                                    csv_data[col] = row[col]
                            
                            poa_data = {
                                "estudiante_id": estudiante_id,
                                "ciclo_formacion": str(row["POA_ciclo_formacion"]),
                                "nombre_asignatura": str(row["POA_nombre_asignatura"]) if pd.notna(row["POA_nombre_asignatura"]) else None,
                                "fecha": convert_date_format(row["POA_fecha"]) if pd.notna(row["POA_fecha"]) else None
                            }
                            
                            # Insertar en POA
                            print(f"Creando registro POA: {poa_data}")
                            supabase.table("poa").insert(poa_data).execute()
                            print("Registro POA creado correctamente")
                        except Exception as e:
                            print(f"Error al crear registro POA: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 4. Procesar datos de Comedor Universitario si corresponde
                    if "ComedorUniversitario_condicion_socioeconomica" in row and pd.notna(row["ComedorUniversitario_condicion_socioeconomica"]) and estudiante_id:
                        try:
                            # Obtener datos del estudiante para completar campos obligatorios
                            estudiante_info = supabase.table("estudiantes").select("*").eq("id", estudiante_id).execute()
                            nombre_estudiante = ""
                            if estudiante_info.data and len(estudiante_info.data) > 0:
                                nombre_estudiante = f"{estudiante_info.data[0].get('nombres', '')} {estudiante_info.data[0].get('apellidos', '')}"
                            
                            # Determinar la condición socioeconómica
                            condicion_socioeconomica = str(row["ComedorUniversitario_condicion_socioeconomica"]).lower() if pd.notna(row.get("ComedorUniversitario_condicion_socioeconomica")) else "media"
                            
                            # Determinar el tipo de subsidio basado en la condición socioeconómica
                            tipo_subsidio_map = {
                                "baja": "Completo",
                                "media": "Parcial",
                                "alta": "Regular"
                            }
                            tipo_subsidio = tipo_subsidio_map.get(condicion_socioeconomica, "Regular")
                            
                            # Determinar el tipo de comida basado en la fecha de solicitud
                            fecha_solicitud = convert_date_format(row["ComedorUniversitario_fecha_solicitud"]) if pd.notna(row.get("ComedorUniversitario_fecha_solicitud")) else datetime.now().strftime('%Y-%m-%d')
                            
                            # Determinar el número de raciones asignadas basado en el estrato
                            estrato = int(row["estudiante_estrato"]) if pd.notna(row.get("estudiante_estrato")) else 1
                            raciones_asignadas = 1 if estrato > 3 else 2
                            
                            # Determinar el periodo académico
                            periodo_academico = str(row["RegistroBeneficio_periodo_academico_beneficiado"]) if pd.notna(row.get("RegistroBeneficio_periodo_academico_beneficiado")) else "2023-1"
                            
                            # Obtener el semestre del estudiante
                            semestre_estudiante = str(row["estudiante_semestre"]) if pd.notna(row.get("estudiante_semestre")) else "1"
                            
                            # Crear observaciones detalladas
                            observaciones = f"Estudiante de estrato {estrato}, programa {programa_academico}, semestre {semestre_estudiante}. "
                            observaciones += f"Condición socioeconómica: {condicion_socioeconomica}. Importado desde CSV."
                            
                            comedor_data = {
                                "estudiante_id": estudiante_id,
                                "condicion_socioeconomica": condicion_socioeconomica,
                                "fecha_solicitud": fecha_solicitud,
                                "aprobado": bool(row["ComedorUniversitario_aprobado"]) if pd.notna(row.get("ComedorUniversitario_aprobado")) else False,
                                "tipo_comida": "Almuerzo",  # Campo obligatorio
                                "raciones_asignadas": raciones_asignadas,
                                "observaciones": observaciones,
                                "tipo_subsidio": tipo_subsidio,
                                "periodo_academico": periodo_academico,
                                "estrato": estrato
                            }
                            
                            # Insertar en Comedor
                            print(f"Creando registro Comedor con tipo_comida: {comedor_data}")
                            supabase.table("comedor_universitario").insert(comedor_data).execute()
                            print("Registro Comedor creado correctamente")
                        except Exception as e:
                            print(f"Error al crear registro Comedor: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 5. Procesar datos de Registro de Beneficio si corresponde
                    if "RegistroBeneficio_fecha_inscripcion" in row and pd.notna(row["RegistroBeneficio_fecha_inscripcion"]) and estudiante_id:
                        try:
                            beneficio_data = {
                                "estudiante_id": estudiante_id,
                                "fecha_inscripcion": convert_date_format(row["RegistroBeneficio_fecha_inscripcion"]),
                                "estado_solicitud": bool(row["RegistroBeneficio_estado_solicitud"]) if pd.notna(row["RegistroBeneficio_estado_solicitud"]) else False,
                                "periodo_academico": str(row["RegistroBeneficio_periodo_academico_beneficiado"]) if pd.notna(row["RegistroBeneficio_periodo_academico_beneficiado"]) else None,
                                "fecha_inicio": convert_date_format(row["RegistroBeneficio_fecha_inicio_servicio"]) if pd.notna(row["RegistroBeneficio_fecha_inicio_servicio"]) else None,
                                "fecha_finalizacion": convert_date_format(row["RegistroBeneficio_fecha_finalizacion_servicio"]) if pd.notna(row["RegistroBeneficio_fecha_finalizacion_servicio"]) else None
                            }
                            
                            # Insertar el registro de beneficio
                            print(f"Creando registro de beneficio: {beneficio_data}")
                            supabase.table("registro_beneficios").insert(beneficio_data).execute()
                            print("Registro de beneficio creado correctamente")
                        except Exception as e:
                            print(f"Error al crear registro de beneficio: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 6. Procesar datos de Solicitud de Atención Individual si corresponde
                    if "SolicitudAtencionIndividual_fecha_atencion" in row and pd.notna(row["SolicitudAtencionIndividual_fecha_atencion"]) and estudiante_id:
                        try:
                            atencion_data = {
                                "estudiante_id": estudiante_id,
                                "fecha_atencion": convert_date_format(row["SolicitudAtencionIndividual_fecha_atencion"]),
                                "motivo_atencion": str(row["SolicitudAtencionIndividual_motivo_atencion"]) if pd.notna(row["SolicitudAtencionIndividual_motivo_atencion"]) else "general"
                            }
                            
                            # Insertar la solicitud de atención
                            print(f"Creando solicitud de atención: {atencion_data}")
                            supabase.table("solicitudes_atencion").insert(atencion_data).execute()
                            print("Solicitud de atención creada correctamente")
                        except Exception as e:
                            print(f"Error al crear solicitud de atención: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 7. Procesar datos de Intervención Grupal si corresponde
                    if "IntervencionGrupal_fecha_solicitud" in row and pd.notna(row["IntervencionGrupal_fecha_solicitud"]) and estudiante_id:
                        try:
                            # Crear un diccionario con todos los campos posibles de intervenciones grupales
                            intervencion_data = {
                                "estudiante_id": estudiante_id,
                                "fecha_solicitud": convert_date_format(row["IntervencionGrupal_fecha_solicitud"]) or datetime.now().strftime('%Y-%m-%d'),
                                "fecha_recepcion": convert_date_format(row["IntervencionGrupal_fecha_recepcion"]) if pd.notna(row.get("IntervencionGrupal_fecha_recepcion")) else None,
                                "nombre_docente_permanencia": str(row["IntervencionGrupal_nombre_docente_permanencia"]) if pd.notna(row.get("IntervencionGrupal_nombre_docente_permanencia")) else "Docente por defecto",
                                "celular_permanencia": str(row["IntervencionGrupal_celular_permanencia"]) if pd.notna(row.get("IntervencionGrupal_celular_permanencia")) else "0000000000",
                                "correo_permanencia": str(row["IntervencionGrupal_correo_permanencia"]) if pd.notna(row.get("IntervencionGrupal_correo_permanencia")) else f"permanencia_{estudiante_id}@ejemplo.com",
                                "estudiante_programa_academico_permanencia": str(row["IntervencionGrupal_programa_permanencia"]) if pd.notna(row.get("IntervencionGrupal_programa_permanencia")) else programa_academico or "Programa no especificado",
                                "tipo_poblacion": str(row["IntervencionGrupal_tipo_poblacion"]) if pd.notna(row.get("IntervencionGrupal_tipo_poblacion")) else "General",
                                "nombre_docente_asignatura": str(row["IntervencionGrupal_nombre_docente_asignatura"]) if pd.notna(row.get("IntervencionGrupal_nombre_docente_asignatura")) else "Docente asignatura",
                                "celular_docente_asignatura": str(row["IntervencionGrupal_celular_docente_asignatura"]) if pd.notna(row.get("IntervencionGrupal_celular_docente_asignatura")) else "0000000000",
                                "correo_docente_asignatura": str(row["IntervencionGrupal_correo_docente_asignatura"]) if pd.notna(row.get("IntervencionGrupal_correo_docente_asignatura")) else f"docente_{estudiante_id}@ejemplo.com",
                                "estudiante_programa_academico_docente_asignatura": str(row["IntervencionGrupal_programa_docente_asignatura"]) if pd.notna(row.get("IntervencionGrupal_programa_docente_asignatura")) else programa_academico or "Programa no especificado",
                                "asignatura_intervenir": str(row["IntervencionGrupal_asignatura_intervenir"]) if pd.notna(row.get("IntervencionGrupal_asignatura_intervenir")) else "Asignatura general",
                                "grupo": str(row["IntervencionGrupal_grupo"]) if pd.notna(row.get("IntervencionGrupal_grupo")) else "1",
                                "semestre": str(row["IntervencionGrupal_semestre"]) if pd.notna(row.get("IntervencionGrupal_semestre")) else str(row.get("estudiante_semestre", "1")) if pd.notna(row.get("estudiante_semestre")) else "1",
                                "numero_estudiantes": str(row["IntervencionGrupal_numero_estudiantes"]) if pd.notna(row.get("IntervencionGrupal_numero_estudiantes")) else "1",
                                "tematica_sugerida": str(row["IntervencionGrupal_tematica_sugerida"]) if pd.notna(row.get("IntervencionGrupal_tematica_sugerida")) else None,
                                "fecha_estudiante_programa_academicoda": convert_date_format(row["IntervencionGrupal_fecha_programada"]) if pd.notna(row.get("IntervencionGrupal_fecha_programada")) else datetime.now().strftime('%Y-%m-%d'),
                                "hora": str(row["IntervencionGrupal_hora"]) if pd.notna(row.get("IntervencionGrupal_hora")) else "08:00",
                                "aula": str(row["IntervencionGrupal_aula"]) if pd.notna(row.get("IntervencionGrupal_aula")) else "Aula por asignar",
                                "bloque": str(row["IntervencionGrupal_bloque"]) if pd.notna(row.get("IntervencionGrupal_bloque")) else "Bloque por asignar",
                                "sede": str(row["IntervencionGrupal_sede"]) if pd.notna(row.get("IntervencionGrupal_sede")) else "Sede principal",
                                "estado": str(row["IntervencionGrupal_estado"]) if pd.notna(row.get("IntervencionGrupal_estado")) else "espera",
                                "motivo": str(row["IntervencionGrupal_motivo"]) if pd.notna(row.get("IntervencionGrupal_motivo")) else None,
                                "efectividad": str(row["IntervencionGrupal_efectividad"]) if pd.notna(row.get("IntervencionGrupal_efectividad")) else "Pendiente evaluación"
                            }
                            
                            # Si el estado no es "se hizo" y no hay motivo, establecer un motivo por defecto
                            if intervencion_data.get("estado") != "se hizo" and not intervencion_data.get("motivo"):
                                intervencion_data["motivo"] = "Importado desde CSV"
                            
                            # Insertar la intervención grupal
                            print(f"Creando intervención grupal: {intervencion_data}")
                            supabase.table("intervenciones_grupales").insert(intervencion_data).execute()
                            print("Intervención grupal creada correctamente")
                        except Exception as e:
                            print(f"Error al crear intervención grupal: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 8. Procesar remisiones psicológicas si corresponde
                    if "RemisionPsicologica_fecha_remision" in row and pd.notna(row["RemisionPsicologica_fecha_remision"]) and estudiante_id:
                        try:
                            # Obtener datos del estudiante para completar campos obligatorios
                            estudiante_info = supabase.table("estudiantes").select("*").eq("id", estudiante_id).execute()
                            nombre_estudiante = ""
                            numero_documento = ""
                            programa_academico = ""
                            semestre = "1"
                            
                            if estudiante_info.data and len(estudiante_info.data) > 0:
                                nombre_estudiante = f"{estudiante_info.data[0].get('nombres', '')} {estudiante_info.data[0].get('apellidos', '')}"
                                numero_documento = estudiante_info.data[0].get('documento', '')
                                programa_academico = estudiante_info.data[0].get('programa_academico', '')
                                semestre = str(estudiante_info.data[0].get('semestre', '1'))
                            else:
                                # Si no se encuentra el estudiante, usar datos del CSV
                                nombre_estudiante = f"Estudiante {row['estudiante_numero_documento']}" if pd.notna(row.get('estudiante_numero_documento')) else "Estudiante sin nombre"
                                numero_documento = str(row['estudiante_numero_documento']) if pd.notna(row.get('estudiante_numero_documento')) else "0000000000"
                                programa_academico = str(row['estudiante_programa_academico']) if pd.notna(row.get('estudiante_programa_academico')) else "No especificado"
                                semestre = str(row['estudiante_semestre']) if pd.notna(row.get('estudiante_semestre')) else "1"
                            
                            # Determinar el tipo de remisión
                            tipo_remision_psico = str(row["RemisionPsicologica_tipo_remision"]) if pd.notna(row.get("RemisionPsicologica_tipo_remision")) else \
                                                str(row["tipo_remision"]) if pd.notna(row.get("tipo_remision")) else "individual"
                            
                            # Determinar la fecha de remisión
                            fecha_remision_psico = convert_date_format(row["RemisionPsicologica_fecha_remision"]) if pd.notna(row.get("RemisionPsicologica_fecha_remision")) else \
                                                 convert_date_format(row["fecha_remision"]) if pd.notna(row.get("fecha_remision")) else datetime.now().strftime('%Y-%m-%d')
                            
                            # Determinar el motivo de remisión basado en el tipo
                            motivo_map = {
                                "academica": "Dificultades académicas",
                                "tutorias": "Solicitud de tutorías",
                                "asesoria": "Necesita asesoría",
                                "asesorias": "Necesita asesoría especializada"
                            }
                            
                            motivo_remision = motivo_map.get(tipo_remision_psico.lower(), "Importado desde CSV")
                            
                            remision_psico_data = {
                                "estudiante_id": estudiante_id,
                                "nombre_estudiante": nombre_estudiante,
                                "numero_documento": numero_documento,
                                "programa_academico": programa_academico,
                                "semestre": semestre,
                                "motivo_remision": motivo_remision,
                                "docente_remite": "Docente " + programa_academico[:10] if programa_academico else "Docente CSV",
                                "correo_docente": f"docente_{programa_academico.lower().replace(' ', '_')[:10]}@universidad.edu.co" if programa_academico else "docente_csv@universidad.edu.co",
                                "telefono_docente": f"301{numero_documento[-7:]}" if len(str(numero_documento)) >= 7 else "3011234567",
                                "fecha": fecha_remision_psico,
                                "hora": "12:00",
                                "tipo_remision": tipo_remision_psico,
                                "fecha_remision": fecha_remision_psico,
                                "observaciones": f"Estudiante de {programa_academico}, semestre {semestre}. Remisión importada automáticamente desde CSV."
                            }
                            
                            # Insertar la remisión psicológica
                            print(f"Creando remisión psicológica con todos los campos obligatorios: {remision_psico_data}")
                            supabase.table("remisiones_psicologicas").insert(remision_psico_data).execute()
                            print("Remisión psicológica creada correctamente")
                        except Exception as e:
                            print(f"Error al crear remisión psicológica: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 9. Procesar formato de asistencia si corresponde
                    if "FormatoAsistencia_numero_asistencia" in row and pd.notna(row["FormatoAsistencia_numero_asistencia"]) and estudiante_id:
                        try:
                            asistencia_data = {
                                "estudiante_id": estudiante_id,
                                "numero_asistencia": int(row["FormatoAsistencia_numero_asistencia"]) if pd.notna(row["FormatoAsistencia_numero_asistencia"]) else 1,
                                "fecha": convert_date_format(row["FormatoAsistencia_fecha"]) if pd.notna(row["FormatoAsistencia_fecha"]) else None
                            }
                            
                            # Insertar el formato de asistencia
                            print(f"Creando formato de asistencia: {asistencia_data}")
                            supabase.table("formatos_asistencia").insert(asistencia_data).execute()
                            print("Formato de asistencia creado correctamente")
                        except Exception as e:
                            print(f"Error al crear formato de asistencia: {str(e)}")
                            # No interrumpir el proceso si falla la creación del registro
                    
                    # 10. Procesar datos de permanencia
                    # Crear un registro en la tabla permanencia para estadísticas
                    try:
                        # Determinar el tipo de vulnerabilidad
                        tipo_vulnerabilidad = str(row["estudiante_tipo_vulnerabilidad"]) if pd.notna(row.get("estudiante_tipo_vulnerabilidad")) else "Académica"
                        
                        permanencia_data = {
                            "servicio": "POA" if pd.notna(row.get("POA_ciclo_formacion")) else 
                                      "POVAU" if pd.notna(row.get("POVAU_tipo_participante")) else
                                      "Comedor" if pd.notna(row.get("ComedorUniversitario_condicion_socioeconomica")) else
                                      "POPS" if pd.notna(row.get("RemisionPsicologica_fecha_remision")) else
                                      "Intervención Grupal" if pd.notna(row.get("IntervencionGrupal_fecha_solicitud")) else
                                      "Atención Individual" if pd.notna(row.get("SolicitudAtencionIndividual_fecha_atencion")) else
                                      "Otro",
                            "estrato": int(row["estudiante_estrato"]) if pd.notna(row.get("estudiante_estrato")) else 1,
                            "inscritos": 1,  # Cada registro representa un estudiante inscrito
                            "estudiante_programa_academico": programa_academico,
                            "riesgo_desercion": str(row["estudiante_riesgo_desercion"]).lower() if pd.notna(row.get("estudiante_riesgo_desercion")) else "bajo",
                            "tipo_vulnerabilidad": tipo_vulnerabilidad,
                            "periodo": str(row["RegistroBeneficio_periodo_academico_beneficiado"]) if pd.notna(row.get("RegistroBeneficio_periodo_academico_beneficiado")) else "2023-1",
                            "semestre": int(row["estudiante_semestre"]) if pd.notna(row.get("estudiante_semestre")) else 1,
                            "matriculados": 1,  # Por defecto, asumimos que están matriculados
                            "desertores": 0,  # Por defecto, no son desertores
                            "graduados": 0,  # Por defecto, no son graduados
                            "requiere_tutoria": "Sí" if str(row.get("estudiante_riesgo_desercion", "")).lower() in ["alto", "muy alto"] else "No"
                        }
                        
                        # Insertar en la tabla permanencia
                        print(f"Creando registro de permanencia: {permanencia_data}")
                        supabase.table("permanencia").insert(permanencia_data).execute()
                    except Exception as e:
                        print(f"Error al crear registro de permanencia: {str(e)}")
                        # No interrumpir el proceso si falla la creación del registro de permanencia
                    
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
                    print(f"Traceback: {traceback.format_exc()}")
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
        print(f"Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "data": [],
            "inserted": 0,
            "errors": [error_msg],
            "message": "Ocurrió un error al procesar el archivo CSV. Por favor, verifica el formato e intenta nuevamente."
        }
