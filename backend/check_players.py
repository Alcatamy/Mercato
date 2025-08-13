"""
Script para verificar jugadores en Firebase
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore
from collections import Counter

def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    try:
        if os.path.exists('firebase-admin-key.json'):
            cred = credentials.Certificate('firebase-admin-key.json')
        else:
            cred = credentials.Certificate('firebase_credentials.json')
        
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        return db
        
    except Exception as e:
        print(f"❌ Error inicializando Firebase: {e}")
        return None

def check_players():
    """Verificar jugadores en la base de datos"""
    db = initialize_firebase()
    if not db:
        return
    
    # Obtener todos los jugadores
    players_ref = db.collection('players')
    players_snapshot = players_ref.get()
    
    print(f"📊 Total de jugadores en la base de datos: {len(players_snapshot)}")
    
    # Contar por fuente
    sources = Counter()
    teams = Counter()
    first_letters = Counter()
    
    # Mostrar algunos ejemplos
    print(f"\n📋 Primeros 20 jugadores (ordenados alfabéticamente):")
    players_list = []
    
    for doc in players_snapshot:
        player = doc.to_dict()
        player['id'] = doc.id
        players_list.append(player)
        
        # Contar estadísticas
        source = player.get('source', 'Unknown')
        team = player.get('team', 'Unknown')
        name = player.get('name', '')
        
        sources[source] += 1
        teams[team] += 1
        if name:
            first_letters[name[0].upper()] += 1
    
    # Ordenar por nombre
    players_list.sort(key=lambda x: x.get('name', ''))
    
    # Mostrar primeros 20
    for i, player in enumerate(players_list[:20]):
        name = player.get('name', 'Sin nombre')
        team = player.get('team', 'Sin equipo')
        value = player.get('value', 0)
        source = player.get('source', 'Unknown')
        print(f"   {i+1:2d}. {name} ({team}) - {value:,}€ - {source}")
    
    # Estadísticas por fuente
    print(f"\n📈 Jugadores por fuente:")
    for source, count in sources.items():
        print(f"   {source}: {count} jugadores")
    
    # Estadísticas por letra
    print(f"\n🔤 Jugadores por primera letra:")
    for letter in sorted(first_letters.keys()):
        count = first_letters[letter]
        print(f"   {letter}: {count} jugadores")
    
    # Equipos más representados
    print(f"\n🏟️  Top 10 equipos con más jugadores:")
    for team, count in teams.most_common(10):
        print(f"   {team}: {count} jugadores")

if __name__ == "__main__":
    check_players()
