#!/usr/bin/env python3
"""
Script para limpiar archivos no utilizados del proyecto SIUP.
Ejecutar: python cleanup_unused_files.py
"""

import os
import shutil

def eliminar_archivos_no_utilizados():
    """Elimina archivos que no están siendo utilizados en el proyecto."""
    
    archivos_a_eliminar = [
        # Archivos de rutas no utilizados
        "routes/estadisticas_new.py",
        
        # Archivos de test
        "test_poa_validation.py",
        "test_povau_validation.py", 
        "test_comedor_endpoint.py",
        "test_supabase.py",
        
        # Scripts one-time ya ejecutados
        "fix_riesgo_desercion.py",
        "verify_db_structure.py",
        "create_permanencia_tables.py",
        "create_asistencias_actividades_table.py",
        "create_actas_negacion_table.py",
        
        # Archivos de configuración no utilizados
        "config/__init__.py.new",
        "supabase_client.py",
        
        # Documentación duplicada
        "DICCIONARIO_DATOS_COMPLETO.md"
    ]
    
    directorios_a_eliminar = [
        "frontejemplos"  # Directorio vacío
    ]
    
    print("🧹 LIMPIEZA DE ARCHIVOS NO UTILIZADOS")
    print("=" * 50)
    
    # Eliminar archivos
    print("\n📄 ARCHIVOS A ELIMINAR:")
    for archivo in archivos_a_eliminar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✅ Eliminado: {archivo}")
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
        else:
            print(f"⚠️  No existe: {archivo}")
    
    # Eliminar directorios
    print("\n📁 DIRECTORIOS A ELIMINAR:")
    for directorio in directorios_a_eliminar:
        if os.path.exists(directorio):
            try:
                shutil.rmtree(directorio)
                print(f"✅ Eliminado directorio: {directorio}")
            except Exception as e:
                print(f"❌ Error eliminando directorio {directorio}: {e}")
        else:
            print(f"⚠️  No existe: {directorio}")
    
    print("\n🎯 PROBLEMAS DETECTADOS (requieren acción manual):")
    print("• routes/usuarios.py - Importado en main.py pero no incluido en la aplicación")
    print("  → Recomendación: Agregar app.include_router(usuarios_router, prefix='/api', tags=['Usuarios'])")
    print("  → O eliminar la importación si no se usa")
    
    print("\n✅ LIMPIEZA COMPLETADA")
    print("📊 ESTADÍSTICAS:")
    print(f"   • Archivos procesados: {len(archivos_a_eliminar)}")
    print(f"   • Directorios procesados: {len(directorios_a_eliminar)}")

def mostrar_resumen_antes_eliminar():
    """Muestra qué se va a eliminar antes de ejecutar."""
    archivos_a_eliminar = [
        "routes/estadisticas_new.py",
        "test_poa_validation.py",
        "test_povau_validation.py", 
        "test_comedor_endpoint.py",
        "test_supabase.py",
        "fix_riesgo_desercion.py",
        "verify_db_structure.py",
        "create_permanencia_tables.py",
        "create_asistencias_actividades_table.py",
        "create_actas_negacion_table.py",
        "config/__init__.py.new",
        "supabase_client.py",
        "DICCIONARIO_DATOS_COMPLETO.md"
    ]
    
    directorios_a_eliminar = ["frontejemplos"]
    
    print("🔍 VISTA PREVIA DE LIMPIEZA")
    print("=" * 40)
    
    print("\n📄 ARCHIVOS QUE SE ELIMINARÁN:")
    for i, archivo in enumerate(archivos_a_eliminar, 1):
        existe = "✅" if os.path.exists(archivo) else "❌"
        print(f"  {i:2d}. {existe} {archivo}")
    
    print("\n📁 DIRECTORIOS QUE SE ELIMINARÁN:")
    for i, directorio in enumerate(directorios_a_eliminar, 1):
        existe = "✅" if os.path.exists(directorio) else "❌"
        print(f"  {i}. {existe} {directorio}")
    
    print("\n⚠️  ARCHIVOS QUE PERMANECERÁN (PERO REQUIEREN ATENCIÓN):")
    print("  • routes/usuarios.py (importado pero no utilizado)")
    
    print(f"\n📊 TOTAL: {len(archivos_a_eliminar)} archivos + {len(directorios_a_eliminar)} directorios")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        mostrar_resumen_antes_eliminar()
    elif len(sys.argv) > 1 and sys.argv[1] == "--execute":
        eliminar_archivos_no_utilizados()
    else:
        print("Uso:")
        print("  python cleanup_unused_files.py --preview   # Ver qué se eliminará")
        print("  python cleanup_unused_files.py --execute   # Ejecutar limpieza") 