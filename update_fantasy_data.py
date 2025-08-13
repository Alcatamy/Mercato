# -*- coding: utf-8 -*-

# ==============================================================================
# LIBRERÍAS NECESARIAS
# ==============================================================================
import requests  # Para hacer peticiones a la página web
from bs4 import BeautifulSoup  # Para "leer" el HTML de la página
import re  # Para limpiar los datos del precio (quitar puntos, €, etc.)
import firebase_admin  # Para conectar con Firebase
from firebase_admin import credentials, firestore
import os # Para buscar el archivo de credenciales

# ==============================================================================
# INICIALIZACIÓN DE FIREBASE
# ==============================================================================
# El script buscará el archivo de credenciales en la misma carpeta.
# ¡Recuerda NUNCA subir este archivo a un repositorio público!
CREDENTIALS_FILE = 'firebase_credentials.json'

try:
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Error: El archivo de credenciales '{CREDENTIALS_FILE}' no se encontró.")
    
    cred = credentials.Certificate(CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión con Firebase establecida correctamente.")

except Exception as e:
    print(f"❌ ERROR FATAL: No se pudo conectar con Firebase. {e}")
    db = None # Si no hay conexión, db será None y el script no continuará.

# ==============================================================================
# FUNCIÓN DE SCRAPING
# ==============================================================================
def get_player_data_from_futbolfantasy():
    """
    Visita la web de FutbolFantasy, extrae los datos de la tabla de mercado
    y los devuelve como una lista de diccionarios de jugadores.
    """
    url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
    print(f"\n📥 Obteniendo datos de jugadores desde: {url}")

    try:
        # Usamos un User-Agent para simular ser un navegador y evitar bloqueos
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15) # Timeout de 15 segundos
        response.raise_for_status()  # Lanza un error si la petición HTTP falla

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con FutbolFantasy: {e}")
        return None

    # Analizamos el contenido HTML de la página con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscamos la tabla de jugadores por su ID único: 'market-table-info'
    player_table = soup.find('table', id='market-table-info')

    if not player_table:
        print("❌ No se encontró la tabla de jugadores ('market-table-info'). La estructura de la web puede haber cambiado.")
        return None

    players_list = []
    # Iteramos sobre cada fila <tr> en el cuerpo <tbody> de la tabla
    for row in player_table.find('tbody').find_all('tr'):
        cells = row.find_all('td')  # Obtenemos todas las celdas <td> de la fila
        
        # Nos aseguramos de que la fila tiene el formato esperado (al menos 4 celdas)
        if len(cells) > 3:
            try:
                # --- Extracción de datos ---
                player_name = cells[1].find('a').text.strip()
                team_name = cells[1].find('span', class_='team-name').text.strip()
                price_text = cells[3].text.strip()
                
                # --- Limpieza de datos ---
                # Convierte '15.340.000 €' a un número entero 15340000
                price = int(re.sub(r'[.€\s]', '', price_text))
                
                # Creamos un ID único y predecible para cada jugador
                team_id = team_name.lower().replace(' ', '-')
                player_id = player_name.lower().replace(' ', '-')
                document_id = f"{team_id}-{player_id}"
                
                players_list.append({
                    'id': document_id,
                    'name': player_name,
                    'team': team_name,
                    'value': price
                })

            except (AttributeError, IndexError, ValueError) as e:
                # Si una fila está mal formada, la ignoramos y mostramos un aviso
                # print(f"⚠️ Saltando fila por formato inesperado. Error: {e}")
                continue
                
    print(f"👍 Se han extraído datos de {len(players_list)} jugadores.")
    return players_list

# ==============================================================================
# FUNCIÓN DE ACTUALIZACIÓN EN FIREBASE
# ==============================================================================
def update_data_in_firestore(players_list):
    """
    Recibe la lista de jugadores y actualiza los datos en la colección 'players'
    de Firestore de manera eficiente usando un batch.
    """
    if not db:
        print("❌ No hay conexión a Firebase. No se pueden actualizar los datos.")
        return

    print("🔄 Actualizando datos en Firestore... (esto puede tardar un momento)")
    
    # Un "batch" permite realizar múltiples operaciones en una sola llamada a la base de datos
    batch = db.batch()
    players_collection_ref = db.collection(u'players') # Reemplaza 'players' si tu colección se llama diferente

    for player in players_list:
        # Usamos el ID único del jugador como ID del documento en Firestore
        player_doc_ref = players_collection_ref.document(player['id'])
        
        # Creamos un diccionario con los datos a actualizar
        player_data = {
            'name': player['name'],
            'team': player['team'],
            'value': player['value'],
            'last_update': firestore.SERVER_TIMESTAMP # Añade la fecha de actualización
        }
        
        # Usamos 'set' con 'merge=True' para crear el jugador si no existe,
        # o para actualizar sus datos sin borrar otros campos (como 'ownerId').
        batch.set(player_doc_ref, player_data, merge=True)

    # Enviamos todas las operaciones a Firebase
    batch.commit()
    print(f"🔥 ¡Éxito! Base de datos actualizada con la información de {len(players_list)} jugadores.")


# ==============================================================================
# EJECUCIÓN PRINCIPAL DEL SCRIPT
# ==============================================================================
if __name__ == "__main__":
    print("==================================================")
    print("   INICIANDO SCRIPT DE ACTUALIZACIÓN FANTASY      ")
    print("==================================================")

    # 1. Obtener los datos de la web
    players = get_player_data_from_futbolfantasy()

    # 2. Si se obtuvieron los datos, actualizarlos en Firebase
    if players:
        update_data_in_firestore(players)
    else:
        print("\n❌ No se obtuvieron datos de jugadores, no se realizará ninguna actualización en Firebase.")
    
    print("\nSCRIPT FINALIZADO.")
