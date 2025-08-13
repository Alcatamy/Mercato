#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación para comprobar que los datos se subieron correctamente a Firebase
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

def verify_firebase_data():
    """Verificar los datos en Firebase"""
    try:
        # Inicializar Firebase
        cred = credentials.Certificate('backend/firebase_credentials.json')
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ Conexión con Firebase establecida correctamente.")
        
        # Obtener datos de la colección players
        players_ref = db.collection('players')
        docs = players_ref.limit(10).stream()  # Obtener solo los primeros 10 para verificar
        
        players = []
        for doc in docs:
            player_data = doc.to_dict()
            player_data['id'] = doc.id
            players.append(player_data)
        
        if players:
            print(f"\n🔍 VERIFICACIÓN DE DATOS EN FIREBASE:")
            print(f"✅ Se encontraron datos en la colección 'players'")
            print(f"📊 Muestra de los primeros {len(players)} jugadores:")
            
            for i, player in enumerate(players, 1):
                name = player.get('name', 'N/A')
                team = player.get('team', 'N/A')
                value = player.get('value', 0)
                last_update = player.get('last_update', 'N/A')
                source = player.get('source', 'N/A')
                
                print(f"   {i}. {name} ({team}) - {value:,} € [Fuente: {source}]")
            
            # Obtener estadísticas generales
            all_docs = players_ref.stream()
            total_count = sum(1 for _ in all_docs)
            print(f"\n📈 ESTADÍSTICAS GENERALES:")
            print(f"   🔢 Total de jugadores en Firebase: {total_count}")
            
            return True
        else:
            print("❌ No se encontraron datos en la colección 'players'")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar datos en Firebase: {e}")
        return False

if __name__ == "__main__":
    print("==================================================")
    print("        VERIFICACIÓN DE DATOS EN FIREBASE         ")
    print("==================================================")
    verify_firebase_data()
