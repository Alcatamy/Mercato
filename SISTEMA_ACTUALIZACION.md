# 🔄 Sistema de Actualización de Datos - Mercato

## 📊 **¿Cómo se Actualizan los Datos?**

### 🟢 **TIEMPO REAL (En la Aplicación Web)**

**SÍ - Los datos se actualizan automáticamente:**

✅ **Firebase Realtime Listeners** - Configurado en `app.js`:
```javascript
// Players - Se actualiza al instante cuando cambia la DB
firestoreFunctions.onSnapshot(collection(db, 'players'), snapshot => {
    allPlayers = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderAllTabs(); // Re-renderiza automáticamente
});

// Market - Ofertas y ventas se ven inmediatamente
firestoreFunctions.onSnapshot(collection(db, 'market'), snapshot => {
    marketItems = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderMarketTab(); // Actualiza mercado al instante
});

// Auctions - Subastas en tiempo real
firestoreFunctions.onSnapshot(collection(db, 'auctions'), snapshot => {
    auctionItems = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderAuctionsTab(); // Actualiza subastas al instante
});
```

### 🤖 **ACTUALIZACIÓN AUTOMÁTICA DE VALORES (Scripts)**

**Configuración Actual:**

#### 1. **Script Principal: `update_laliga_fantasy_final.py`**
- 🎯 **Fuente:** `https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado`
- 🛠️ **Tecnología:** Playwright (web scraping avanzado)
- 📊 **Datos:** Valores reales de jugadores LaLiga Fantasy
- 🔄 **Frecuencia:** Manual (necesita programarse)

#### 2. **Automatizador: `automation.py`**
- ⏰ **Programado para:** Cada 12 horas
- 🎯 **Ejecuta:** `update_laliga_fantasy.py`
- 📝 **Logging:** Guarda historial en `mercato_automation.log`

## 🕐 **Frecuencias de Actualización**

### **Inmediato (0 segundos):**
- ✅ Ofertas de mercado entre managers
- ✅ Subastas y pujas
- ✅ Intercambios entre equipos
- ✅ Fichajes y traspasos
- ✅ Cambios en plantillas

### **Cada 12 horas (Automático):**
- 📈 Valores de jugadores de FutbolFantasy.com
- 🏃‍♂️ Stats de rendimiento
- 💰 Precios de mercado actualizados
- 🎯 Datos de jornada actual

### **Manual (Cuando ejecutes scripts):**
- 🔄 `update_laliga_fantasy_final.py` - Actualización completa
- 🧹 `clean_duplicates.py` - Limpieza de duplicados
- 📊 `check_players.py` - Verificación de estado

## 🚀 **¿Cómo Activar Actualizaciones Automáticas?**

### **Opción 1: Ejecutar Automatizador**
```bash
# En tu terminal
cd "C:\Users\adrian.alcaide\Documents\Proyectos\Mercato"
python automation.py
```
- ⏰ Se ejecutará cada 12 horas automáticamente
- 📝 Creará logs en `mercato_automation.log`

### **Opción 2: Programar con Windows Task Scheduler**
1. Abrir **Programador de Tareas** de Windows
2. Crear tarea básica
3. Programar para ejecutar `automation.py` diariamente
4. Configurar usuario y permisos

### **Opción 3: Actualización Manual**
```bash
# Actualizar valores inmediatamente
python update_laliga_fantasy_final.py
```

## 📊 **Estado Actual del Sistema**

### ✅ **ACTUALIZADO - 14 Agosto 2025:**
- ✅ Firebase Realtime Updates (ofertas, mercado, subastas)
- ✅ Scripts de scraping configurados y funcionando
- ✅ Base de datos actualizada con 528 jugadores únicos
- ✅ Valores actuales de FutbolFantasy.com (14/08/2025)
- ✅ Credenciales Firebase configuradas correctamente
- ✅ Módulo 'schedule' instalado para automatización

### 💰 **Datos Actuales:**
- **Total jugadores:** 528 con valores reales
- **Valor mercado:** 5,020,293,526 €
- **Equipos:** 20 equipos de LaLiga
- **Última actualización:** 14 Agosto 2025, 08:10

### 🏆 **Top 5 Más Caros:**
1. Lamine Yamal (Barcelona) - 139,936,566 €
2. Kylian Mbappe (Real Madrid) - 138,329,088 €
3. Raphinha (Barcelona) - 117,198,564 €
4. Julian Alvarez (Atlético) - 102,815,341 €
5. Pedri Gonzalez (Barcelona) - 102,556,166 €

### ⚠️ **Para Activar Automatización:**
- Ejecutar: `python automation.py` para updates cada 12h
- O usar: `python manage_updates.py` para gestión interactiva

## 🎯 **Recomendaciones**

### **Para Desarrollo/Testing:**
- Ejecutar scripts manualmente cuando necesites datos frescos
- Los cambios del mercado interno se ven inmediatamente

### **Para Producción:**
- Configurar `automation.py` para que se ejecute automáticamente
- Considerar usar un servidor/VPS para automatización 24/7
- Monitorear logs para asegurar que funciona correctamente

## 🔍 **Verificar Estado Actual**
```bash
# Ver últimos jugadores actualizados
python backend/check_players.py

# Ver logs de automatización
type mercato_automation.log
```

## 📈 **Flujo de Datos Completo**

```
FutbolFantasy.com 
    ↓ (cada 12h - automation.py)
update_laliga_fantasy_final.py
    ↓ (scraping + processing)
Firebase Database
    ↓ (tiempo real - onSnapshot)
Interfaz Web (app.js)
    ↓ (instantáneo)
Usuario Final
```

**RESUMEN:** Las transacciones entre managers son instantáneas, pero los valores de FutbolFantasy.com necesitan activar la automatización para actualizarse cada 12 horas.
