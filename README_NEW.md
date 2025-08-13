# ⚽ Mercato - Fantasy Football League Manager

Una aplicación web completa para gestionar tu liga de fantasy football con datos **REALES** de LaLiga Fantasy obtenidos mediante web scraping.

## 🌟 Características Principales

- ✅ **Datos REALES de LaLiga Fantasy** - 43 jugadores reales con precios y estadísticas actualizadas
- ✅ **Interfaz web moderna** - HTML5, Tailwind CSS, JavaScript vanilla
- ✅ **Base de datos en tiempo real** - Firebase Firestore con sincronización automática
- ✅ **Búsqueda inteligente** - Busca jugadores por nombre, equipo o posición
- ✅ **Gestión de plantilla** - Añade/elimina jugadores con validación de presupuesto
- ✅ **Web Scraping automatizado** - Datos actualizados desde FutbolFantasy.com
- ✅ **Validación de formaciones** - Control de posiciones y límites de jugadores

## 🚀 Configuración Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/mercato.git
cd mercato
```

### 2. Configurar Firebase
1. Crea un proyecto en [Firebase Console](https://console.firebase.google.com)
2. Habilita Firestore Database
3. Descarga el archivo de configuración y renómbralo como `firebase-key.json`
4. Colócalo en el directorio `backend/`

### 3. Instalar Dependencias Python
```bash
cd backend
pip install -r requirements.txt
```

### 4. Poblar con Datos REALES
Abre `frontend/index.html` en tu navegador y:
1. Presiona el botón **"⚡ LaLiga Fantasy REAL"** (rojo)
2. Confirma la población de datos
3. ¡Ya tienes 43 jugadores reales de LaLiga Fantasy!

## 📊 Datos Disponibles

### Estadísticas de LaLiga Fantasy (Temporada 2024/25)
- **43 jugadores** de LaLiga Fantasy
- **10 equipos** representados (Real Madrid, Barcelona, Atlético, etc.)
- **€1.836 billones** en valor total de mercado
- **Posiciones**: DEL (14), MED (15), POR (6), DEF (8)

### Top Jugadores Más Valiosos
1. **Kylian Mbappé** (Real Madrid) - €120M
2. **Jude Bellingham** (Real Madrid) - €105M  
3. **Vinícius Jr.** (Real Madrid) - €95M
4. **Robert Lewandowski** (FC Barcelona) - €85M
5. **Pedri** (FC Barcelona) - €75M

## 🔧 Uso de la Aplicación

### Interfaz Web
1. **Abrir**: `frontend/index.html` en cualquier navegador
2. **Búsqueda**: Usa el modal "Buscar Jugador" para encontrar jugadores
3. **Añadir**: Selecciona jugadores y añádelos a tu plantilla
4. **Gestión**: Controla tu presupuesto (€100M) y formación

### Funciones de Desarrollo (Solo en localhost)
```javascript
// En la consola del navegador:

// Poblar con datos REALES de LaLiga Fantasy
populateRealLaLigaFantasy();

// Verificar estado de la base de datos
checkRealDataStatus();

// Obtener estadísticas por equipo
getDetailedTeamStatistics();

// Búsqueda avanzada
searchPlayersByCriteria({
    position: 'DEL',        // Delanteros
    team: 'Real Madrid',    // Equipo específico
    minValue: 50000000,     // Valor mínimo €50M
    minPoints: 80           // Puntos mínimos 80
});
```

## 🕷️ Web Scraping

### Scraper Automático
El sistema incluye scrapers avanzados para obtener datos actualizados:

```bash
# Ejecutar scraper manual
cd backend
python scraper/futbolfantasy_advanced.py

