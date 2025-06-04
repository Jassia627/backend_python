#!/usr/bin/env python3
"""
Ejemplo de uso de validaciones POVAU
Ejecutar: python test_povau_validation.py
"""

from services.Funciones_validar import validar_povau

def test_povau_validations():
    print("🧪 PROBANDO VALIDACIONES POVAU")
    print("=" * 50)
    
    # ✅ CASO VÁLIDO
    print("\n✅ CASO VÁLIDO:")
    datos_validos = {
        # Datos del estudiante (campos comunes)
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
        "nombres": "JUAN CARLOS",
        "apellidos": "PÉREZ GARCÍA",
        "correo": "juan.perez@unicesar.edu.co",
        "telefono": "3001234567",
        "direccion": "Calle 15 #10-20",
        "programa_academico": "INGENIERÍA DE SISTEMAS",
        "semestre": 5,
        "riesgo_desercion": "Bajo",
        "estrato": 3,
        
        # Datos específicos POVAU
        "tipo_participante": "Nuevo",
        "riesgo_spadies": "Medio",
        "fecha_ingreso_programa": "2024-01-15",
        "observaciones": "Estudiante proactivo con buen rendimiento académico"
    }
    
    errores = validar_povau(datos_validos)
    if errores:
        print(f"❌ Errores encontrados: {errores}")
    else:
        print("✅ Validación exitosa - todos los datos son correctos")
    
    # ❌ CASO INVÁLIDO
    print("\n❌ CASO INVÁLIDO:")
    datos_invalidos = {
        # Datos del estudiante (algunos errores)
        "tipo_documento": "CEDULA",  # Error: valor no válido
        "numero_documento": "123",   # Error: muy corto
        "nombres": "juan123",        # Error: tiene números
        "apellidos": "",             # Error: vacío
        "correo": "correo_malo",     # Error: formato inválido
        "programa_academico": "PROGRAMA INEXISTENTE",  # Error: no existe
        "semestre": 0,               # Error: debe ser >= 1
        "riesgo_desercion": "Super Alto",  # Error: valor no válido
        "estrato": 8,                # Error: debe ser 1-6
        
        # Datos específicos POVAU (errores)
        "tipo_participante": "Veterano",  # Error: valor no válido
        "riesgo_spadies": "Altísimo",     # Error: valor no válido
        "fecha_ingreso_programa": "",      # Error: obligatorio
        "observaciones": "a" * 300        # Error: muy largo (>255)
    }
    
    errores = validar_povau(datos_invalidos)
    print(f"❌ Errores encontrados ({len(errores)}):")
    for campo, error in errores.items():
        print(f"   • {campo}: {error}")
    
    # ⚠️ CASO PARCIAL (solo campos obligatorios)
    print("\n⚠️ CASO MÍNIMO (solo campos obligatorios):")
    datos_minimos = {
        # Mínimos campos del estudiante
        "tipo_documento": "CC",
        "numero_documento": "9876543210",
        "nombres": "MARÍA FERNANDA",
        "apellidos": "LÓPEZ TORRES",
        "correo": "maria.lopez@unicesar.edu.co",
        "programa_academico": "DERECHO",
        "semestre": 3,
        "riesgo_desercion": "Alto",
        "estrato": 2,
        
        # Campos obligatorios POVAU
        "tipo_participante": "Admitido",
        "riesgo_spadies": "Alto",
        "fecha_ingreso_programa": "2024-02-10"
        # observaciones es opcional, no se incluye
    }
    
    errores = validar_povau(datos_minimos)
    if errores:
        print(f"❌ Errores encontrados: {errores}")
    else:
        print("✅ Validación exitosa - datos mínimos correctos")

if __name__ == "__main__":
    test_povau_validations() 