#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del scraper de FutbolFantasy.com sin Firebase
Solo para probar la extracción de datos
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

class FutbolFantasyTester:
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

    def save_to_json(self, players_list, filename="futbolfantasy_players.json"):
        """Guardar datos en JSON"""
        data = {
            'players': players_list,
            'metadata': {
                'total_players': len(players_list),
                'source': 'FutbolFantasy.com',
                'scrape_timestamp': datetime.now().isoformat(),
                'url': 'https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado'
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Datos guardados en {filename}")
        return filename

    def generate_statistics(self, players_list):
        """Generar estadísticas de los datos extraídos"""
        print("\n📈 ESTADÍSTICAS DE EXTRACCIÓN:")
        
        stats = {
            'total': len(players_list),
            'by_position': {},
            'by_team': {},
            'total_value': 0,
            'top_players': []
        }
        
        for player in players_list:
            # Por posición
            pos = player.get('position', 'Unknown')
            stats['by_position'][pos] = stats['by_position'].get(pos, 0) + 1
            
            # Por equipo
            team = player['team']
            stats['by_team'][team] = stats['by_team'].get(team, 0) + 1
            
            # Valor total
            stats['total_value'] += player['value']
            
            # Top players
            stats['top_players'].append({
                'name': player['name'],
                'team': team,
                'value': player['value'],
                'position': pos
            })
        
        # Ordenar top players por valor
        stats['top_players'].sort(key=lambda x: x['value'], reverse=True)
        stats['top_players'] = stats['top_players'][:10]
        
        print(f"  📊 Total de jugadores: {stats['total']}")
        print(f"  🏆 Por posición: {dict(stats['by_position'])}")
        print(f"  🏟️  Equipos representados: {len(stats['by_team'])}")
        print(f"  💰 Valor total del mercado: €{stats['total_value']:,}")
        
        print(f"  💎 Top 10 jugadores más valiosos:")
        for i, player in enumerate(stats['top_players'], 1):
            print(f"    {i:2d}. {player['name']:20} ({player['team']:15}) {player['position']} - €{player['value']:,}")
        
        return stats

def main():
    """Función principal"""
    print("==================================================")
    print("   TEST SCRAPER FUTBOLFANTASY.COM                 ")
    print("==================================================")
    print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = FutbolFantasyTester()
    
    try:
        # Obtener datos de FutbolFantasy
        players = tester.get_player_data_from_futbolfantasy()
        
        if players:
            # Generar estadísticas
            tester.generate_statistics(players)
            
            # Guardar en JSON
            filename = tester.save_to_json(players)
            
            print("\n🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
            print(f"📁 Archivo guardado: {filename}")
            print("🌐 Fuente: FutbolFantasy.com/analytics/laliga-fantasy/mercado")
            return True
        else:
            print("\n❌ No se obtuvieron datos de jugadores")
            return False
            
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        return False

if __name__ == "__main__":
    main()
