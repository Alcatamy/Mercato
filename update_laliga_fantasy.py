#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de actualización para Mercato - LaLiga Fantasy
Extrae datos REALES de FutbolFantasy.com y actualiza Firebase
Basado en: https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado
"""

import requests
from bs4 import BeautifulSoup
import re
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

class FutbolFantasyUpdater:
    def __init__(self):
        self.db = None
        self.credentials_file = 'backend/firebase_credentials.json'
        
    def initialize_firebase(self):
        """Inicializar conexión con Firebase"""
        try:
            # Buscar archivo de credenciales
            if not os.path.exists(self.credentials_file):
                print(f"❌ Error: El archivo de credenciales '{self.credentials_file}' no se encontró.")
                print("💡 Asegúrate de tener el archivo firebase_credentials.json en el directorio backend")
                return False
            
            # Inicializar Firebase si no está ya inicializado
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.credentials_file)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("✅ Conexión con Firebase establecida correctamente.")
            return True
            
        except Exception as e:
            print(f"❌ ERROR FATAL: No se pudo conectar con Firebase. {e}")
            return False
    
    def get_player_data_from_futbolfantasy(self):
        """
        Visita la web de FutbolFantasy, extrae los datos de la tabla de mercado
        y los devuelve como una lista de diccionarios de jugadores.
        """
        url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
        print(f"\n📥 Obteniendo datos de jugadores desde: {url}")

        try:
            # Usamos un User-Agent para simular ser un navegador y evitar bloqueos
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"❌ Error al conectar con FutbolFantasy: {e}")
            return None

        # Analizamos el contenido HTML de la página con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        players_list = []
        
        # Buscar datos de jugadores en el HTML
        # Los datos están en formato: DELDanjuma![Valencia]...Valencia 🔎+4.243.8440% 2días5.939.0630
        page_text = soup.get_text()
        
        # Buscar patrones de jugadores
        import re
        
        # Patrón que captura: POSICION + Nombre + ![Equipo] + datos
        pattern = r'(DEL|MED|DEF|POR)([A-Za-záéíóúüñ\s]+)!\[([^\]]+)\][^🔎]*🔎[^0-9]*(?:[\+\-][\d\.]+[%]?\s*)?(?:\d+días)?(\d+\.?\d*\.?\d*)\d*'
        
        matches = re.findall(pattern, page_text, re.MULTILINE)
        
        print(f"🔍 Encontrados {len(matches)} patrones de jugadores")
        
        for match in matches:
            try:
                position = match[0]
                player_name = match[1].strip()
                team_name = match[2].strip()
                price_text = match[3]
                
                # Limpiar precio - convertir de formato como "5.939.063" a 5939063
                if '.' in price_text:
                    price = int(price_text.replace('.', ''))
                else:
                    price = int(price_text) if price_text else 1000000
                
                # Crear ID único
                team_id = team_name.lower().replace(' ', '-')
                player_id = player_name.lower().replace(' ', '-')
                document_id = f"{team_id}-{player_id}"
                
                # Validar que tengamos datos mínimos
                if len(player_name) > 2 and len(team_name) > 2 and price > 0:
                    players_list.append({
                        'id': document_id,
                        'name': player_name,
                        'team': team_name,
                        'position': position,
                        'value': price
                    })

            except (ValueError, IndexError) as e:
                continue
        
        # Si no encontramos jugadores con el primer método, intentar método alternativo
        if len(players_list) < 10:
            print("🔄 Intentando método alternativo de extracción...")
            
            # Buscar todas las líneas que contengan información de jugadores
            lines = page_text.split('\n')
            for line in lines:
                if any(pos in line for pos in ['DEL', 'MED', 'DEF', 'POR']) and '![' in line:
                    try:
                        # Extraer datos de líneas como: "DELDanjuma![Valencia]..."
                        parts = line.strip()
                        
                        # Buscar posición
                        position = None
                        for pos in ['DEL', 'MED', 'DEF', 'POR']:
                            if parts.startswith(pos):
                                position = pos
                                parts = parts[3:]  # Quitar posición del inicio
                                break
                        
                        if not position:
                            continue
                        
                        # Buscar nombre y equipo
                        if '![' in parts and ']' in parts:
                            name_part = parts.split('![')[0]
                            team_part = parts.split('![')[1].split(']')[0]
                            
                            # Extraer precio del final de la línea
                            price_match = re.search(r'(\d+\.?\d*\.?\d*)\s*$', line)
                            if price_match:
                                price_text = price_match.group(1)
                                price = int(price_text.replace('.', '')) if '.' in price_text else int(price_text)
                            else:
                                price = 1000000
                            
                            if len(name_part) > 2 and len(team_part) > 2:
                                team_id = team_part.lower().replace(' ', '-')
                                player_id = name_part.lower().replace(' ', '-')
                                document_id = f"{team_id}-{player_id}"
                                
                                players_list.append({
                                    'id': document_id,
                                    'name': name_part.strip(),
                                    'team': team_part.strip(),
                                    'position': position,
                                    'value': price
                                })
                    except:
                        continue
        
        # Eliminar duplicados
        seen_ids = set()
        unique_players = []
        for player in players_list:
            if player['id'] not in seen_ids:
                seen_ids.add(player['id'])
                unique_players.append(player)
        
        print(f"👍 Se han extraído datos de {len(unique_players)} jugadores únicos.")
        return unique_players if unique_players else None

    def update_data_in_firestore(self, players_list):
        """
        Recibe la lista de jugadores y actualiza los datos en la colección 'players'
        de Firestore de manera eficiente usando un batch.
        """
        if not self.db:
            print("❌ No hay conexión a Firebase. No se pueden actualizar los datos.")
            return False

        print("🔄 Actualizando datos en Firestore... (esto puede tardar un momento)")
        
        # Un "batch" permite realizar múltiples operaciones en una sola llamada a la base de datos
        batch = self.db.batch()
        players_collection_ref = self.db.collection('players')

        for player in players_list:
            # Usamos el ID único del jugador como ID del documento en Firestore
            player_doc_ref = players_collection_ref.document(player['id'])
            
            # Creamos un diccionario con los datos a actualizar
            player_data = {
                'name': player['name'],
                'team': player['team'],
                'value': player['value'],
                'last_update': firestore.SERVER_TIMESTAMP,
                'source': 'FutbolFantasy.com',
                'status': 'available'
            }
            
            # Usamos 'set' con 'merge=True' para crear el jugador si no existe,
            # o para actualizar sus datos sin borrar otros campos (como 'ownerId').
            batch.set(player_doc_ref, player_data, merge=True)

        # Enviamos todas las operaciones a Firebase
        batch.commit()
        print(f"🔥 ¡Éxito! Base de datos actualizada con la información de {len(players_list)} jugadores.")
        return True

    def generate_statistics(self, players_list):
        """Generar estadísticas de los datos actualizados"""
        print("\n📈 ESTADÍSTICAS DE ACTUALIZACIÓN:")
        
        stats = {
            'total': len(players_list),
            'by_team': {},
            'total_value': 0,
            'top_players': []
        }
        
        for player in players_list:
            # Por equipo
            team = player['team']
            stats['by_team'][team] = stats['by_team'].get(team, 0) + 1
            
            # Valor total
            stats['total_value'] += player['value']
            
            # Top players
            stats['top_players'].append({
                'name': player['name'],
                'team': team,
                'value': player['value']
            })
        
        # Ordenar top players por valor
        stats['top_players'].sort(key=lambda x: x['value'], reverse=True)
        stats['top_players'] = stats['top_players'][:10]
        
        print(f"  📊 Total de jugadores: {stats['total']}")
        print(f"  🏟️  Equipos representados: {len(stats['by_team'])}")
        print(f"  💰 Valor total del mercado: €{stats['total_value']:,}")
        
        print(f"  💎 Top 10 jugadores más valiosos:")
        for i, player in enumerate(stats['top_players'], 1):
            print(f"    {i:2d}. {player['name']:25} ({player['team']:15}) - €{player['value']:,}")
        
        return stats

    def run_update(self):
        """Ejecutar actualización completa"""
        print("==================================================")
        print("   INICIANDO SCRIPT DE ACTUALIZACIÓN FANTASY      ")
        print("==================================================")
        print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Inicializar Firebase
        if not self.initialize_firebase():
            return False
        
        # Obtener datos de FutbolFantasy
        players = self.get_player_data_from_futbolfantasy()
        
        if players:
            # Actualizar base de datos
            if self.update_data_in_firestore(players):
                # Generar estadísticas
                self.generate_statistics(players)
                
                print("\n🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!")
                print("✨ La aplicación web ahora tiene datos actualizados de LaLiga Fantasy")
                print("🌐 Fuente: FutbolFantasy.com/analytics/laliga-fantasy/mercado")
                return True
            else:
                print("\n❌ Error actualizando Firebase")
                return False
        else:
            print("\n❌ No se obtuvieron datos de jugadores, no se realizará ninguna actualización en Firebase.")
            return False

def main():
    """Función principal"""
    updater = FutbolFantasyUpdater()
    
    try:
        success = updater.run_update()
        if success:
            print("\n✅ SCRIPT FINALIZADO - Proceso completado exitosamente")
            return 0
        else:
            print("\n❌ SCRIPT FINALIZADO - Proceso completado con errores")
            return 1
    except KeyboardInterrupt:
        print("\n⏹️  Proceso cancelado por el usuario")
        return 1
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
