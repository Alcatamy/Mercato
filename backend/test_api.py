"""
Script para probar y obtener datos reales de MARCA Fantasy API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.marca_scraper import MarcaFantasyAPI, get_real_players, get_sample_players
import json


def test_marca_api():
    """Probar la API de MARCA Fantasy"""
    print("🧪 Probando conexión con MARCA Fantasy API...")
    print("=" * 60)
    
    # Crear instancia de la API
    api = MarcaFantasyAPI(use_real_api=True)
    
    # Probar conexión básica
    print("1. 🌐 Probando conexión básica...")
    if api.test_connection():
        print("   ✅ Conexión exitosa con MARCA")
    else:
        print("   ❌ No se pudo conectar con MARCA")
        print("   💡 Esto es normal, la API puede requerir autenticación")
    
    print("\n2. 📊 Obteniendo lista de jugadores...")
    try:
        players = api.get_all_players()
        
        if players:
            print(f"   ✅ Se obtuvieron {len(players)} jugadores")
            
            # Mostrar estadísticas
            positions = {}
            teams = {}
            total_value = 0
            
            for player in players:
                positions[player.position] = positions.get(player.position, 0) + 1
                teams[player.team] = teams.get(player.team, 0) + 1
                total_value += player.value
            
            print(f"\n📈 Estadísticas:")
            print(f"   💰 Valor total del mercado: €{total_value:,}")
            print(f"   📊 Por posición: {positions}")
            print(f"   🏟️  Equipos representados: {len(teams)}")
            
            # Mostrar top 10 jugadores
            print(f"\n🏆 Top 10 jugadores más valiosos:")
            sorted_players = sorted(players, key=lambda x: x.value, reverse=True)[:10]
            for i, player in enumerate(sorted_players, 1):
                print(f"   {i:2d}. {player.name:<25} | {player.position} | {player.team:<20} | €{player.value:,}")
            
            # Mostrar algunos ejemplos por posición
            print(f"\n🎯 Ejemplos por posición:")
            for pos in ['POR', 'DEF', 'MED', 'DEL']:
                pos_players = [p for p in players if p.position == pos]
                if pos_players:
                    best = max(pos_players, key=lambda x: x.value)
                    print(f"   {pos}: {best.name} ({best.team}) - €{best.value:,}")
            
            return players
        else:
            print("   ⚠️  No se obtuvieron jugadores reales")
            return []
    
    except Exception as e:
        print(f"   ❌ Error obteniendo jugadores: {e}")
        return []


def save_players_to_json(players, filename="players_data.json"):
    """Guardar jugadores en archivo JSON"""
    try:
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'name': player.name,
                'position': player.position,
                'team': player.team,
                'value': player.value,
                'points': player.points,
                'status': player.status,
                'photo_url': player.photo_url
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(players_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Datos guardados en {filename}")
        return True
    except Exception as e:
        print(f"❌ Error guardando datos: {e}")
        return False


def load_players_from_json(filename="players_data.json"):
    """Cargar jugadores desde archivo JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        from scraper.marca_scraper import Player
        players = []
        for item in data:
            player = Player(
                id=item['id'],
                name=item['name'],
                position=item['position'],
                team=item['team'],
                value=item['value'],
                points=item.get('points', 0),
                status=item.get('status', 'available'),
                photo_url=item.get('photo_url', '')
            )
            players.append(player)
        
        print(f"📖 Se cargaron {len(players)} jugadores desde {filename}")
        return players
    except FileNotFoundError:
        print(f"❌ Archivo {filename} no encontrado")
        return []
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return []


def compare_data_sources():
    """Comparar datos de muestra vs datos reales"""
    print("\n🔄 Comparando fuentes de datos...")
    print("=" * 60)
    
    # Datos de muestra
    sample_players = get_sample_players()
    print(f"📊 Datos de muestra: {len(sample_players)} jugadores")
    
    # Intentar obtener datos reales
    real_players = test_marca_api()
    
    if real_players and len(real_players) > len(sample_players):
        print(f"🌐 Datos reales: {len(real_players)} jugadores")
        print("✅ Se recomienda usar datos reales")
        
        # Guardar datos reales para uso posterior
        save_players_to_json(real_players, "real_players.json")
        
        return real_players
    else:
        print(f"⚠️  Usando datos de muestra ({len(sample_players)} jugadores)")
        return sample_players


def main():
    """Función principal"""
    print("🚀 MARCA Fantasy API Tester")
    print("🎯 Objetivo: Obtener datos completos de jugadores de LaLiga")
    print("=" * 60)
    
    try:
        # Comparar fuentes de datos
        best_players = compare_data_sources()
        
        print(f"\n🎉 Resultado final: {len(best_players)} jugadores disponibles")
        
        if len(best_players) > 15:  # Mínimo aceptable
            print("✅ Datos suficientes para poblar la base de datos")
            
            # Preguntar si guardar
            save_data = input("\n💾 ¿Guardar datos para uso en la aplicación? (s/n): ")
            if save_data.lower() in ['s', 'si', 'y', 'yes']:
                save_players_to_json(best_players, "frontend_players.json")
                print("💡 Ahora puedes usar estos datos en populate-db.js")
        else:
            print("⚠️  Pocos datos obtenidos, considera verificar la API")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n🛑 Operación cancelada por el usuario")
        return 1
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
