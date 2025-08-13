# API Documentation - Mercado La Liga El Rancho

Documentación de la estructura de datos y las funciones principales de la aplicación.

## 🗃️ Estructura de Datos (Firebase Firestore)

### Colección: `managers`

Información de los equipos/managers de la liga.

```javascript
{
  id: "alcatamy-esports-by-rolex",
  name: "Alcatamy eSports by Rolex",
  createdAt: timestamp,
  totalValue: 450000000,  // Valor total de la plantilla
  playerCount: 15         // Número de jugadores
}
```

### Colección: `players`

Información completa de todos los jugadores disponibles.

```javascript
{
  id: "bellingham",
  name: "Jude Bellingham",
  position: "MED",        // POR, DEF, MED, DEL
  team: "Real Madrid",
  value: 105000000,       // Valor en euros
  points: 89,             // Puntos en Fantasy
  ownerId: "vigar-fc",    // ID del manager propietario (null si libre)
  ownerName: "Vigar FC",  // Nombre del manager propietario
  lastUpdated: timestamp,
  status: "available"     // available, injured, suspended
}
```

### Colección: `market`

Jugadores puestos en venta por los managers.

```javascript
{
  id: "market_item_123",
  playerId: "bellingham",
  playerName: "Jude Bellingham",
  sellerId: "vigar-fc",
  sellerName: "Vigar FC",
  price: 110000000,       // Precio de venta
  createdAt: timestamp
}
```

#### Subcolección: `market/{marketId}/offers`

Ofertas realizadas para jugadores en venta.

```javascript
{
  id: "offer_456",
  buyerId: "dubai-city-fc",
  buyerName: "Dubai cITY FC",
  amount: 108000000,      // Cantidad ofrecida
  createdAt: timestamp
}
```

### Colección: `auctions`

Subastas activas de jugadores.

```javascript
{
  id: "auction_789",
  playerId: "lewandowski",
  playerName: "Robert Lewandowski",
  sellerId: "baena10",
  sellerName: "Baena10",
  startPrice: 80000000,   // Precio de salida
  endTime: timestamp,     // Fin de la subasta (24h)
  createdAt: timestamp
}
```

#### Subcolección: `auctions/{auctionId}/bids`

Pujas realizadas en las subastas.

```javascript
{
  id: "bid_101",
  bidderId: "morenazos-fc",
  bidderName: "Morenazos FC",
  amount: 85000000,       // Cantidad pujada
  timestamp: timestamp
}
```

### Colección: `trades`

Propuestas de intercambio entre managers.

```javascript
{
  id: "trade_202",
  proposerId: "alcatamy-esports-by-rolex",
  proposerName: "Alcatamy eSports by Rolex",
  receiverId: "visite-la-manga-fc",
  receiverName: "Visite La Manga FC",
  proposerPlayers: ["bellingham", "modric"],  // IDs de jugadores ofrecidos
  receiverPlayers: ["oyarzabal"],             // IDs de jugadores solicitados
  cashFromProposer: 15000000,                 // Dinero adicional del proponente
  cashFromReceiver: 0,                        // Dinero adicional del receptor
  status: "pending",                          // pending, accepted, rejected
  timestamp: timestamp
}
```

### Colección: `system`

Información del sistema y estadísticas.

```javascript
{
  id: "update_stats",
  lastUpdate: timestamp,
  playersUpdated: 245,
  totalMarketValue: 12500000000,
  source: "real_api"      // real_api o sample_data
}
```

## 🔧 Funciones JavaScript Principales

### Autenticación y Gestión de Usuarios

```javascript
// Verificar clave de manager
window.verifyManagerKey(managerId)

// Cerrar sesión
window.cancelLogin()
```

### Gestión de Plantilla

```javascript
// Abrir modal de edición de plantilla
window.openEditSquadModal()

// Añadir jugador a la plantilla
window.addPlayerToSquad()

// Eliminar jugador de la plantilla
window.deletePlayerFromSquad(playerId, playerName)
```

### Mercado de Traspasos

