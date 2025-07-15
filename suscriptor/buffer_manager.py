import os
import json
from threading import Lock

lock = Lock()
BUFFER_FILE = "buffer_paquetes.json"

def guardar_paquete(paquete: dict):
    with lock:
        data = []
        if os.path.exists(BUFFER_FILE):
            with open(BUFFER_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        data.append(paquete)
        with open(BUFFER_FILE, "w") as f:
            json.dump(data, f)
        print(f"📦 SUSCRIPTOR 1 Paquete guardado en buffer: {paquete}")

def obtener_paquetes():
    with lock:
        if not os.path.exists(BUFFER_FILE):
            return []
        with open(BUFFER_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

def limpiar_buffer():
    with lock:
        if os.path.exists(BUFFER_FILE):
            os.remove(BUFFER_FILE)