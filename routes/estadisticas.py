from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import traceback

from config import supabase

router = APIRouter()

# Tabla de permanencia para consultas
TABLA_PERMANENCIA = "permanencia"

@router.get("/estadisticas-generales", 
          summary="Obtener estadísticas generales para el dashboard",
          description="Retorna estadísticas generales del sistema de permanencia",
          response_model=Dict[str, Any])
async def get_estadisticas():
    """Obtiene estadísticas generales para el dashboard."""
    try:
        print(f"Consultando tabla: {TABLA_PERMANENCIA}")
        
        # Consultar datos reales de la tabla de permanencia
        permanencia_data = supabase.table(TABLA_PERMANENCIA).select("*").execute()
        
        if not permanencia_data or not permanencia_data.data:
            print("No se encontraron datos en la tabla permanencia")
            return {
                "totals": {
                    "inscritos": 0,
                    "matriculados": 0,
                    "desertores": 0,
                    "graduados": 0
                },
                "programaStats": [],
                "riesgoDesercionData": [],
                "tutoriaData": [],
                "vulnerabilidadData": [],
                "serviciosData": [],
                "edadDesertores": [],
                "estratoInscritos": []
            }
        
        datos_reales = permanencia_data.data
        total_estudiantes = len(datos_reales)
        print(f"Procesando {total_estudiantes} registros de la base de datos")
        
        # Calcular estadísticas básicas
        estudiantes_inscritos = sum(item.get("inscritos", 0) for item in datos_reales)
        estudiantes_matriculados = sum(item.get("matriculados", 0) for item in datos_reales)
        desertores = sum(item.get("desertores", 0) for item in datos_reales)
        graduados = sum(item.get("graduados", 0) for item in datos_reales)
        
        # Datos para RiesgoDesercionChart
        riesgo_count = {"Alto": 0, "Medio": 0, "Bajo": 0}
        for item in datos_reales:
            riesgo = item.get("riesgo_desercion", "").lower()
            if riesgo in ["alto", "muy alto"]:
                riesgo_count["Alto"] += 1
            elif riesgo == "medio":
                riesgo_count["Medio"] += 1
            elif riesgo in ["bajo", "muy bajo"]:
                riesgo_count["Bajo"] += 1
        
        riesgo_desercion_data = [
            {"riesgo": nivel, "cantidad": count} 
            for nivel, count in riesgo_count.items()
        ]
        
        # Datos para TutoriaDonutChart
        requieren_tutoria = sum(1 for item in datos_reales if item.get("requiere_tutoria", "").lower() == "sí")
        no_requieren_tutoria = total_estudiantes - requieren_tutoria
        
        tutoria_data = [
            {"name": "Requieren", "value": requieren_tutoria},
            {"name": "No requieren", "value": no_requieren_tutoria}
        ]
        
        # Datos para VulnerabilidadBarChart
        vulnerabilidad_count = {}
        for item in datos_reales:
            tipo = item.get("tipo_vulnerabilidad")
            if tipo:
                vulnerabilidad_count[tipo] = vulnerabilidad_count.get(tipo, 0) + 1
        
        vulnerabilidad_data = [
            {"name": tipo, "cantidad": count} 
            for tipo, count in vulnerabilidad_count.items()
        ]
        
        # Datos para ServiciosBarChart
        servicios_count = {}
        for item in datos_reales:
            servicio = item.get("servicio")
            if servicio:
                servicios_count[servicio] = servicios_count.get(servicio, 0) + 1
        
        servicios_data = [
            {"name": servicio, "cantidad": count} 
            for servicio, count in servicios_count.items()
        ]
        
        # Datos para ScatterChartPanel (estrato vs inscritos)
        estrato_count = {}
        for item in datos_reales:
            try:
                estrato = int(item.get("estrato", 0))
                inscritos = int(item.get("inscritos", 0))
                if estrato > 0:
                    if estrato not in estrato_count:
                        estrato_count[estrato] = 0
                    estrato_count[estrato] += inscritos
            except (ValueError, TypeError):
                continue
        
        estrato_inscritos = [
            {"estrato": estrato, "inscritos": count} 
            for estrato, count in estrato_count.items()
        ]
        
        # Datos para el gráfico de programas (top 5)
        programa_count = {}
        for item in datos_reales:
            programa = item.get("estudiante_programa_academico")
            if programa:
                programa_count[programa] = programa_count.get(programa, 0) + 1
        
        programa_stats = [
            {"programa": programa, "value": count} 
            for programa, count in programa_count.items()
        ]
        programa_stats.sort(key=lambda x: x["value"], reverse=True)
        
        # Limitar a top 5 programas
        if len(programa_stats) > 5:
            programa_stats = programa_stats[:5]
        
        # Para edades de desertores necesitarías una columna edad en tu tabla
        # Por ahora devolvemos array vacío
        edad_desertores = []
        
        return {
            "totals": {
                "inscritos": estudiantes_inscritos,
                "matriculados": estudiantes_matriculados,
                "desertores": desertores,
                "graduados": graduados
            },
            "programaStats": programa_stats,
            "riesgoDesercionData": riesgo_desercion_data,
            "tutoriaData": tutoria_data,
            "vulnerabilidadData": vulnerabilidad_data,
            "serviciosData": servicios_data,
            "edadDesertores": edad_desertores,
            "estratoInscritos": estrato_inscritos
        }
        
    except Exception as e:
        print(f"Error en get_estadisticas: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/datos-permanencia", 
          summary="Obtener datos para el gráfico de Estrato por Servicio",
          description="Retorna datos para el gráfico de distribución de estratos por servicio")
