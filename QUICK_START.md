# 🚀 Inicio Rápido - Mercato La Liga El Rancho

¡Tu proyecto está listo! Aquí tienes los pasos finales para ponerlo en funcionamiento:

## ✅ Estado Actual
- ✅ Firebase configurado (`mercato-fbdcc`)
- ✅ Reglas de Firestore establecidas
- ✅ Frontend configurado con tu proyecto
- ✅ Backend listo para datos

## 🎯 Próximos Pasos (5-10 minutos)

### 1. Probar la Aplicación Web
```bash
# Abrir en navegador:
frontend/index.html
```

**Claves de prueba:**
- `ALCA-2025` → Alcatamy eSports by Rolex
- `VIGA-2025` → Vigar FC
- `BA10-2025` → Baena10
- `DUBA-2025` → Dubai cITY FC
- `MANGA-2025` → Visite La Manga FC
- `MORE-2025` → Morenazos FC

### 2. Poblar Base de Datos (Opcional)

Si quieres datos iniciales, necesitas:

**Para GitHub (recomendado):**
1. Sube el código a GitHub
2. Configura GitHub Pages (Settings > Pages)
3. Añade secret `FIREBASE_CREDENTIALS` con las credenciales de admin
4. El GitHub Action poblará automáticamente la base de datos

**Para local (manual):**
1. Instala dependencias: `pip install firebase-admin requests`
2. Descarga credenciales de Firebase Admin
3. Ejecuta: `python backend/player_updater.py`

### 3. Desplegar en GitHub Pages

1. **Crea repositorio en GitHub**
2. **Push del código:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Mercato La Liga El Rancho"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/mercato.git
   git push -u origin main
   ```

3. **Activar GitHub Pages:**
   - Settings > Pages
   - Source: Deploy from branch
   - Branch: main, / (root)

4. **Configurar Secrets (para datos automáticos):**
   - Settings > Secrets and variables > Actions
   - Añadir `FIREBASE_CREDENTIALS` (JSON completo)
   - Opcionalmente: `MARCA_API_TOKEN`

## 🎮 Funcionalidades Disponibles

- ✅ **Login de Managers** con claves secretas
- ✅ **Gestión de Plantillas** (añadir/eliminar jugadores)
- ✅ **Mercado de Traspasos** (vender/comprar con ofertas)
- ✅ **Sistema de Subastas** (24h con pujas en tiempo real)
- ✅ **Intercambios Complejos** (jugadores + dinero)
- ✅ **Contratos Descargables** en PDF
- ✅ **Tiempo Real** con Firebase
- ⏳ **Actualización Automática** (con GitHub Actions)

## 🔧 Personalización

### Cambiar Claves de Managers
Edita `frontend/app.js`, línea ~25:
```javascript
const managerKeys = {
    'alcatamy-esports-by-rolex': 'TU-NUEVA-CLAVE',
    // ... resto de claves
};
```

### Añadir Más Equipos
1. Modifica `managerNames` en `frontend/app.js`
2. Añade claves correspondientes en `managerKeys`
3. Actualiza la documentación

### Conectar API Real de MARCA
1. Obtén token de [MARCA Fantasy API](https://github.com/alxgarci/marca-fantasy-api-scraper-updated)
2. Añádelo como secret `MARCA_API_TOKEN` en GitHub
3. Los datos se actualizarán automáticamente cada día

## 🆘 Solución de Problemas

**No se cargan los managers:**
- Verifica que Firebase esté bien configurado
- Comprueba la consola del navegador (F12)

**Error de autenticación:**
- Asegúrate que la autenticación anónima esté habilitada en Firebase

**No hay jugadores:**
- Ejecuta el script poblador o GitHub Action
- Verifica que la colección `players` existe en Firestore

## 📞 Soporte

- 📖 Documentación completa: `docs/setup.md`
- 🔧 API Reference: `docs/api.md`
- 🐛 Issues: Crear issue en GitHub

---

**¡Que comience la temporada! ⚽🏆**

Tu plataforma de mercado está lista para gestionar todos los traspasos, subastas e intercambios de La Liga El Rancho 2025/2026.
