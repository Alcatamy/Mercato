# Guía de Configuración - Mercado La Liga El Rancho

Esta guía te ayudará a configurar y desplegar la aplicación completa paso a paso.

## 📋 Prerrequisitos

- Cuenta de GitHub
- Proyecto de Firebase
- Token de acceso a MARCA Fantasy API (opcional para datos reales)

## 🔥 Configuración de Firebase

### 1. Crear Proyecto Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com)
2. Haz clic en "Crear un proyecto"
3. Nombra tu proyecto (ej: `mercato-liga-rancho`)
4. Acepta los términos y crea el proyecto

### 2. Configurar Firestore Database

1. En la consola de Firebase, ve a **Firestore Database**
2. Haz clic en "Crear base de datos"
3. Selecciona "Empezar en modo de producción"
4. Elige una ubicación cercana (ej: `europe-west1`)

### 3. Configurar Authentication

1. Ve a **Authentication** → **Comenzar**
2. En la pestaña "Sign-in method"
3. Habilita "Anónimo" (necesario para la app web)
4. Guarda los cambios

### 4. Configurar Web App

1. En **Configuración del proyecto** (⚙️)
2. Desplázate hasta "Tus apps"
3. Haz clic en "Web" (icono `</>`)
4. Registra la app con nombre: `Mercado Liga Rancho`
5. **¡IMPORTANTE!** Copia la configuración que aparece:

```javascript
const firebaseConfig = {
  apiKey: "tu-api-key-aqui",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdefghijklmnop"
};
```

### 5. Configurar Firebase Admin (Backend)

1. Ve a **Configuración del proyecto** → **Cuentas de servicio**
2. Haz clic en "Generar nueva clave privada"
3. Se descargará un archivo JSON
4. **¡IMPORTANTE!** Guarda este archivo de forma segura
5. **NUNCA** subas este archivo a un repositorio público

## 🌐 Configuración del Frontend

### 1. Actualizar Configuración Firebase

Edita el archivo `frontend/firebase-config.js` y reemplaza el objeto `firebaseConfig` con tu configuración real obtenida en el paso anterior.

```javascript
const firebaseConfig = {
  // Tu configuración real aquí
  apiKey: "AIzaSyC...",
  authDomain: "tu-proyecto.firebaseapp.com",
  // ... resto de configuración
};
```

### 2. Verificar Reglas de Firestore

En la consola de Firebase, ve a **Firestore Database** → **Reglas** y configura:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permitir lectura y escritura autenticada
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 🤖 Configuración del Backend

### 1. Configurar Secrets de GitHub

En tu repositorio de GitHub:

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Crea los siguientes secrets:

**FIREBASE_CREDENTIALS** (Obligatorio)
- Abre el archivo JSON de credenciales de Firebase Admin
- Copia TODO el contenido del archivo
- Pégalo como valor de este secret

**MARCA_API_TOKEN** (Opcional)
- Si tienes acceso a la API de MARCA Fantasy
- Obtén tu token siguiendo [esta guía](https://github.com/alxgarci/marca-fantasy-api-scraper-updated)
- Pégalo como valor de este secret
- Si no tienes token, la app usará datos de muestra

### 2. Verificar GitHub Actions

El archivo `.github/workflows/update-prices.yml` ya está configurado para:
- Ejecutarse automáticamente cada día a las 2:00 AM UTC
- Poder ejecutarse manualmente desde GitHub Actions
- Usar los secrets configurados de forma segura

## 🚀 Despliegue

### 1. Desplegar Frontend (GitHub Pages)

1. En tu repositorio, ve a **Settings** → **Pages**
2. En "Source", selecciona "Deploy from a branch"
3. Selecciona la rama `main` y carpeta `/ (root)`
4. Haz clic en "Save"
5. Tu app estará disponible en: `https://tu-usuario.github.io/tu-repositorio`

### 2. Configurar Dominio Personalizado (Opcional)

Si tienes un dominio propio:
1. En **GitHub Pages settings**, añade tu dominio personalizado
2. Configura los registros DNS según las instrucciones de GitHub

## 🧪 Verificar Configuración

### 1. Probar Frontend

1. Abre tu aplicación web desplegada
2. Deberías ver la página de selección de manager
3. Intenta iniciar sesión con una de las claves:
   - `ALCA-2025` para Alcatamy eSports by Rolex
   - `VIGA-2025` para Vigar FC
   - etc.

### 2. Probar Backend

1. Ve a **GitHub Actions** en tu repositorio
2. Ejecuta manualmente "Update Player Prices Nightly"
3. Verifica que se ejecute sin errores
4. Comprueba en Firebase Console que se crearon las colecciones:
   - `managers`
   - `players`
   - `system`

### 3. Verificar Datos en Firebase

En Firestore Database deberías ver:
- Colección `managers` con 6 documentos
- Colección `players` con datos de jugadores
- Colección `system` con estadísticas de actualización

## 🔐 Configuración de Seguridad

### 1. Claves de Manager

Por defecto, las claves son:
- `ALCA-2025` - Alcatamy eSports by Rolex
- `VIGA-2025` - Vigar FC
- `BA10-2025` - Baena10
- `DUBA-2025` - Dubai cITY FC
- `MANGA-2025` - Visite La Manga FC
- `MORE-2025` - Morenazos FC

**¡IMPORTANTE!** Cambia estas claves en `frontend/app.js` antes del despliegue.

### 2. Mejorar Seguridad (Recomendado)

Para mayor seguridad, considera:
1. Implementar autenticación por email/contraseña
2. Usar Cloud Functions para lógica sensible
3. Configurar reglas de Firestore más restrictivas

## 🆘 Solución de Problemas

### Error: "No se pudo conectar con la base de datos"
- Verifica la configuración de Firebase en `firebase-config.js`
- Asegúrate de que las reglas de Firestore permiten acceso autenticado
- Comprueba que está habilitada la autenticación anónima

### Error en GitHub Actions
- Verifica que los secrets están configurados correctamente
- Revisa los logs de la ejecución en GitHub Actions
- Asegúrate de que el archivo de credenciales JSON es válido

### Jugadores no aparecen
- Ejecuta manualmente el workflow de GitHub Actions
- Verifica que la colección `players` existe en Firestore
- Comprueba los logs del script `player_updater.py`

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en GitHub Actions
2. Verifica la configuración en Firebase Console
3. Consulta la documentación de Firebase
4. Crea un issue en GitHub con detalles del error

---

¡Una vez completada esta configuración, tu aplicación estará lista para gestionar el mercado de La Liga El Rancho! ⚽🏆
