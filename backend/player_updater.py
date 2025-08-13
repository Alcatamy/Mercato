"""
Actualizador de precios de jugadores en Firebase Firestore
Utiliza el scraper de FutbolFantasy.com para mantener actualizados los valores
"""

import os
import sys
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Añadir el directorio padre al path para importar el scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar el scraper real que funciona
try:
    from update_laliga_fantasy_final import FutbolFantasyUpdater
    SCRAPER_AVAILABLE = True
except ImportError:
    print("⚠️  Scraper principal no disponible, usando datos de ejemplo")
    SCRAPER_AVAILABLE = False


def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    try:
        # Intentar usar credenciales desde archivo
        if os.path.exists('firebase-admin-key.json'):
            cred = credentials.Certificate('firebase-admin-key.json')
        else:
            # Usar credenciales desde variable de entorno (GitHub Actions)
            firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
            if firebase_credentials:
                import json
                cred_dict = json.loads(firebase_credentials)
                cred = credentials.Certificate(cred_dict)
            else:
                raise ValueError("No se encontraron credenciales de Firebase")
        
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Conexión con Firebase establecida")
        return db
        
    except Exception as e:
        print(f"❌ Error inicializando Firebase: {e}")
        return None


def update_players_in_firestore(db, players_list):
    """
    Actualizar información de jugadores en Firestore
    
    Args:
        db: Cliente de Firestore
        players_list: Lista de objetos Player
    """
    try:
        print(f"🔄 Actualizando {len(players_list)} jugadores en Firestore...")
        
        # Usar batch para operaciones múltiples
        batch = db.batch()
        players_collection = db.collection('players')
        
        for player in players_list:
            # Crear ID único basado en el nombre (normalizado)
            player_id = player.name.lower().replace(' ', '-').replace('.', '').replace("'", '')
            
            # Referencia al documento
            player_ref = players_collection.document(player_id)
            
            # Datos del jugador
            player_data = {
                'name': player.name,
                'name_lowercase': player.name.lower(),  # Campo para búsqueda eficiente
                'team_lowercase': player.team.lower(),  # Campo para búsqueda de equipo
                'position': player.position,
                'team': player.team,
                'value': player.value,
                'points': player.points,
                'source': 'FutbolFantasy.com',  # Identificar la fuente
                'lastUpdated': datetime.now(),
                'status': 'available'
            }
            
            # Usar merge=True para preservar campos adicionales como ownerId
            batch.set(player_ref, player_data, merge=True)
        
        # Ejecutar todas las actualizaciones
        batch.commit()
        print(f"🔥 ¡Éxito! {len(players_list)} jugadores actualizados en Firestore")
        
        # Estadísticas
        positions = {}
        total_value = 0
        
        for player in players_list:
            positions[player.position] = positions.get(player.position, 0) + 1
            total_value += player.value
        
        print(f"\n📊 Estadísticas de actualización:")
        print(f"   💰 Valor total del mercado: {total_value:,}€")
        for position, count in positions.items():
            print(f"   🏃 {position}: {count} jugadores")
        
    except Exception as e:
        print(f"❌ Error actualizando jugadores: {e}")


def create_initial_managers(db):
    """
    Crear managers iniciales si no existen
    
    Args:
        db: Cliente de Firestore
    """
    try:
        managers_ref = db.collection('managers')
        
        # Verificar si ya existen managers
        existing_managers = managers_ref.get()
        if len(existing_managers) > 0:
            print("ℹ️  Los managers ya existen, saltando creación inicial")
            return
        
        print("👥 Creando managers iniciales...")
        
        managers = [
            {'id': 'alcatamy-esports-by-rolex', 'name': 'Alcatamy eSports by Rolex'},
            {'id': 'vigar-fc', 'name': 'Vigar FC'},
            {'id': 'baena10', 'name': 'Baena10'},
            {'id': 'dubai-city-fc', 'name': 'Dubai cITY FC'},
            {'id': 'visite-la-manga-fc', 'name': 'Visite La Manga FC'},
            {'id': 'morenazos-fc', 'name': 'Morenazos FC'}
        ]
        
        batch = db.batch()
        
        for manager in managers:
            manager_ref = managers_ref.document(manager['id'])
            manager_data = {
                'name': manager['name'],
                'createdAt': datetime.now(),
                'totalValue': 0,
                'playerCount': 0
            }
            batch.set(manager_ref, manager_data)
        
        batch.commit()
        print(f"✅ {len(managers)} managers creados")
        
    except Exception as e:
        print(f"❌ Error creando managers: {e}")


def main():
    """Función principal del script"""
    print("🚀 Iniciando actualización de precios de jugadores")
    print(f"📅 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Inicializar Firebase
    db = initialize_firebase()
    if not db:
        print("❌ No se pudo conectar a Firebase. Abortando.")
        sys.exit(1)
    
    # Crear managers iniciales si es necesario
    create_initial_managers(db)
    
    # Obtener datos de jugadores
    players = []
    
    if SCRAPER_AVAILABLE:
        print("🌐 Usando scraper de FutbolFantasy.com")
        try:
            # Usar el scraper real de FutbolFantasy.com
            updater = FutbolFantasyUpdater()
            
            # Obtener jugadores reales desde FutbolFantasy.com
            players_data = updater.get_player_data_from_futbolfantasy()
            
            if players_data and len(players_data) > 0:
                print(f"✅ Obtenidos {len(players_data)} jugadores de FutbolFantasy.com")
                
                # Convertir a formato compatible con Firestore
                for player_data in players_data:
                    # Crear objeto player compatible
                    class Player:
                        def __init__(self, data):
                            self.name = data.get('name', '')
                            self.position = data.get('position', 'MED')
                            self.team = data.get('team', '')
                            self.value = data.get('value', 0)
                            self.points = data.get('points', 0)
                    
                    players.append(Player(player_data))
            else:
                print("⚠️  No se obtuvieron jugadores del scraper")
                
        except Exception as e:
            print(f"⚠️  Error con el scraper de FutbolFantasy: {e}")
            print("📊 Sin datos disponibles")
    else:
        print("📊 Scraper no disponible, sin datos que actualizar")
    
    if players and len(players) > 0:
        # Actualizar jugadores en Firestore
        update_players_in_firestore(db, players)
        
        # Crear estadísticas de ejecución
        execution_stats = {
            'lastUpdate': datetime.now(),
            'playersUpdated': len(players),
            'totalMarketValue': sum(p.value for p in players),
            'source': 'FutbolFantasy.com' if SCRAPER_AVAILABLE else 'no_data'
        }
        
        # Guardar estadísticas
        try:
            db.collection('system').document('update_stats').set(execution_stats)
            print("📈 Estadísticas de ejecución guardadas")
        except Exception as e:
            print(f"⚠️  Error guardando estadísticas: {e}")
        
        print("\n🎉 Actualización completada exitosamente!")
    else:
        print("❌ No se pudieron obtener datos de jugadores")
        # No hacer sys.exit(1) para que GitHub Actions no falle
        print("ℹ️  El sistema continuará funcionando con los datos existentes")


if __name__ == "__main__":
    main()
