#!/usr/bin/env python3
"""
🔍 Script de verificación y activación del sistema de actualización
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def check_system_status():
    """Verificar el estado del sistema de actualización"""
    print("🔍 VERIFICANDO SISTEMA DE ACTUALIZACIÓN MERCATO")
    print("=" * 50)
    
    # 1. Verificar archivos de automatización
    automation_files = [
        'automation.py',
        'update_laliga_fantasy_final.py',
        'backend/firebase_credentials.json'
    ]
    
    print("\n📁 ARCHIVOS DE AUTOMATIZACIÓN:")
    for file in automation_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")
    
    # 2. Verificar logs
    print("\n📝 LOGS DE AUTOMATIZACIÓN:")
    if os.path.exists('mercato_automation.log'):
        with open('mercato_automation.log', 'r') as f:
            lines = f.readlines()
            print(f"   ✅ mercato_automation.log ({len(lines)} líneas)")
            if lines:
                print(f"   📅 Última entrada: {lines[-1].strip()}")
    else:
        print("   ⚠️  mercato_automation.log - No existe (automatización nunca ejecutada)")
    
    # 3. Verificar dependencias
    print("\n📦 DEPENDENCIAS:")
    dependencies = ['schedule', 'playwright', 'firebase_admin', 'beautifulsoup4']
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - NO INSTALADO")
    
    # 4. Estado de Firebase
    print("\n🔥 FIREBASE:")
    try:
        if os.path.exists('backend/firebase_credentials.json'):
            print("   ✅ Credenciales Firebase encontradas")
        else:
            print("   ❌ Credenciales Firebase NO encontradas")
    except Exception as e:
        print(f"   ❌ Error verificando Firebase: {e}")
    
    print("\n" + "=" * 50)

def start_automation():
    """Iniciar el sistema de automatización"""
    print("\n🚀 INICIANDO AUTOMATIZACIÓN...")
    
    if not os.path.exists('automation.py'):
        print("❌ Error: automation.py no encontrado")
        return False
    
    try:
        # Ejecutar automation.py
        process = subprocess.Popen([sys.executable, 'automation.py'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        print("✅ Automatización iniciada en background")
        print("📝 Los logs se guardarán en mercato_automation.log")
        print("⏰ Se ejecutará cada 12 horas automáticamente")
        return True
        
    except Exception as e:
        print(f"❌ Error iniciando automatización: {e}")
        return False

def manual_update():
    """Ejecutar actualización manual"""
    print("\n🔄 EJECUTANDO ACTUALIZACIÓN MANUAL...")
    
    if not os.path.exists('update_laliga_fantasy_final.py'):
        print("❌ Error: update_laliga_fantasy_final.py no encontrado")
        return False
    
    try:
        result = subprocess.run([sys.executable, 'update_laliga_fantasy_final.py'], 
                               capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Actualización manual completada exitosamente")
            print("📊 Datos de jugadores actualizados")
            return True
        else:
            print(f"❌ Error en actualización: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout: La actualización tardó más de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando actualización: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 GESTOR DE ACTUALIZACIÓN MERCATO")
    print("=" * 40)
    
    while True:
        print("\n¿Qué quieres hacer?")
        print("1. 🔍 Verificar estado del sistema")
        print("2. 🚀 Iniciar automatización (cada 12h)")
        print("3. 🔄 Actualización manual (ahora)")
        print("4. 📊 Ver estado de la base de datos")
        print("5. ❌ Salir")
        
        choice = input("\nElige una opción (1-5): ").strip()
        
        if choice == '1':
            check_system_status()
        elif choice == '2':
            start_automation()
        elif choice == '3':
            manual_update()
        elif choice == '4':
            if os.path.exists('backend/check_players.py'):
                subprocess.run([sys.executable, 'backend/check_players.py'])
            else:
                print("❌ Script de verificación no encontrado")
        elif choice == '5':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()
