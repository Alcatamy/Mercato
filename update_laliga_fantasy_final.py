#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de actualización para Mercato - LaLiga Fantasy (Versión Mejorada)
Extrae datos REALES de FutbolFantasy.com usando Playwright con:
- Manejo de banner de cookies
- Navegación por TODAS las páginas
- Extracción robusta de datos
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
        Utiliza Playwright para obtener datos reales de FutbolFantasy.com
        Navega por TODAS las páginas y maneja el banner de cookies
        """
        url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
        print(f"\n📥 Abriendo navegador para visitar: {url}")

        all_players = []  # Lista para acumular jugadores de todas las páginas

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)  # headless=True para ejecutar sin ventana
                page = browser.new_page()
                page.goto(url, timeout=60000)  # Timeout de 60 segundos para cargar la página

                # ========================================
                # MANEJO DEL BANNER DE PRIVACIDAD/COOKIES
                # ========================================
                try:
                    print("🔎 Buscando banner de privacidad...")
                    # Buscar el botón "ACEPTO" con un timeout corto
                    accept_button = page.get_by_role("button", name="ACEPTO")
                    accept_button.wait_for(timeout=10000)  # Esperar máximo 10 segundos
                    
                    print("👍 Banner encontrado. Haciendo clic en 'ACEPTO'...")
                    accept_button.click()
                    time.sleep(2)  # Pausa para que el banner desaparezca
                except PlaywrightTimeoutError:
                    print("✅ Banner de privacidad no detectado, continuando.")

                # Esperar a que los elementos de jugadores se carguen
                print("⏳ Esperando a que JavaScript rellene los datos de jugadores...")
                page.wait_for_selector('.elemento_jugador', timeout=30000)
                print("👍 Elementos de jugadores cargados.")

                # ========================================
                # NAVEGACIÓN POR TODAS LAS PÁGINAS
                # ========================================
                page_number = 1
                while True:
                    print(f"🔎 Procesando página {page_number}...")
                    
                    # Obtener el HTML de la página actual
                    html_content = page.content()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    player_elements = soup.find_all('div', class_='elemento_jugador')
                    
                    if player_elements:
                        # Extraer jugadores de la página actual
                        page_players = 0
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
                                
                                # Obtener el equipo desde el texto del elemento
                                text_lines = [line.strip() for line in element.get_text().split('\n') if line.strip()]
                                team_name = None
                                
                                # El equipo suele estar en la segunda línea de texto
                                if len(text_lines) >= 2:
                                    potential_team = text_lines[1]
                                    # Verificar que no sea un símbolo o dato numérico
                                    if not potential_team.startswith('+') and not potential_team.isdigit() and potential_team not in ['🔎']:
                                        team_name = potential_team
                                
                                if not team_name:
                                    team_id_attr = element.get('data-equipo', '')
                                    team_name = f"Equipo_{team_id_attr}"
                                
                                # Capitalizar correctamente el nombre del jugador
                                player_name = ' '.join(word.capitalize() for word in player_name.split())
                                
                                # Crear el ID del documento
                                team_id = team_name.lower().replace(' ', '-')
                                player_id_part = player_name.lower().replace(' ', '-')
                                document_id = f"{team_id}-{player_id_part}"
                                
                                all_players.append({
                                    'id': document_id,
                                    'name': player_name,
                                    'team': team_name,
                                    'value': price
                                })
                                page_players += 1
                                
                            except Exception as e:
                                continue
                        
                        print(f"   ✅ Extraídos {page_players} jugadores de la página {page_number}")
                    
                    # ========================================
                    # LÓGICA DE PAGINACIÓN
                    # ========================================
                    try:
                        # Buscar el botón "Siguiente" con el selector correcto
                        next_button = page.locator('.next')
                        
                        # Verificar si el botón existe y está habilitado
                        if next_button.count() == 0:
                            print("\n🏁 No se encontró botón 'Siguiente'. Probablemente sea la única página.")
                            break
                        
                        # Verificar si el botón está deshabilitado
                        button_class = next_button.get_attribute('class')
                        if 'disabled' in button_class.lower():
                            print("\n🏁 Se ha llegado a la última página. No hay más jugadores que extraer.")
                            break  # Salir del bucle while
                        
                        # Si no está desactivado, hacer clic
                        print("▶️  Haciendo clic en 'Siguiente'...")
                        next_button.click()
                        
                        # Esperar a que la página procese el clic y cargue los nuevos datos
                        page.wait_for_load_state('networkidle', timeout=30000)
                        
                        # Esperar también a que aparezcan los nuevos elementos de jugadores
                        page.wait_for_selector('.elemento_jugador', timeout=15000)
                        page_number += 1
                        
                    except Exception as e:
                        print(f"⚠️  Error en la navegación de páginas: {e}")
                        print("🔍 Verificando si hay más páginas disponibles...")
                        
                        # Intentar buscar con selectores alternativos
                        alt_selectors = ['a.next', '.next-page', '[data-next]', '.page-next']
                        found_next = False
                        
                        for alt_selector in alt_selectors:
                            try:
                                alt_button = page.locator(alt_selector)
                                if alt_button.count() > 0:
                                    print(f"✅ Encontrado botón alternativo: {alt_selector}")
                                    alt_button.click()
                                    page.wait_for_load_state('networkidle', timeout=30000)
                                    page.wait_for_selector('.elemento_jugador', timeout=15000)
                                    page_number += 1
                                    found_next = True
                                    break
                            except:
                                continue
                        
                        if not found_next:
                            print("🏁 No se pudo encontrar más páginas. Finalizando extracción.")
                            break

                browser.close()

            except PlaywrightTimeoutError:
                print("❌ Error de Timeout: Los elementos de jugadores no aparecieron en el tiempo esperado.")
                if 'browser' in locals() and browser.is_connected():
                    browser.close()
                return None
            except Exception as e:
                print(f"❌ Ocurrió un error inesperado con Playwright: {e}")
                if 'browser' in locals() and browser.is_connected():
                    browser.close()
                return None

        # Eliminar duplicados usando el ID como clave única
        unique_players = list({player['id']: player for player in all_players}.values())
        print(f"\n👍 Se han extraído un total de {len(unique_players)} jugadores únicos de {page_number} páginas.")
        return unique_players

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
            # Estadísticas por equipo
            team = player['team']
            if team not in stats['by_team']:
                stats['by_team'][team] = 0
            stats['by_team'][team] += 1
            
            # Valor total
            stats['total_value'] += player['value']
        
        # Top 5 jugadores más caros
        sorted_players = sorted(players_list, key=lambda x: x['value'], reverse=True)
        stats['top_players'] = sorted_players[:5]
        
        print(f"   🔢 Total de jugadores: {stats['total']}")
        print(f"   💰 Valor total del mercado: {stats['total_value']:,} €")
        print(f"   🏟️  Equipos encontrados: {len(stats['by_team'])}")
        
        print("\n   🏆 Top 5 jugadores más caros:")
        for i, player in enumerate(stats['top_players'], 1):
            print(f"      {i}. {player['name']} ({player['team']}) - {player['value']:,} €")
        
        return stats

    def run_update(self):
        """Ejecutar el proceso completo de actualización"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("==================================================")
        print("   INICIANDO SCRIPT DE ACTUALIZACIÓN FANTASY      ")
        print("   (Manejo de Cookies + Paginación Completa)      ")
        print("==================================================")
        print(f"🕒 Timestamp: {timestamp}")

        # Inicializar Firebase
        if not self.initialize_firebase():
            print("\n❌ SCRIPT FINALIZADO - No se pudo conectar a Firebase")
            return False

        # Obtener datos de jugadores
        players = self.get_player_data_from_futbolfantasy()

        if players:
            # Generar estadísticas
            self.generate_statistics(players)
            
            # Actualizar en Firebase
            success = self.update_data_in_firestore(players)
            
            if success:
                print("\n✅ SCRIPT FINALIZADO - Proceso completado exitosamente")
                return True
            else:
                print("\n❌ SCRIPT FINALIZADO - Error al actualizar Firebase")
                return False
        else:
            print("\n❌ No se obtuvieron datos de jugadores, no se realizará ninguna actualización en Firebase.")
            print("❌ SCRIPT FINALIZADO - Proceso completado con errores")
            return False

# ==============================================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    updater = FutbolFantasyUpdater()
    updater.run_update()
