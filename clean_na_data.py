#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar datos con N/A de Firebase
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

def clean_na_data():
    """Eliminar jugadores con datos N/A de Firebase"""
    try:
        # Inicializar Firebase
        cred = credentials.Certificate('backend/firebase_credentials.json')
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ Conexión con Firebase establecida correctamente.")
        
        # Obtener todos los jugadores
        players_ref = db.collection('players')
        docs = players_ref.stream()
        
        na_players = []
        total_players = 0
        
        print("🔍 Buscando jugadores con datos N/A...")
        
        for doc in docs:
            total_players += 1
            player_data = doc.to_dict()
            player_id = doc.id
            
            # Verificar si tiene datos N/A o fuente N/A
            team = player_data.get('team', '')
            source = player_data.get('source', '')
            name = player_data.get('name', '')
            
            if (team == 'N/A' or source == 'N/A' or source == '' or 
                'N/A' in str(team) or name == 'N/A'):
                na_players.append({
                    'id': player_id,
                    'name': name,
                    'team': team,
                    'source': source
                })
        
        print(f"📊 Total de jugadores analizados: {total_players}")
        print(f"🗑️  Jugadores con datos N/A encontrados: {len(na_players)}")
        
        if na_players:
            print("\n📋 Lista de jugadores a eliminar:")
            for i, player in enumerate(na_players[:10], 1):  # Mostrar solo los primeros 10
                print(f"   {i}. {player['name']} - Team: {player['team']} - Source: {player['source']}")
            
            if len(na_players) > 10:
                print(f"   ... y {len(na_players) - 10} más")
            
            # Confirmar eliminación
            response = input(f"\n❓ ¿Eliminar {len(na_players)} jugadores con datos N/A? (s/n): ")
            
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                print("🗑️  Eliminando jugadores con datos N/A...")
                
                # Eliminar en lotes de 500 (límite de Firestore)
                batch = db.batch()
                batch_count = 0
                
                for player in na_players:
                    doc_ref = players_ref.document(player['id'])
                    batch.delete(doc_ref)
                    batch_count += 1
                    
                    # Ejecutar batch cada 500 operaciones
                    if batch_count >= 500:
                        batch.commit()
                        print(f"   ✅ Eliminados {batch_count} jugadores...")
                        batch = db.batch()
                        batch_count = 0
                
                # Ejecutar el último batch si queda algo
                if batch_count > 0:
                    batch.commit()
                    print(f"   ✅ Eliminados los últimos {batch_count} jugadores...")
                
                print(f"🎉 ¡Limpieza completada! Se eliminaron {len(na_players)} jugadores con datos N/A.")
            else:
                print("❌ Operación cancelada por el usuario.")
        else:
            print("✅ No se encontraron jugadores con datos N/A. La base de datos está limpia.")
            
    except Exception as e:
        print(f"❌ Error al limpiar datos: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("        LIMPIEZA DE DATOS N/A EN FIREBASE         ")
    print("==================================================")
    clean_na_data()
