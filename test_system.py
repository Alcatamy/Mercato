#!/usr/bin/env python3
"""
Script de prueba para verificar que toda la integración funcione correctamente
"""

import os
import sys
import json
import time
from datetime import datetime

def test_scraper():
    """Probar el scraper de FutbolFantasy"""
    print("🕷️  PROBANDO SCRAPER DE FUTBOLFANTASY.COM")
    print("=" * 50)
    
    try:
        # Importar scraper
        sys.path.append('backend')
        from scraper.futbolfantasy_advanced import FutbolFantasyAnalyzer
        
        scraper = FutbolFantasyAnalyzer()
        print("✅ Scraper inicializado correctamente")
        
        # Ejecutar scraping
        print("🌐 Obteniendo datos de FutbolFantasy.com...")
        players = scraper.get_all_players_advanced()
        
        if players and len(players) > 0:
            print(f"✅ Se obtuvieron {len(players)} jugadores")
            
            # Estadísticas
            stats = {'positions': {}, 'teams': {}, 'total_value': 0}
            for player in players:
                pos = player.position if hasattr(player, 'position') else 'Unknown'
                team = player.team if hasattr(player, 'team') else 'Unknown'
                value = player.value if hasattr(player, 'value') else 0
                
                stats['positions'][pos] = stats['positions'].get(pos, 0) + 1
                stats['teams'][team] = stats['teams'].get(team, 0) + 1
                stats['total_value'] += value
            
            print(f"📊 Estadísticas:")
            print(f"  Por posición: {dict(stats['positions'])}")
            print(f"  Equipos: {len(stats['teams'])}")
            print(f"  Valor total: €{stats['total_value']:,}")
            
            # Top 3 jugadores
            top_players = sorted(players, key=lambda x: x.value if hasattr(x, 'value') else 0, reverse=True)[:3]
            print(f"💎 Top 3 más valiosos:")
            for i, player in enumerate(top_players, 1):
                print(f"  {i}. {player.name} ({player.team}) - €{player.value:,}")
            
            return True, players
        else:
            print("❌ No se pudieron obtener datos")
            return False, None
            
    except Exception as e:
        print(f"❌ Error en scraper: {e}")
        return False, None

def test_file_structure():
    """Verificar estructura de archivos"""
    print("\n📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("=" * 50)
    
    required_files = [
        'frontend/index.html',
        'frontend/app.js',
        'frontend/populate-laliga-fantasy.js',
        'backend/scraper/futbolfantasy_advanced.py',
        'backend/requirements.txt'
    ]
    
    optional_files = [
        'backend/firebase-key.json',
        'backend/futbolfantasy_players.json'
    ]
    
    all_good = True
    
    # Archivos requeridos
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - FALTA")
            all_good = False
    
    # Archivos opcionales
    for file_path in optional_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} (opcional)")
        else:
            print(f"⚠️  {file_path} - No encontrado (opcional)")
    
    return all_good

def test_frontend_files():
    """Verificar contenido de archivos frontend"""
    print("\n🎨 VERIFICANDO ARCHIVOS FRONTEND")
    print("=" * 50)
    
    try:
        # Verificar HTML
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        html_checks = [
            ('populate-laliga-fantasy.js', 'Script de datos reales incluido'),
            ('Firebase SDK', 'SDK de Firebase'),
            ('Tailwind CSS', 'Framework CSS'),
            ('searchPlayersAPI', 'Función de búsqueda de API')
        ]
        
        for check, description in html_checks:
            if check in html_content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - No encontrado")
        
        # Verificar JavaScript
        with open('frontend/populate-laliga-fantasy.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        js_checks = [
            ('laligaFantasyPlayers', 'Datos de jugadores reales'),
            ('populateRealLaLigaFantasy', 'Función de población real'),
            ('FutbolFantasy.com', 'Referencia a fuente de datos'),
            ('43 jugadores', 'Documentación de cantidad')
        ]
        
        for check, description in js_checks:
            if check in js_content:
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} - Podría estar ausente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando frontend: {e}")
        return False

def test_backend_dependencies():
    """Verificar dependencias del backend"""
    print("\n🐍 VERIFICANDO DEPENDENCIAS PYTHON")
    print("=" * 50)
    
    required_packages = [
        'beautifulsoup4',
        'requests',
        'lxml',
        'firebase-admin'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Para instalar dependencias faltantes:")
        print("cd backend && pip install -r requirements.txt")
    
    return all_installed

def generate_test_report(results):
    """Generar reporte de pruebas"""
    print("\n📋 REPORTE FINAL DE PRUEBAS")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"📊 Resumen: {passed_tests}/{total_tests} pruebas pasadas")
    
    for test_name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"  {status} - {test_name}")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✨ El sistema está listo para usar con datos reales de LaLiga Fantasy")
        print("🌐 Fuente: FutbolFantasy.com/analytics/laliga-fantasy/mercado")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} pruebas fallaron")
        print("🔧 Revisa los errores arriba y corrige los problemas")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA MERCATO")
    print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    results = {}
    
    # Test 1: Estructura de archivos
    results['Estructura de archivos'] = test_file_structure()
    
    # Test 2: Archivos frontend
    results['Archivos frontend'] = test_frontend_files()
    
    # Test 3: Dependencias backend
    results['Dependencias Python'] = test_backend_dependencies()
    
    # Test 4: Scraper
    scraper_success, players_data = test_scraper()
    results['Scraper FutbolFantasy'] = scraper_success
    
    # Generar reporte final
    all_tests_passed = generate_test_report(results)
    
    # Instrucciones adicionales
    print("\n🛠️  PRÓXIMOS PASOS:")
    if all_tests_passed:
        print("1. Abre frontend/index.html en tu navegador")
        print("2. Presiona el botón '⚡ LaLiga Fantasy REAL' para poblar datos")
        print("3. ¡Comienza a usar la aplicación con datos reales!")
    else:
        print("1. Corrige los errores reportados arriba")
        print("2. Vuelve a ejecutar este script")
        print("3. Una vez que todas las pruebas pasen, estará listo")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("- README.md: Guía completa de uso")
    print("- frontend/populate-laliga-fantasy.js: 43 jugadores reales disponibles")
    print("- backend/scraper/futbolfantasy_advanced.py: Scraper principal")
    
    return all_tests_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas canceladas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)
