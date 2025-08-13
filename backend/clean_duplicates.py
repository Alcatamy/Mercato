"""
Script para limpiar jugadores duplicados en Firebase
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore
from collections import defaultdict

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

def clean_duplicates():
    """Limpiar jugadores duplicados"""
    db = initialize_firebase()
    if not db:
        return
    
    # Obtener todos los jugadores
    players_ref = db.collection('players')
    players_snapshot = players_ref.get()
    
    print(f"📊 Total de documentos antes de limpiar: {len(players_snapshot)}")
    
    # Agrupar por nombre + equipo
    players_by_key = defaultdict(list)
    
    for doc in players_snapshot:
        player = doc.to_dict()
        if not player:
            continue
            
        name = player.get('name', '').strip()
        team = player.get('team', '').strip()
        
        if name and team:
            key = f"{name}|{team}"
            players_by_key[key].append({
                'id': doc.id,
                'data': player,
                'ref': doc.reference
            })
    
    print(f"🔍 Jugadores únicos por nombre+equipo: {len(players_by_key)}")
    
    # Encontrar duplicados
    duplicates_found = 0
    docs_to_delete = []
    
    for key, docs in players_by_key.items():
        if len(docs) > 1:
            duplicates_found += 1
            name_team = key.replace('|', ' - ')
            print(f"   🔄 Duplicado: {name_team} ({len(docs)} copias)")
            
            # Mantener el documento con más información o el primero
            best_doc = docs[0]
            for doc in docs[1:]:
                # Si encontramos uno con más campos, mantener ese
                if len(doc['data']) > len(best_doc['data']):
                    docs_to_delete.append(best_doc['id'])
                    best_doc = doc
                else:
                    docs_to_delete.append(doc['id'])
    
    print(f"❌ Se encontraron {duplicates_found} jugadores duplicados")
    print(f"🗑️  Se eliminarán {len(docs_to_delete)} documentos duplicados")
    
    if len(docs_to_delete) > 0:
        confirm = input("¿Confirmas la eliminación de duplicados? (s/N): ")
        if confirm.lower() == 's':
            # Eliminar duplicados en lotes
            batch_size = 500
            deleted_count = 0
            
            for i in range(0, len(docs_to_delete), batch_size):
                batch = db.batch()
                batch_docs = docs_to_delete[i:i + batch_size]
                
                for doc_id in batch_docs:
                    batch.delete(players_ref.document(doc_id))
                
                batch.commit()
                deleted_count += len(batch_docs)
                print(f"   ✅ Eliminados {deleted_count}/{len(docs_to_delete)} duplicados")
            
            print(f"🎉 ¡Limpieza completada! Se eliminaron {deleted_count} documentos duplicados")
            
            # Verificar resultado final
            final_snapshot = players_ref.get()
            print(f"📊 Total de documentos después de limpiar: {len(final_snapshot)}")
        else:
            print("❌ Limpieza cancelada")
    else:
        print("✅ No se encontraron duplicados para eliminar")

if __name__ == "__main__":
    clean_duplicates()
