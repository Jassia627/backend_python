"""
Script para generar datos de muestra en la tabla permanencia.
Este script genera datos aleatorios para la tabla de permanencia
y los inserta en la base de datos Supabase.
"""

import random
import sys
import os

# Añadir el directorio raíz al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import supabase

# Constantes
SERVICIOS = [
    "POA",
    "POVAU",
    "Comedor",
    "POPS",
    "Intervención Grupal",
    "Atención Individual"
]

ESTRATOS = [1, 2, 3, 4, 5, 6]

PROGRAMAS = [
    "LICENCIATURA EN LITERATURA Y LENGUA CASTELLANA",
    "ENFERMERÍA",
    "CONTADURIA PUBLICA",
    "MUSICA",
    "INGENIERÍA AGROINDUSTRIAL",
    "LICENCIATURA EN ESPAÑOL E INGLÉS",
    "RECREACIÓN Y DEPORTES"
]

NIVELES_RIESGO = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy Alto"]

TIPOS_VULNERABILIDAD = [
    "Académica",
    "Social",
    "Psicológica",
    "Económica"
]

# Tabla de permanencia
TABLA_PERMANENCIA = "permanencia"

def generar_datos_muestra(num_registros=100):
    """Genera datos de muestra para la tabla permanencia."""
    datos = []
    
    # Periodos académicos de los últimos 3 años
    periodos = []
    for año in range(2021, 2024):
        for semestre in [1, 2]:
            periodos.append(f"{año}-{semestre}")
    
    for _ in range(num_registros):
        # Seleccionar valores aleatorios
        servicio = random.choice(SERVICIOS)
        estrato = random.choice(ESTRATOS)
        programa = random.choice(PROGRAMAS)
        riesgo = random.choice(NIVELES_RIESGO)
        vulnerabilidad = random.choice(TIPOS_VULNERABILIDAD)
        periodo = random.choice(periodos)
        semestre = random.randint(1, 10)
        
        # Generar cantidades realistas basadas en el estrato
        if estrato <= 3:
            inscritos = random.randint(5, 15)
        else:
            inscritos = random.randint(1, 8)
        
        # Determinar si está matriculado, ha desertado o se ha graduado
        matriculado = random.choices([0, 1], weights=[10, 90])[0]  # 90% matriculados
        desertor = 0
        graduado = 0
        
        if matriculado == 1:
            # Solo los matriculados pueden desertar o graduarse
            desertor = random.choices([0, 1], weights=[90, 10])[0]  # 10% desertores
            
            if desertor == 0:
                # Solo los no desertores pueden graduarse
                graduado = random.choices([0, 1], weights=[95, 5])[0]  # 5% graduados
        
        # Determinar si requiere tutoría
        requiere_tutoria = random.choice(["Sí", "No"])
        
        # Crear el registro
        registro = {
            "servicio": servicio,
            "estrato": estrato,
            "inscritos": inscritos,
            "estudiante_programa_academico": programa,
            "riesgo_desercion": riesgo,
            "tipo_vulnerabilidad": vulnerabilidad,
            "periodo": periodo,
            "semestre": semestre,
            "matriculados": matriculado,
            "desertores": desertor,
            "graduados": graduado,
            "requiere_tutoria": requiere_tutoria
        }
        
        datos.append(registro)
    
    return datos

def insertar_datos_supabase(datos):
    """Inserta los datos en la tabla permanencia en Supabase."""
    try:
        # Verificar si la tabla existe
        try:
            # Intentar seleccionar un registro para verificar si la tabla existe
            supabase.table(TABLA_PERMANENCIA).select("id").limit(1).execute()
            print(f"La tabla {TABLA_PERMANENCIA} existe.")
        except Exception as e:
            if "42P01" in str(e):  # Código de error para tabla inexistente
                print(f"La tabla {TABLA_PERMANENCIA} no existe. Por favor, crea la tabla primero.")
                print("Puedes usar el script SQL en scripts/crear_tabla_permanencia.sql")
                return False
            else:
                raise e
        
        # Insertar los datos en lotes de 20 para evitar sobrecarga
        lote_size = 20
        total_registros = len(datos)
        registros_insertados = 0
        
        for i in range(0, total_registros, lote_size):
            lote = datos[i:i+lote_size]
            resultado = supabase.table(TABLA_PERMANENCIA).insert(lote).execute()
            registros_insertados += len(resultado.data)
            print(f"Insertados {registros_insertados} de {total_registros} registros...")
        
        print(f"¡Completado! Se insertaron {registros_insertados} registros en la tabla {TABLA_PERMANENCIA}.")
        return True
    
    except Exception as e:
        print(f"Error al insertar datos en Supabase: {e}")
        return False

def main():
    """Función principal."""
    print("Generando datos de muestra para la tabla permanencia...")
    
    # Solicitar al usuario el número de registros a generar
    try:
        num_registros = int(input("Número de registros a generar (predeterminado: 100): ") or "100")
    except ValueError:
        print("Valor inválido. Usando el valor predeterminado de 100 registros.")
        num_registros = 100
    
    # Generar los datos
    datos = generar_datos_muestra(num_registros)
    print(f"Se generaron {len(datos)} registros de muestra.")
    
    # Preguntar si desea insertar los datos en Supabase
    respuesta = input("¿Desea insertar estos datos en Supabase? (s/n): ").lower()
    
    if respuesta == "s":
        insertar_datos_supabase(datos)
    else:
        print("Operación cancelada. No se insertaron datos en Supabase.")

if __name__ == "__main__":
    main()
