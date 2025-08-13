"""
Script para poblar la base de datos con jugadores desde la API de MARCA Fantasy
"""

import os
import sys
import json
from typing import List, Dict

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, firestore

# Importar nuestro scraper
from scraper.marca_scraper import MarcaFantasyAPI, get_sample_players, Player


class PlayerDatabase:
    """Clase para gestionar la base de datos de jugadores"""
    
    def __init__(self, firebase_credentials_path: str = None):
        """
        Inicializar la conexión a Firebase
        
        Args:
            firebase_credentials_path: Ruta al archivo de credenciales de Firebase
        """
        try:
            # Verificar si Firebase ya está inicializado
            firebase_admin.get_app()
            print("✅ Firebase ya está inicializado")
        except ValueError:
            # Inicializar Firebase
            if firebase_credentials_path and os.path.exists(firebase_credentials_path):
                cred = credentials.Certificate(firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase inicializado con credenciales")
            else:
                # Usar configuración por defecto para desarrollo
                firebase_admin.initialize_app()
                print("✅ Firebase inicializado con configuración por defecto")
        
        self.db = firestore.client()
        print("🔗 Conectado a Firestore")
    
    def clear_players_collection(self):
        """Limpiar la colección de jugadores disponibles"""
        try:
            print("🗑️  Limpiando colección de jugadores disponibles...")
            
            # Obtener todos los documentos de la colección
            docs = self.db.collection('available_players').stream()
            
            # Eliminar documentos en lotes
            batch = self.db.batch()
            count = 0
            
            for doc in docs:
                batch.delete(doc.reference)
                count += 1
                
                # Ejecutar lote cada 500 documentos
                if count % 500 == 0:
                    batch.commit()
                    batch = self.db.batch()
            
            # Ejecutar lote final
            if count % 500 != 0:
                batch.commit()
            
            print(f"✅ Se eliminaron {count} jugadores de la colección")
            
        except Exception as e:
            print(f"❌ Error limpiando colección: {e}")
    
    def add_available_players(self, players: List[Player]):
        """
        Añadir jugadores a la colección de jugadores disponibles
        
        Args:
            players: Lista de jugadores para añadir
        """
        try:
            print(f"📥 Añadiendo {len(players)} jugadores a la base de datos...")
            
            # Procesar jugadores en lotes
            batch = self.db.batch()
            batch_size = 0
            
            for player in players:
                player_data = {
                    'id': player.id,
                    'name': player.name,
                    'position': player.position,
                    'team': player.team,
                    'value': player.value,
                    'points': player.points,
                    'status': player.status,
                    'updated_at': firestore.SERVER_TIMESTAMP
                }
                
                # Usar el ID del jugador como documento ID
                doc_ref = self.db.collection('available_players').document(player.id)
                batch.set(doc_ref, player_data)
                batch_size += 1
                
                # Ejecutar lote cada 500 documentos
                if batch_size >= 500:
                    batch.commit()
                    batch = self.db.batch()
                    batch_size = 0
                    print(f"  📦 Procesados {len(players) - len(players[players.index(player):])}")
            
            # Ejecutar lote final
            if batch_size > 0:
                batch.commit()
            
            print(f"✅ Se añadieron {len(players)} jugadores exitosamente")
            
        except Exception as e:
            print(f"❌ Error añadiendo jugadores: {e}")
            raise
    
    def get_players_by_position(self, position: str) -> List[Dict]:
        """
        Obtener jugadores por posición
        
        Args:
            position: Posición a filtrar (POR, DEF, MED, DEL)
            
        Returns:
            Lista de jugadores de esa posición
        """
        try:
            docs = self.db.collection('available_players').where('position', '==', position).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"❌ Error obteniendo jugadores por posición: {e}")
            return []
    
    def search_players(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Buscar jugadores por nombre
        
        Args:
            query: Texto a buscar
            limit: Límite de resultados
            
        Returns:
            Lista de jugadores que coinciden
        """
        try:
            # Firestore no soporta búsqueda de texto completo nativa
            # Implementamos una búsqueda simple
            docs = self.db.collection('available_players').limit(limit * 3).stream()
            
            results = []
            query_lower = query.lower()
            
            for doc in docs:
                data = doc.to_dict()
                if query_lower in data.get('name', '').lower():
                    results.append(data)
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            print(f"❌ Error buscando jugadores: {e}")
            return []
    
    def get_player_stats(self) -> Dict:
        """Obtener estadísticas de jugadores"""
        try:
            all_docs = list(self.db.collection('available_players').stream())
            
            if not all_docs:
                return {'total': 0, 'by_position': {}, 'by_team': {}}
            
            stats = {
                'total': len(all_docs),
                'by_position': {},
                'by_team': {},
                'value_range': {'min': float('inf'), 'max': 0}
            }
            
            for doc in all_docs:
                data = doc.to_dict()
                position = data.get('position', 'Unknown')
                team = data.get('team', 'Unknown')
                value = data.get('value', 0)
                
                # Contar por posición
                stats['by_position'][position] = stats['by_position'].get(position, 0) + 1
                
                # Contar por equipo
                stats['by_team'][team] = stats['by_team'].get(team, 0) + 1
                
                # Rango de valores
                if value > 0:
                    stats['value_range']['min'] = min(stats['value_range']['min'], value)
                    stats['value_range']['max'] = max(stats['value_range']['max'], value)
            
            return stats
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}


def main():
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando población de base de datos con jugadores de MARCA Fantasy")
    
    try:
        # Inicializar base de datos
        db = PlayerDatabase()
        
        # Intentar usar API real (por ahora usamos datos de muestra)
        print("\n📊 Obteniendo datos de jugadores...")
        
        # TODO: Descomentar cuando tengas token de MARCA API
        # marca_api = MarcaFantasyAPI("tu_token_aqui")
        # if marca_api.test_connection():
        #     print("✅ Conexión con MARCA API exitosa")
        #     players = marca_api.get_all_players()
        # else:
        #     print("⚠️  No se pudo conectar con MARCA API, usando datos de muestra")
        #     players = get_sample_players()
        
        # Usar datos de muestra por ahora
        print("⚠️  Usando datos de muestra (configura token de MARCA API para datos reales)")
        players = get_sample_players()
        
        if not players:
            print("❌ No se pudieron obtener datos de jugadores")
            return
        
        # Limpiar colección existente
        db.clear_players_collection()
        
        # Añadir nuevos jugadores
        db.add_available_players(players)
        
        # Mostrar estadísticas
        print("\n📈 Estadísticas de la base de datos:")
        stats = db.get_player_stats()
        print(f"  Total de jugadores: {stats.get('total', 0)}")
        print(f"  Por posición: {stats.get('by_position', {})}")
        print(f"  Rango de valores: €{stats.get('value_range', {}).get('min', 0):,} - €{stats.get('value_range', {}).get('max', 0):,}")
        
        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print("💡 Ahora los usuarios pueden seleccionar jugadores desde el desplegable en la app")
        
    except Exception as e:
        print(f"💥 Error ejecutando el script: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