# Actualizar base de datos Firebase automáticamente
python ../update_laliga_fantasy.py
```

### Fuente de Datos
- **URL**: [FutbolFantasy.com - LaLiga Analytics](https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado)
- **Método**: BeautifulSoup4 con múltiples estrategias de extracción
- **Datos**: Precios, puntos, estadísticas, equipos, posiciones

## 📁 Estructura del Proyecto

```
mercato/
├── frontend/
│   ├── index.html                      # Aplicación web principal
│   ├── app.js                         # Lógica de la aplicación
│   ├── populate-db.js                 # Datos de muestra (legacy)
│   └── populate-laliga-fantasy.js     # Datos REALES de LaLiga Fantasy
├── backend/
│   ├── scraper/
│   │   ├── futbolfantasy_advanced.py  # Scraper principal
│   │   └── marca_scraper.py           # Scraper MARCA (legacy)
│   ├── firebase-key.json             # Credenciales Firebase
│   ├── futbolfantasy_players.json    # Dataset generado
│   └── requirements.txt              # Dependencias Python
├── update_laliga_fantasy.py          # Script de actualización automática
└── README.md                         # Este archivo
```

## 🎯 Características Técnicas

### Frontend
- **Framework**: HTML5 + Tailwind CSS + Vanilla JavaScript
- **Base de datos**: Firebase Firestore con listeners en tiempo real
- **Autenticación**: Firebase Anonymous Auth
- **Responsive**: Optimizado para desktop y móvil

### Backend
- **Lenguaje**: Python 3.11+
- **Scraping**: BeautifulSoup4, requests, lxml
- **Base de datos**: Firebase Admin SDK
- **Análisis**: Extracción de JSON y HTML parsing avanzado

### Automatización
- **GitHub Actions**: CI/CD pipeline (configurado)
- **Scraping automático**: Scripts de actualización periódica
- **Validación**: Control de errores y fallbacks

## 🚀 Despliegue

### GitHub Pages
1. Habilita GitHub Pages en tu repositorio
2. Configura las variables de entorno de Firebase
3. La aplicación se desplegará automáticamente

### Local
```bash
# Servidor local simple
cd frontend
python -m http.server 8000
# Abre http://localhost:8000
```

## 🔄 Actualización de Datos

### Manual
1. Ejecuta el scraper: `python backend/scraper/futbolfantasy_advanced.py`
2. Actualiza Firebase: `python update_laliga_fantasy.py`

### Automática
Los datos se pueden actualizar automáticamente mediante:
- **Cron jobs** en servidores Linux
- **GitHub Actions** con schedule
- **Firebase Functions** con triggers temporales

## 🛠️ Desarrollo

### Requisitos
- Python 3.11+
- Navegador moderno (Chrome, Firefox, Safari)
- Cuenta de Firebase
- Conexión a internet (para scraping)

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/mercato.git
cd mercato

# Instalar dependencias
pip install -r backend/requirements.txt

# Configurar Firebase (ver sección de configuración)

# Abrir aplicación
open frontend/index.html
```

## 📈 Roadmap

- [x] ✅ Integración con datos reales de LaLiga Fantasy
- [x] ✅ Web scraping automatizado de FutbolFantasy.com
- [x] ✅ Base de datos con 43 jugadores reales
- [x] ✅ Interfaz de búsqueda avanzada
- [ ] 🔄 Actualización automática diaria de precios
- [ ] 🔄 Sistema de ligas y competición entre usuarios
- [ ] 🔄 Notificaciones de cambios de precios
- [ ] 🔄 Análisis predictivo de rendimiento
- [ ] 🔄 Integración con APIs oficiales

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🌐 Enlaces

- **Demo**: [Ver aplicación en vivo](https://tu-usuario.github.io/mercato)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/mercato/wiki)
- **Issues**: [Reportar bugs](https://github.com/tu-usuario/mercato/issues)
- **Fuente de datos**: [FutbolFantasy.com](https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado)

---

**Creado con ❤️ para la comunidad de Fantasy Football** 

🔥 **Datos actualizados de LaLiga Fantasy 2024/25** | ⚡ **43 jugadores reales** | 🌐 **Web scraping automatizado**
