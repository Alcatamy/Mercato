"""
API endpoints para obtener jugadores disponibles desde el frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import List, Dict

app = Flask(__name__)
CORS(app)  # Permitir requests desde el frontend

# Inicializar Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

db = firestore.client()


@app.route('/api/players', methods=['GET'])
def get_all_players():
    """Obtener todos los jugadores disponibles"""
    try:
        # Parámetros de consulta
        position = request.args.get('position')
        search = request.args.get('search', '').lower()
        limit = int(request.args.get('limit', 100))
        
        # Construir consulta base
        query = db.collection('available_players')
        
        # Filtrar por posición si se especifica
        if position:
            query = query.where('position', '==', position.upper())
        
        # Ejecutar consulta
        docs = query.limit(limit * 2).stream()  # Obtener más para filtrar después
        
        players = []
        for doc in docs:
            data = doc.to_dict()
            
            # Filtrar por búsqueda de texto si se especifica
            if search and search not in data.get('name', '').lower():
                continue
            
            players.append({
                'id': data.get('id'),
                'name': data.get('name'),
                'position': data.get('position'),
                'team': data.get('team'),
                'value': data.get('value'),
                'points': data.get('points', 0)
            })
            
            if len(players) >= limit:
                break
        
        # Ordenar por valor (más caros primero)
        players.sort(key=lambda x: x.get('value', 0), reverse=True)
        
        return jsonify({
            'success': True,
            'players': players,
            'count': len(players)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/players/positions', methods=['GET'])
def get_positions():
    """Obtener lista de posiciones disponibles"""
    try:
        # Obtener estadísticas de posiciones
        docs = db.collection('available_players').stream()
        
        positions = {}
        for doc in docs:
            data = doc.to_dict()
            position = data.get('position', 'Unknown')
            positions[position] = positions.get(position, 0) + 1
        
        return jsonify({
            'success': True,
            'positions': positions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/players/search', methods=['GET'])
def search_players():
    """Buscar jugadores por nombre"""
    try:
        query = request.args.get('q', '').lower()
        limit = int(request.args.get('limit', 20))
        
        if not query or len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters'
            }), 400
        
        # Obtener jugadores y filtrar por nombre
        docs = db.collection('available_players').limit(200).stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            if query in data.get('name', '').lower():
                results.append({
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'position': data.get('position'),
                    'team': data.get('team'),
                    'value': data.get('value'),
                    'points': data.get('points', 0)
                })
                
                if len(results) >= limit:
                    break
        
        # Ordenar por relevancia (nombre más corto primero, luego por valor)
        results.sort(key=lambda x: (len(x.get('name', '')), -x.get('value', 0)))
        
        return jsonify({
            'success': True,
            'players': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/players/<player_id>', methods=['GET'])
def get_player_by_id(player_id):
    """Obtener información detallada de un jugador"""
    try:
        doc = db.collection('available_players').document(player_id).get()
        
        if not doc.exists:
            return jsonify({
                'success': False,
                'error': 'Player not found'
            }), 404
        
        data = doc.to_dict()
        
        return jsonify({
            'success': True,
            'player': {
                'id': data.get('id'),
                'name': data.get('name'),
                'position': data.get('position'),
                'team': data.get('team'),
                'value': data.get('value'),
                'points': data.get('points', 0),
                'status': data.get('status', 'available')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas generales de jugadores"""
    try:
        docs = list(db.collection('available_players').stream())
        
        stats = {
            'total': len(docs),
            'by_position': {},
            'by_team': {},
            'value_stats': {
                'min': float('inf'),
                'max': 0,
                'avg': 0
            }
        }
        
        total_value = 0
        
        for doc in docs:
            data = doc.to_dict()
            position = data.get('position', 'Unknown')
            team = data.get('team', 'Unknown')
            value = data.get('value', 0)
            
            # Contar por posición
            stats['by_position'][position] = stats['by_position'].get(position, 0) + 1
            
            # Contar por equipo
            stats['by_team'][team] = stats['by_team'].get(team, 0) + 1
            
            # Estadísticas de valor
            if value > 0:
                stats['value_stats']['min'] = min(stats['value_stats']['min'], value)
                stats['value_stats']['max'] = max(stats['value_stats']['max'], value)
                total_value += value
        
        # Calcular promedio
        if stats['total'] > 0:
            stats['value_stats']['avg'] = total_value / stats['total']
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que la API está funcionando"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Iniciando API en puerto {port}")
    print(f"🔧 Modo debug: {debug}")
    print(f"🌐 Accesible en: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
