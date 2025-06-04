"""
Script de prueba para verificar el funcionamiento del endpoint de comedor universitario
"""
import requests
import json
from datetime import datetime

# URL base del API
BASE_URL = "http://127.0.0.1:8001/api"

def test_get_comedores():
    """Prueba obtener todos los registros de comedor universitario"""
    print("🔍 Probando GET /api/comedor...")
    try:
        response = requests.get(f"{BASE_URL}/comedor", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error al obtener comedores: {str(e)}")
        return False

def test_create_comedor():
    """Prueba crear un nuevo registro de comedor universitario"""
    print("\n📝 Probando POST /api/comedor...")
    
    # Datos de prueba para crear un registro de comedor
    datos_prueba = {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
        "nombres": "Juan Carlos",
        "apellidos": "Pérez García",
        "correo": "juan.perez@test.com",
        "telefono": "3001234567",
        "direccion": "Calle 123 #45-67",
        "programa_academico": "INGENIERÍA DE SISTEMAS",
        "semestre": 5,
        "estrato": 2,
        "riesgo_desercion": "Medio",
        "condicion_socioeconomica": "Estrato 2",
        "fecha_solicitud": datetime.now().strftime('%Y-%m-%d'),
        "aprobado": True,
        "tipo_comida": "Almuerzo",
        "raciones_asignadas": 30,
        "observaciones": "Estudiante con necesidad socioeconómica verificada",
        "tipo_subsidio": "Completo",
        "periodo_academico": "2024-1"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/comedor", 
            json=datos_prueba,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error al crear comedor: {str(e)}")
        return False

def test_minimal_comedor():
    """Prueba crear un registro de comedor con datos mínimos"""
    print("\n📝 Probando POST /api/comedor con datos mínimos...")
    
    # Datos mínimos requeridos
    datos_minimos = {
        "tipo_documento": "CC",
        "numero_documento": "9876543210",
        "nombres": "María Elena",
        "apellidos": "López Rodríguez",
        "correo": "maria.lopez@test.com",
        "programa_academico": "ADMINISTRACIÓN DE EMPRESAS",
        "condicion_socioeconomica": "Estrato 1"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/comedor", 
            json=datos_minimos,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error al crear comedor con datos mínimos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del endpoint de Comedor Universitario\n")
    
    # Ejecutar pruebas
    resultados = []
    
    resultados.append(("GET Comedores", test_get_comedores()))
    resultados.append(("POST Comedor Completo", test_create_comedor()))
    resultados.append(("POST Comedor Mínimo", test_minimal_comedor()))
    
    # Mostrar resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    for nombre, exito in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{nombre}: {estado}")
    
    total_exitosos = sum(1 for _, exito in resultados if exito)
    print(f"\nTotal: {total_exitosos}/{len(resultados)} pruebas exitosas") 