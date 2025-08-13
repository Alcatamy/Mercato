#!/usr/bin/env python3
"""
🤖 AUTOMATIZADOR DE MERCATO
Ejecuta el scraper de FutbolFantasy.com cada 12 horas y mantiene la base de datos actualizada
Fuente: https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado
"""

import schedule
import time
import subprocess
import logging
import os
import sys
from datetime import datetime
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mercato_automation.log'),
        logging.StreamHandler()
    ]
)

class MercatoAutomation:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = os.path.join(self.project_root, '.venv', 'Scripts', 'python.exe')
        self.update_script = os.path.join(self.project_root, 'update_laliga_fantasy.py')
        self.log_file = os.path.join(self.project_root, 'automation_log.json')
        
        # Asegurar que el ejecutable de Python existe
        if not os.path.exists(self.python_exe):
            self.python_exe = 'python'  # Fallback al Python del sistema
    
    def run_update(self):
        """Ejecutar actualización de datos"""
        try:
            logging.info("🚀 INICIANDO ACTUALIZACIÓN AUTOMÁTICA")
            logging.info("=" * 50)
            
            # Ejecutar el script de actualización
            result = subprocess.run(
                [self.python_exe, self.update_script],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # Timeout de 5 minutos
            )
            
            if result.returncode == 0:
                logging.info("✅ Actualización completada exitosamente")
                self.log_execution(True, result.stdout)
                return True
            else:
                logging.error(f"❌ Error en actualización: {result.stderr}")
                self.log_execution(False, result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("⏰ Timeout: La actualización tardó más de 5 minutos")
            self.log_execution(False, "Timeout después de 5 minutos")
            return False
        except Exception as e:
            logging.error(f"💥 Error inesperado: {e}")
            self.log_execution(False, str(e))
            return False
    
    def log_execution(self, success: bool, output: str):
        """Registrar ejecución en log JSON"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'output': output[:1000],  # Limitar output a 1000 caracteres
            'next_run': schedule.jobs[0].next_run.isoformat() if schedule.jobs else None
        }
        
        # Leer log existente
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Agregar nueva entrada
        logs.append(log_entry)
        
        # Mantener solo los últimos 50 registros
        logs = logs[-50:]
        
        # Guardar log actualizado
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def show_status(self):
        """Mostrar estado actual del automatizador"""
        print("\n📊 ESTADO DEL AUTOMATIZADOR MERCATO")
        print("=" * 40)
        
        # Información del siguiente trabajo
        if schedule.jobs:
            next_job = schedule.jobs[0]
            next_run = next_job.next_run
            print(f"⏰ Próxima actualización: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Tiempo hasta la próxima ejecución
            time_until = next_run - datetime.now()
            hours = int(time_until.total_seconds() // 3600)
            minutes = int((time_until.total_seconds() % 3600) // 60)
            print(f"⏳ Tiempo restante: {hours}h {minutes}m")
        else:
            print("⚠️  No hay trabajos programados")
        
        # Último log
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    if logs:
                        last_log = logs[-1]
                        status = "✅ Éxito" if last_log['success'] else "❌ Error"
                        print(f"📝 Última ejecución: {last_log['timestamp']} - {status}")
            except:
                print("📝 No hay logs disponibles")
        
        print(f"🐍 Python ejecutable: {self.python_exe}")
        print(f"📁 Directorio de trabajo: {self.project_root}")
    
    def run_scheduler(self):
        """Ejecutar el programador principal"""
        logging.info("🤖 AUTOMATIZADOR MERCATO INICIADO")
        logging.info("⏰ Programado para ejecutar cada 12 horas")
        
        # Programar actualización cada 12 horas
        schedule.every(12).hours.do(self.run_update)
        
        # Ejecutar una vez al inicio (opcional)
        logging.info("🏃 Ejecutando actualización inicial...")
        self.run_update()
        
        # Bucle principal
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar cada minuto
                
                # Mostrar estado cada hora
                if datetime.now().minute == 0:
                    self.show_status()
                    
        except KeyboardInterrupt:
            logging.info("⏹️  Automatizador detenido por el usuario")
        except Exception as e:
            logging.error(f"💥 Error en automatizador: {e}")

def main():
    """Función principal"""
    automation = MercatoAutomation()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'status':
            automation.show_status()
            return
        elif sys.argv[1] == 'run':
            automation.run_update()
            return
        elif sys.argv[1] == 'test':
            # Modo test: ejecutar una vez y salir
            success = automation.run_update()
            sys.exit(0 if success else 1)
    
    # Modo normal: ejecutar programador
    automation.run_scheduler()

if __name__ == "__main__":
    main()
