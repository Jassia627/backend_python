#!/usr/bin/env python3
"""
Ejemplo de uso de validaciones POA
Ejecutar: python test_poa_validation.py
"""

from services.Funciones_validar import validar_POA

def test_poa_validations():
    print("🧪 PROBANDO VALIDACIONES POA - TABLA OFICIAL UPC")
    print("=" * 60)
    
    # ✅ CASO VÁLIDO COMPLETO
    print("\n✅ CASO VÁLIDO COMPLETO:")
    datos_validos = {
        # Datos básicos del estudiante POA
        "Nombre_apellido": "JUAN CARLOS PÉREZ GARCÍA",
        "Correo": "juan.perez@unicesar.edu.co",
        "Celular": "3001234567",
        "Semestre": 5,
        "nivel_riesgo": "Medio",
        "requiere_tutoria": True,
        "fecha": "2024-01-15",
        
        # Datos académicos
        "Docente_tutor": "MARÍA FERNANDA LÓPEZ TORRES",
        "Facultad": "FACULTAD DE INGENIERÍAS Y TECNOLOGÍAS",
        "Programa": "INGENIERÍA DE SISTEMAS",
        "Periodo_Académico": "2024-1",
        "Ciclo_formacion": "pregrado",
        
        # Datos específicos del acompañamiento
        "Nombre_asignatura": "PROGRAMACIÓN ORIENTADA A OBJETOS",
        "Tema": "Implementación de clases y objetos en Python",
        "Objetivo": "Desarrollar habilidades en POO para la creación de sistemas eficientes y escalables.",
        "Metodologia": "Aprendizaje basado en proyectos, desarrollo de casos prácticos y tutorías personalizadas.",
        "Logros": "El estudiante logró implementar correctamente herencia, polimorfismo y encapsulación.",
        "FIRMA_TUTOR": "MARÍA FERNANDA LÓPEZ TORRES"
    }
    
    errores = validar_POA(datos_validos)
    if errores:
        print(f"❌ Errores encontrados: {errores}")
    else:
        print("✅ Validación exitosa - todos los datos son correctos")
    
    # ❌ CASO INVÁLIDO (múltiples errores)
    print("\n❌ CASO INVÁLIDO (múltiples errores):")
    datos_invalidos = {
        # Errores en datos básicos
        "Nombre_apellido": "Juan123",  # Error: contiene números
        "Correo": "juan@gmail.com",   # Error: no es institucional
        "Celular": "300123",          # Error: formato incorrecto
        "Semestre": 15,               # Error: fuera del rango 1-10
        "nivel_riesgo": "Altísimo",   # Error: valor no válido
        "requiere_tutoria": "si",     # Error: no es booleano
        "fecha": "15/01/24",          # Error: formato incorrecto
        
        # Errores en datos académicos
        "Docente_tutor": "",          # Error: campo vacío
        "Facultad": "FACULTAD INEXISTENTE",  # Error: no existe
        "Programa": "PROGRAMA FALSO", # Error: no existe
        "Periodo_Académico": "2024",  # Error: formato incorrecto
        "Ciclo_formacion": "bachillerato",  # Error: valor no válido
        
        # Errores en datos específicos
        "Nombre_asignatura": "",      # Error: campo vacío
        "Tema": "",                   # Error: campo vacío
        "Objetivo": "",               # Error: campo vacío
        "Metodologia": "",            # Error: campo vacío
        "Logros": "",                 # Error: campo vacío
        "FIRMA_TUTOR": ""             # Error: campo vacío
    }
    
    errores = validar_POA(datos_invalidos)
    print(f"❌ Errores encontrados ({len(errores)}):")
    for campo, error in errores.items():
        print(f"   • {campo}: {error}")
    
    # ⚠️ CASO LÍMITES (campos con longitudes máximas)
    print("\n⚠️ CASO LÍMITES (campos con longitudes máximas):")
    datos_limites = {
        # Datos básicos válidos
        "Nombre_apellido": "ESTUDIANTE CON NOMBRE MUY LARGO PERO VÁLIDO",
        "Correo": "estudiante.nombre.largo@unicesar.edu.co",
        "Celular": "3109876543",
        "Semestre": 10,  # Máximo permitido
        "nivel_riesgo": "Muy alto",
        "requiere_tutoria": False,
        "fecha": "2024-12-31",
        
        # Datos académicos válidos
        "Docente_tutor": "DOCENTE CON NOMBRE COMPLETO MUY LARGO",
        "Facultad": "FACULTAD DE CIENCIAS ADMINISTRATIVAS, CONTABLES Y ECONÓMICAS",
        "Programa": "ADMINISTRACIÓN DE EMPRESAS TURÍSTICAS Y HOTELERAS",
        "Periodo_Académico": "2024-2",
        "Ciclo_formacion": "postgrado",
        
        # Campos con longitud máxima
        "Nombre_asignatura": "A" * 100,  # Exactamente 100 caracteres
        "Tema": "B" * 150,               # Exactamente 150 caracteres
        "Objetivo": "C" * 300,           # Exactamente 300 caracteres
        "Metodologia": "D" * 300,        # Exactamente 300 caracteres
        "Logros": "E" * 300,             # Exactamente 300 caracteres
        "FIRMA_TUTOR": "F" * 100         # Exactamente 100 caracteres (pero solo letras)
    }
    
    errores = validar_POA(datos_limites)
    if errores:
        print(f"❌ Errores encontrados: {errores}")
    else:
        print("✅ Validación exitosa - campos con longitudes máximas válidas")
    
    # 📋 INFORMACIÓN ADICIONAL
    print("\n📋 INFORMACIÓN DE VALIDACIONES POA:")
    print("  • Total de campos obligatorios: 17")
    print("  • Formato de correo: *@unicesar.edu.co")
    print("  • Formato de celular: 3** *** ****")
    print("  • Rango de semestre: 1-10")
    print("  • Periodo académico: yyyy-S (ejemplo: 2024-1)")
    print("  • Ciclos válidos: pregrado, postgrado")
    print("  • Facultades UPC: 5 disponibles")
    print("  • Programas UPC: 18 disponibles")

if __name__ == "__main__":
    test_poa_validations() 