```javascript
// Poner jugador en venta
window.openSellModal(playerId)
window.listPlayerForSale(playerId)

// Hacer oferta por jugador
window.openOfferModal(marketId)
window.submitOffer(marketId)

// Aceptar oferta recibida
window.acceptOffer(marketId, offerId)

// Retirar jugador del mercado
window.cancelSale(marketId)
```

### Sistema de Subastas

```javascript
// Iniciar subasta de jugador
window.openAuctionModal(playerId)
window.listPlayerForAuction(playerId)

// Realizar puja
window.placeBid(auctionId)

// Finalizar subasta (solo vendedor)
window.finalizeAuction(auctionId)

// Cancelar subasta sin pujas
window.cancelAuction(auctionId)
```

### Sistema de Intercambios

```javascript
// Proponer intercambio
window.openTradeModal()
window.submitTrade()

// Aceptar propuesta recibida
window.acceptTrade(tradeId)

// Rechazar propuesta
window.rejectTrade(tradeId)

// Cancelar propuesta enviada
window.cancelTrade(tradeId)
```

### Utilidades

```javascript
// Formatear moneda
formatCurrency(value) // Ej: 105000000 → "105.000.000 €"

// Formatear tiempo restante
formatTimeLeft(milliseconds) // Ej: 3600000 → "1h 0m restantes"

// Obtener estado de jugador
getPlayerStatus(playerId) // { status, text, class }

// Generar contrato de traspaso
generateContractText(type, data)
```

## 🔄 Backend API (Python)

### Clase MarcaFantasyAPI

```python
from scraper.marca_scraper import MarcaFantasyAPI

# Inicializar cliente
api = MarcaFantasyAPI(token="tu_token")

# Obtener todos los jugadores
players = api.get_all_players()

# Obtener jugador específico
player = api.get_player_by_id("bellingham")

# Obtener estado del mercado
status = api.get_market_status()

# Probar conexión
is_connected = api.test_connection()
```

### Clase Player (DataClass)

```python
@dataclass
class Player:
    id: str
    name: str
    position: str  # POR, DEF, MED, DEL
    team: str
    value: int
    points: int = 0
    status: str = "available"
```

### Firebase Manager

```python
from firebase_admin import FirebaseManager

# Inicializar Firebase
manager = FirebaseManager()
db = manager.initialize()

# Obtener cliente de Firestore
db = manager.get_db()
```

## 📊 Eventos en Tiempo Real

La aplicación utiliza Firebase Firestore listeners para actualizaciones en tiempo real:

```javascript
// Escuchar cambios en managers
onSnapshot(collection(db, 'managers'), snapshot => {
  // Actualizar lista de managers
});

// Escuchar cambios en jugadores
onSnapshot(collection(db, 'players'), snapshot => {
  // Actualizar plantillas y mercado
});

// Escuchar cambios en el mercado
onSnapshot(collection(db, 'market'), snapshot => {
  // Actualizar ofertas y ventas
});
```

## 🔐 Reglas de Seguridad (Firestore)

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permitir acceso autenticado
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
    
    // Reglas específicas para managers
    match /managers/{managerId} {
      allow read: if request.auth != null;
      allow write: if false; // Solo el sistema puede escribir
    }
    
    // Reglas para jugadores
    match /players/{playerId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null; // Permitir transferencias
    }
  }
}
```

## 🛠️ Configuración de Desarrollo

### Variables de Entorno

```bash
# Backend
FIREBASE_CREDENTIALS="{...}" # JSON de credenciales de Firebase
MARCA_API_TOKEN="tu_token"   # Token de MARCA Fantasy API (opcional)

# GitHub Secrets (para GitHub Actions)
FIREBASE_CREDENTIALS         # Credenciales de Firebase Admin
MARCA_API_TOKEN             # Token de MARCA API (opcional)
```

### Comandos de Desarrollo

```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Ejecutar actualizador de precios manualmente
python player_updater.py

# Probar scraper
python scraper/marca_scraper.py

# Ejecutar tests
python -m pytest tests/
```

---

Esta documentación cubre las principales funciones y estructuras de datos de la aplicación. Para más detalles sobre configuración, consulta `docs/setup.md`.
