#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis del HTML de FutbolFantasy para entender la estructura
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_page():
    url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
    print(f"🔍 Analizando estructura de: {url}")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=15)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Buscar elementos que contengan información de jugadores
    print("\n📋 Buscando elementos con datos de jugadores...")
    
    # Método 1: Buscar por texto que contenga posiciones
    page_text = soup.get_text()
    lines = page_text.split('\n')
    
    player_lines = []
    for line in lines:
        if any(pos in line for pos in ['DEL', 'MED', 'DEF', 'POR']) and ('Real Madrid' in line or 'Barcelona' in line or 'Valencia' in line):
            player_lines.append(line.strip())
    
    print(f"📝 Líneas encontradas con información de jugadores: {len(player_lines)}")
    
    for i, line in enumerate(player_lines[:10]):  # Solo mostrar las primeras 10
        print(f"  {i+1:2d}. {line}")
    
    # Método 2: Buscar en el HTML elementos específicos
    print(f"\n🔍 Buscando elementos HTML...")
    
    # Buscar divs, spans o elementos que contengan nombres de equipos conocidos
    teams = ['Real Madrid', 'Barcelona', 'Valencia', 'Atlético', 'Sevilla']
    for team in teams:
        elements = soup.find_all(text=re.compile(team, re.IGNORECASE))
        if elements:
            print(f"  🏟️  {team}: {len(elements)} menciones encontradas")
            
            # Buscar el contexto de estos elementos
            for element in elements[:3]:  # Solo los primeros 3
                parent = element.parent
                if parent:
                    print(f"    📄 Contexto: {parent.get_text()[:100]}...")
    
    # Método 3: Buscar patrones de precio
    print(f"\n💰 Buscando patrones de precios...")
    price_patterns = [
        r'\d+\.\d+\.\d+',  # Formato 15.340.000
        r'\d+\.\d+',       # Formato 15.340
        r'\d{6,}',         # Números grandes (6+ dígitos)
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, page_text)
        if matches:
            print(f"  💵 Patrón {pattern}: {len(matches)} coincidencias")
            print(f"    📊 Ejemplos: {matches[:5]}")
    
    # Método 4: Buscar elementos con clases específicas
    print(f"\n🎨 Buscando elementos con clases relevantes...")
    
    potential_classes = ['player', 'market', 'table', 'row', 'data']
    for class_name in potential_classes:
        elements = soup.find_all(attrs={'class': re.compile(class_name, re.IGNORECASE)})
        if elements:
            print(f"  🏷️  Clase *{class_name}*: {len(elements)} elementos")
    
    # Método 5: Mostrar una muestra del HTML
    print(f"\n📜 Muestra del HTML (primeros 2000 caracteres):")
    print("=" * 60)
    print(response.text[:2000])
    print("=" * 60)

if __name__ == "__main__":
    analyze_page()
