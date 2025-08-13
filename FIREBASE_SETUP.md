# 🔥 Configuración Firebase para Mercato

## 📋 Instrucciones de Configuración

Para que la aplicación funcione completamente con Firebase, necesitas configurar las credenciales:

### 1. Configuración de Firebase Project

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. En la configuración del proyecto, ve a "Service accounts"
4. Haz click en "Generate new private key"
5. Descarga el archivo JSON con las credenciales

### 2. Configuración del archivo de credenciales

1. Renombra el archivo descargado como `firebase-key.json`
2. Colócalo en el directorio `backend/`
3. Asegúrate de que la estructura sea:
   ```
   Mercato/
   ├── backend/
   │   ├── firebase-key.json  ← Aquí
   │   └── scraper/
   └── ...
   ```

### 3. Configuración de Firestore

1. En Firebase Console, ve a "Firestore Database"
2. Crea una nueva base de datos en modo "test" (para desarrollo)
3. La aplicación creará automáticamente la colección `available_players`

### 4. Variables del Frontend

En el archivo `frontend/js/firebase-config.js`, actualiza la configuración:

```javascript
const firebaseConfig = {
  apiKey: "tu-api-key",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "tu-app-id"
};
```

### 5. Ejecutar el actualizador

Una vez configurado todo:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar scraper y actualizar Firebase
python update_laliga_fantasy.py
```

## 🚀 Datos Disponibles

El scraper obtiene **~500 jugadores reales** de LaLiga con:
- ✅ Nombres reales de jugadores
- ✅ Equipos actuales de LaLiga 2024/25
- ✅ Posiciones (POR, DEF, MED, DEL)
- ✅ Valores de mercado realistas
- ✅ Estadísticas de rendimiento
- ✅ Coeficientes analíticos

## 📊 Fuente de Datos

- **Fuente primaria**: AnaliticaFantasy.com/oraculo-fantasy
- **Fallback**: Dataset realista con jugadores reales
- **Actualización**: Cada 12 horas automáticamente
- **Total jugadores**: ~400-500 jugadores únicos

## 🔧 Troubleshooting

### Error: "No se encontró firebase-key.json"
- Asegúrate de que el archivo esté en `backend/firebase-key.json`
- Verifica que el nombre sea exactamente `firebase-key.json`

### Error: "Permission denied"
- Verifica que las reglas de Firestore permitan lectura/escritura
- Asegúrate de que el service account tenga permisos

### Error de importación
- Instala las dependencias: `pip install -r requirements.txt`
- Activa el entorno virtual si estás usando uno

## 📁 Estructura de Datos

Cada jugador en Firebase tiene la estructura:

```json
{
  "id": "real_madrid_1",
  "name": "Mbappé",
  "position": "DEL",
  "team": "Real Madrid",
  "value": 113218438,
  "coefficient": 82.69,
  "points": 29,
  "average": 6.84,
  "starter_probability": 83,
  "status": "available",
  "source": "AnaliticaFantasy.com",
  "is_real_data": true,
  "last_updated": "2025-01-13T13:25:19"
}
```
