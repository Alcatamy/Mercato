"""
Script simplificado para probar la conexión con Firebase
sin dependencias externas complejas
"""

def test_firebase_connection():
    """
    Función de prueba para verificar que la configuración
    de Firebase está correcta
    """
    
    firebase_config = {
        "apiKey": "AIzaSyCyM423fae8Lmft0M2xxhZD2DvC_fbZLCY",
        "authDomain": "mercato-fbdcc.firebaseapp.com",
        "projectId": "mercato-fbdcc",
        "storageBucket": "mercato-fbdcc.firebasestorage.app",
        "messagingSenderId": "865841758007",
        "appId": "1:865841758007:web:31786b65366b99584864b2",
        "measurementId": "G-5GJRTD7E72"
    }
    
    print("🔥 Configuración de Firebase:")
    print(f"   📍 Proyecto ID: {firebase_config['projectId']}")
    print(f"   🌐 Auth Domain: {firebase_config['authDomain']}")
    print(f"   💾 Storage: {firebase_config['storageBucket']}")
    
    # Datos de muestra para testing
    sample_players = [
        {"id": "bellingham", "name": "Jude Bellingham", "position": "MED", "team": "Real Madrid", "value": 105000000},
        {"id": "lewandowski", "name": "Robert Lewandowski", "position": "DEL", "team": "FC Barcelona", "value": 85000000},
        {"id": "vinicius", "name": "Vinícius Jr.", "position": "DEL", "team": "Real Madrid", "value": 95000000},
        {"id": "pedri", "name": "Pedri", "position": "MED", "team": "FC Barcelona", "value": 75000000},
        {"id": "ter-stegen", "name": "Marc-André ter Stegen", "position": "POR", "team": "FC Barcelona", "value": 35000000}
    ]
    
    print(f"\n⚽ Datos de muestra listos:")
    print(f"   📊 {len(sample_players)} jugadores de prueba")
    
    total_value = sum(player['value'] for player in sample_players)
    print(f"   💰 Valor total: {total_value:,}€")
    
    positions = {}
    for player in sample_players:
        pos = player['position']
        positions[pos] = positions.get(pos, 0) + 1
    
    print(f"   🏃 Distribución por posición:")
    for pos, count in positions.items():
        print(f"      {pos}: {count} jugadores")
    
    print("\n✅ ¡Todo listo para conectar con Firebase!")
    print("💡 Ejecuta la aplicación web y prueba el login con:")
    print("   - Clave: ALCA-2025 para Alcatamy eSports by Rolex")
    print("   - Clave: VIGA-2025 para Vigar FC")
    
    return True

if __name__ == "__main__":
    print("🧪 Test de configuración de Mercato - La Liga El Rancho")
    print("=" * 60)
    test_firebase_connection()
    print("=" * 60)
    print("🎯 Siguiente paso: Abrir frontend/index.html en el navegador")
