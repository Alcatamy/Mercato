"""
Configuración central de Firebase Admin SDK
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional


class FirebaseManager:
    """Gestor centralizado para Firebase Admin SDK"""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self) -> Optional[firestore.Client]:
        """
        Inicializar Firebase Admin SDK
        
        Returns:
            Cliente de Firestore o None si hay error
        """
        if self._db is not None:
            return self._db
        
        try:
            # Método 1: Credenciales desde archivo local
            if os.path.exists('firebase-admin-key.json'):
                print("🔑 Usando credenciales desde archivo local")
                cred = credentials.Certificate('firebase-admin-key.json')
            
            # Método 2: Credenciales desde variable de entorno (GitHub Actions)
            elif os.environ.get('FIREBASE_CREDENTIALS'):
                print("🔑 Usando credenciales desde variable de entorno")
                firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
                cred_dict = json.loads(firebase_credentials)
                cred = credentials.Certificate(cred_dict)
            
            # Método 3: Credenciales por defecto (Cloud Functions, etc.)
            else:
                print("🔑 Intentando usar credenciales por defecto de la aplicación")
                cred = credentials.ApplicationDefault()
            
            # Inicializar Firebase Admin
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            
            self._db = firestore.client()
            print("✅ Firebase Admin SDK inicializado correctamente")
            return self._db
            
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {e}")
            return None
    
    def get_db(self) -> Optional[firestore.Client]:
        """
        Obtener cliente de Firestore
        
        Returns:
            Cliente de Firestore o None si no está inicializado
        """
        if self._db is None:
            return self.initialize()
        return self._db


# Instancia global del gestor
firebase_manager = FirebaseManager()
