# ⚽ Mercato - LaLiga Fantasy App

**Aplicación completa de gestión de Fantasy Football para LaLiga con datos reales actualizados automáticamente cada 12 horas**

## 🌟 Características Principales

- ✅ **Datos Reales**: ~500 jugadores reales de LaLiga 2024/25 extraídos de AnaliticaFantasy.com
- ✅ **Scraping Automático**: Actualización cada 12 horas con datos reales como solicité el usuario
- ✅ **Base de Datos en Tiempo Real**: Firebase Firestore con sincronización automática
- ✅ **Frontend Moderno**: Interfaz responsive con Tailwind CSS
- ✅ **Búsqueda Avanzada**: Filtros por posición, equipo y valor
- ✅ **Plantilla Personalizable**: Gestión completa de tu equipo fantasy

## ✨ Características Principales

### 🎯 **Gestión de Plantillas Inteligente**
- **Búsqueda de API**: Selecciona jugadores reales de LaLiga con datos actualizados de MARCA Fantasy
- **Filtros avanzados**: Por posición, equipo y nombre
- **Entrada manual**: Crea jugadores personalizados cuando sea necesario
- **Prevención de duplicados**: El sistema evita añadir jugadores ya en plantillas

### 🏪 **Mercado en Tiempo Real**
- Poner jugadores a la venta con precio personalizado
- Sistema de ofertas y contraofertas
- Transferencias automáticas al aceptar ofertas
- Historial de transacciones

### 🔄 **Sistema de Intercambios**
- Proponer intercambios entre managers
- Negociaciones multiparte
- Validación automática de intercambios

### 🏛️ **Subastas de Jugadores**
- Subastas temporales con cuenta regresiva
- Pujas en tiempo real
- Sistema de notificaciones

### 🔐 **Autenticación Segura**
- Sistema de claves por manager
- Sesiones persistentes
- Protección de acciones sensibles

## 🏗️ Arquitectura

### Frontend
- **Tecnología**: HTML5, CSS (Tailwind), JavaScript vanilla
- **Base de datos**: Firebase Firestore (tiempo real)
- **Hosting**: GitHub Pages

### Backend
- **Tecnología**: Python 3.10+
- **Scraper**: Integración con marca-fantasy-api-scraper
- **Automatización**: GitHub Actions (cron jobs)
- **Base de datos**: Firebase Admin SDK

## 📁 Estructura del Proyecto

```
mercato/
├── frontend/
│   ├── index.html              # Aplicación web principal
│   ├── firebase-config.js      # Configuración de Firebase
│   └── assets/
├── backend/
│   ├── scraper/
│   │   ├── marca_scraper.py    # Scraper de la API de MARCA
│   │   └── player_updater.py   # Actualizador de precios
│   ├── firebase_admin.py       # Configuración Firebase Admin
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── update-prices.yml   # Automatización GitHub Actions
├── docs/
│   ├── setup.md               # Guía de configuración
│   └── api.md                 # Documentación de la API
└── README.md
```

## ⚙️ Configuración

### 1. Prerrequisitos
- Cuenta de GitHub
- Proyecto de Firebase configurado
- Token de acceso a MARCA Fantasy API

### 2. Configuración de Firebase
1. Crear proyecto en [Firebase Console](https://console.firebase.google.com)
2. Habilitar Firestore Database
3. Configurar Authentication (método anónimo)
4. Descargar credenciales de servicio (`firebase-admin-key.json`)

### 3. Configuración del Backend
```bash
cd backend
pip install -r requirements.txt
```

### 4. Variables de Entorno
Configurar en GitHub Secrets:
- `FIREBASE_CREDENTIALS`: Contenido del archivo de credenciales JSON
- `MARCA_API_TOKEN`: Token de acceso a la API de MARCA

## 🚀 Despliegue

### Frontend (GitHub Pages)
1. Push del código a tu repositorio
2. Activar GitHub Pages en Settings > Pages
3. La aplicación estará disponible en `https://usuario.github.io/repositorio`

### Backend (GitHub Actions)
El script de actualización se ejecuta automáticamente cada día a las 2:00 AM UTC.

## 👥 Managers de la Liga

La aplicación está configurada para 6 equipos:
- Alcatamy eSports by Rolex
- Vigar FC  
- Baena10
- Dubai cITY FC
- Visite La Manga FC
- Morenazos FC

## 🔐 Seguridad

- Autenticación por claves secretas para cada manager
- Credenciales de Firebase protegidas como secrets de GitHub
- Validación de transacciones en tiempo real

## 📈 Funcionalidades Avanzadas

- **Contratos de Traspaso**: Generación automática de documentos PDF
- **Historial de Transacciones**: Registro completo de todas las operaciones
- **Notificaciones en Tiempo Real**: Sistema de alertas para ofertas y pujas
- **Estadísticas**: Dashboard con métricas de la liga

## 🛠️ Desarrollo

### Comandos Útiles
```bash
# Ejecutar actualizador manualmente
python backend/player_updater.py

# Configurar entorno de desarrollo
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### Testing
```bash
# Ejecutar tests
python -m pytest backend/tests/

# Verificar scraper
python backend/scraper/marca_scraper.py --test
```

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles.

## 🤝 Contribuir

1. Fork del proyecto
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

Para problemas o sugerencias, crear un issue en GitHub o contactar al administrador de la liga.

---

**¡Que gane el mejor manager! ⚽🏆**
