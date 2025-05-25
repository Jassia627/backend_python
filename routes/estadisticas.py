from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random

from config import supabase

router = APIRouter()

@router.get("/estadisticas", 
          summary="Obtener estadísticas generales",
          description="Retorna estadísticas generales del sistema de permanencia",
          response_model=Dict[str, Any])
async def get_estadisticas():
    """Obtiene estadísticas generales del sistema de permanencia."""
    try:
        # Obtener datos de estudiantes
        estudiantes = supabase.table("estudiantes").select("*").execute()
        total_estudiantes = len(estudiantes.data) if estudiantes.data else 100  # Valor por defecto si no hay datos
        
        # Obtener datos de servicios
        servicios = supabase.table("servicios").select("*").execute()
        
        # Calcular riesgos (simulado por ahora)
        riesgo_alto = int(total_estudiantes * 0.15)
        riesgo_medio = int(total_estudiantes * 0.25)
        riesgo_bajo = total_estudiantes - riesgo_alto - riesgo_medio
        
        # Datos para RiesgoDesercionChart
        riesgo_desercion_data = [
            {"name": "Alto", "value": riesgo_alto},
            {"name": "Medio", "value": riesgo_medio},
            {"name": "Bajo", "value": riesgo_bajo}
        ]
        
        # Datos para TutoriaDonutChart
        tutoria_data = [
            {"name": "Requieren", "value": int(total_estudiantes * 0.65)},
            {"name": "No requieren", "value": int(total_estudiantes * 0.35)}
        ]
        
        # Datos para VulnerabilidadBarChart
        vulnerabilidad_data = [
            {"name": "Económica", "cantidad": int(total_estudiantes * 0.45)},
            {"name": "Académica", "cantidad": int(total_estudiantes * 0.30)},
            {"name": "Psicosocial", "cantidad": int(total_estudiantes * 0.25)},
            {"name": "Familiar", "cantidad": int(total_estudiantes * 0.20)},
            {"name": "Salud", "cantidad": int(total_estudiantes * 0.15)}
        ]
        
        # Datos para ServiciosBarChart
        servicios_data = [
            {"name": "Tutoría Académica", "cantidad": int(total_estudiantes * 0.40)},
            {"name": "Apoyo Psicológico", "cantidad": int(total_estudiantes * 0.25)},
            {"name": "Comedor", "cantidad": int(total_estudiantes * 0.35)},
            {"name": "Talleres", "cantidad": int(total_estudiantes * 0.20)},
            {"name": "Asesoría", "cantidad": int(total_estudiantes * 0.15)}
        ]
        
        # Datos para ScatterChartPanel (estrato vs inscritos)
        estrato_inscritos = [
            {"estrato": 1, "inscritos": int(total_estudiantes * 0.30)},
            {"estrato": 2, "inscritos": int(total_estudiantes * 0.35)},
            {"estrato": 3, "inscritos": int(total_estudiantes * 0.20)},
            {"estrato": 4, "inscritos": int(total_estudiantes * 0.10)},
            {"estrato": 5, "inscritos": int(total_estudiantes * 0.05)}
        ]
        
        return {
            "totals": {
                "matriculados": total_estudiantes,
                "activos": total_estudiantes,
                "riesgo": riesgo_alto,
                "atendidos": total_estudiantes // 2  # Simulado por ahora
            },
            "riesgo": {
                "alto": riesgo_alto,
                "medio": riesgo_medio,
                "bajo": riesgo_bajo
            },
            "riesgoDesercionData": riesgo_desercion_data,
            "tutoriaData": tutoria_data,
            "vulnerabilidadData": vulnerabilidad_data,
            "serviciosData": servicios_data,
            "estratoInscritos": estrato_inscritos,
            "servicios": [
                {"nombre": servicio["nombre"], "count": 0} for servicio in servicios.data
            ] if servicios.data else [],
            "total_estudiantes": total_estudiantes,
            "estudiantes_riesgo_alto": riesgo_alto,
            "estudiantes_riesgo_medio": riesgo_medio,
            "estudiantes_riesgo_bajo": riesgo_bajo,
            "servicios_mas_usados": [
                {"nombre": servicio["nombre"], "count": 0} for servicio in servicios.data
            ] if servicios.data else []
        }
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/datos-permanencia", 
         summary="Obtener datos de permanencia para gráficos",
         description="Retorna datos para el gráfico de estrato vs servicio")
async def get_datos_permanencia():
    """Obtiene datos para el gráfico de estrato vs servicio."""
    try:
        # Simulamos datos para el gráfico EstratoServicioChart
        # Este componente espera un objeto con la propiedad estrato_servicio
        servicios = ["Tutoría Académica", "Apoyo Psicológico", "Comedor", "Talleres", "Asesoría"]
        estratos = [1, 2, 3, 4, 5, 6]
        
        # Crear datos simulados para estrato_servicio
        estrato_servicio = []
        for servicio in servicios[:4]:  # Limitamos a 4 servicios para el ejemplo
            for estrato in estratos[:4]:  # Limitamos a 4 estratos para el ejemplo
                # Generar un número aleatorio de estudiantes para cada combinación
                cantidad = 5 + (estrato * 2) + (servicios.index(servicio) * 3)
                estrato_servicio.append({
                    "servicio": servicio,
                    "estrato": estrato,
                    "inscritos": cantidad
                })
        
        # Crear datos simulados para programa_riesgo
        programas = ["Ingeniería de Sistemas", "Derecho", "Medicina"]
        niveles_riesgo = ["Alto", "Medio", "Bajo"]
        programa_riesgo = []
        for programa in programas:
            for riesgo in niveles_riesgo:
                cantidad = 10 + (programas.index(programa) * 5) + (niveles_riesgo.index(riesgo) * 3)
                programa_riesgo.append({
                    "programa": programa,
                    "riesgo": riesgo,
                    "cantidad": cantidad
                })
        
        # Devolver el objeto con la estructura esperada
        return {
            "estrato_servicio": estrato_servicio,
            "programa_riesgo": programa_riesgo
        }
    except Exception as e:
        print(f"Error al obtener datos de permanencia: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de permanencia: {str(e)}")