async def get_datos_permanencia():
    """Obtiene datos para el gráfico de estrato vs servicio."""
    try:
        print(f"Consultando tabla: {TABLA_PERMANENCIA}")
        
        # Consultar datos reales de la tabla de permanencia
        permanencia_data = supabase.table(TABLA_PERMANENCIA).select("*").execute()
        
        if not permanencia_data or not hasattr(permanencia_data, 'data') or not permanencia_data.data:
            print("No se encontraron datos en la tabla permanencia")
            return []
        
        print(f"Devolviendo {len(permanencia_data.data)} registros de la base de datos")
        return permanencia_data.data
        
    except Exception as e:
        print(f"Error en get_datos_permanencia: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de permanencia: {str(e)}")

@router.get("/estrato-servicio")
async def get_estrato_servicio():
    """Obtiene datos para el gráfico de Estrato por Servicio."""
    try:
        print(f"Consultando tabla: {TABLA_PERMANENCIA}")
        
        # Consultar datos reales
        permanencia_data = supabase.table(TABLA_PERMANENCIA).select("*").execute()
        
        if not permanencia_data or not permanencia_data.data:
            print("No se encontraron datos en la tabla permanencia")
            return []
        
        # Agrupar datos por servicio y estrato
        estrato_servicio = {}
        
        for item in permanencia_data.data:
            servicio = item.get("servicio")
            estrato = item.get("estrato")
            inscritos = item.get("inscritos", 0)
            
            if servicio and estrato:
                key = f"{servicio}_{estrato}"
                if key not in estrato_servicio:
                    estrato_servicio[key] = {
                        "servicio": servicio,
                        "estrato": estrato,
                        "cantidad": 0
                    }
                estrato_servicio[key]["cantidad"] += inscritos
        
        return list(estrato_servicio.values())
        
    except Exception as e:
        print(f"Error en get_estrato_servicio: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de estrato por servicio: {str(e)}")

# Alias para mantener compatibilidad
@router.get("/estadisticas")
async def get_estadisticas_alias():
    """Alias para el endpoint de estadísticas generales."""
    return await get_estadisticas()