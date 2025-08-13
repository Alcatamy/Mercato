#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de actualización para Mercato - LaLiga Fantasy
Extrae datos REALES de FutbolFantasy.com usando Playwright y actualiza Firebase
Basado en: https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado
"""

import re
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

class FutbolFantasyUpdater:
    def __init__(self):
        self.db = None
        self.credentials_file = 'backend/firebase_credentials.json'
        
    def initialize_firebase(self):
        """Inicializar conexión con Firebase"""
        try:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(f"Error: El archivo de credenciales '{self.credentials_file}' no se encontró.")
            
            cred = credentials.Certificate(self.credentials_file)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("✅ Conexión con Firebase establecida correctamente.")
            return True
        except Exception as e:
            print(f"❌ ERROR FATAL: No se pudo conectar con Firebase. {e}")
            return False

    def get_player_data_from_futbolfantasy(self):
        """
        Usa Playwright para abrir un navegador real, esperar a que JavaScript cargue los datos,
        y luego extrae la información de la tabla con BeautifulSoup.
        """
        url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
        print(f"\n📥 Abriendo navegador para visitar: {url}")

        html_content = None
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)  # headless=True para ejecutar sin ventana
                page = browser.new_page()
                page.goto(url, timeout=60000)  # Timeout de 60 segundos para cargar la página

                # --- LA CLAVE ESTÁ AQUÍ ---
                # Esperamos a que los elementos de jugadores aparezcan en la página.
                # El selector '.elemento_jugador' busca los divs con clase elemento_jugador
                # que contienen los datos de cada jugador.
                print("⏳ La página ha cargado. Esperando a que JavaScript rellene los datos de jugadores...")
                page.wait_for_selector('.elemento_jugador', timeout=30000)  # Timeout de 30s
                
                print("👍 Los elementos de jugadores se han cargado.")
                time.sleep(2)  # Una pequeña pausa adicional por si acaso

                # Una vez que los datos están visibles, obtenemos el HTML completo
                html_content = page.content()
                browser.close()

            except PlaywrightTimeoutError:
                print("❌ Error de Timeout: La tabla de jugadores no apareció en el tiempo esperado. Puede que la web esté lenta o haya cambiado.")
                browser.close()
                return None
            except Exception as e:
                print(f"❌ Ocurrió un error inesperado con Playwright: {e}")
                browser.close()
                return None

        if not html_content:
            print("❌ No se pudo obtener el contenido HTML de la página.")
            return None

        # Ahora que tenemos el HTML final, usamos BeautifulSoup como antes
        print("🔎 Analizando el HTML para extraer los datos...")
        soup = BeautifulSoup(html_content, 'html.parser')
        player_elements = soup.find_all('div', class_='elemento_jugador')

        if not player_elements:
            print("❌ No se encontraron elementos de jugadores ('elemento_jugador') en el HTML final.")
            return None

        players_list = []
        for element in player_elements:
            try:
                # Los datos están en los atributos data-* del elemento
                player_name = element.get('data-nombre', '').strip()
                if not player_name:
                    continue
                
                # Obtener el valor directamente del atributo data-valor
                valor_str = element.get('data-valor', '0')
                if not valor_str or valor_str == '0':
                    continue
                
                try:
                    price = int(valor_str)
                except ValueError:
                    continue
                
                # Obtener el equipo desde el atributo data-equipo (es un ID)
                team_id_attr = element.get('data-equipo', '')
                
                # Pero mejor buscar el nombre del equipo en el texto del elemento
                text_lines = [line.strip() for line in element.get_text().split('\n') if line.strip()]
                team_name = None
                
                # El equipo suele estar en la segunda línea de texto
                if len(text_lines) >= 2:
                    # La primera línea contiene el nombre del jugador (puede estar duplicado)
                    # La segunda línea suele ser el equipo
                    potential_team = text_lines[1]
                    # Verificar que no sea un símbolo o dato numérico
                    if not potential_team.startswith('+') and not potential_team.isdigit() and potential_team not in ['🔎']:
                        team_name = potential_team
                
                if not team_name:
                    team_name = f"Equipo_{team_id_attr}"
                
                # Capitalizar correctamente el nombre del jugador
                player_name = ' '.join(word.capitalize() for word in player_name.split())
                
                # Crear el ID del documento
                team_id = team_name.lower().replace(' ', '-')
                player_id_part = player_name.lower().replace(' ', '-')
                document_id = f"{team_id}-{player_id_part}"
                
                players_list.append({
                    'id': document_id,
                    'name': player_name,
                    'team': team_name,
                    'value': price
                })
            except Exception as e:
                print(f"⚠️  Error procesando elemento: {e}")
                continue
                    
        print(f"👍 Se han extraído datos de {len(players_list)} jugadores.")
        return players_list

    def update_data_in_firestore(self, players_list):
        """
        Recibe la lista de jugadores y actualiza los datos en la colección 'players'
        de Firestore de manera eficiente usando un batch.
        """
        if not self.db:
            print("❌ No hay conexión a Firebase. No se pueden actualizar los datos.")
            return False

        print("🔄 Actualizando datos en Firestore... (esto puede tardar un momento)")
        
        batch = self.db.batch()
        players_collection_ref = self.db.collection('players')

        for player in players_list:
            player_doc_ref = players_collection_ref.document(player['id'])
            
            player_data = {
                'name': player['name'],
                'team': player['team'],
                'value': player['value'],
                'last_update': firestore.SERVER_TIMESTAMP,
                'source': 'FutbolFantasy.com',
                'status': 'available'
            }
            
            batch.set(player_doc_ref, player_data, merge=True)

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
        print("        (Modo Navegador con Playwright)           ")
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
