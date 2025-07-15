# main.py
import sys
import argparse
import threading
import signal
import random
import time
import paho.mqtt.client as paho
from mqtt import TipoMensaje  # Importar TipoMensaje
from mqtt.pub import Nodo
from mqtt.config import config

def signal_handler(sig, frame):
    print("Deteniendo nodos...")
    stop_event.set()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--nodos",
        type=int,
        default=4,
        help="Cantidad de nodos para la cual generar datos. (default=1)",
    )
    parser.add_argument(
        "-t",
        "--tipos",
        type=str,
        nargs='+',
        default=['TEMP_T', 'VOLTAGE_T', 'LEVEL_T'],  # Tipos de mensaje por defecto
        help="Lista de tipos de mensaje que cada nodo va a publicar. Ej: TEMP_T HUMIDITY_T PRESSURE_T",
    )

    stop_event = threading.Event()
    signal.signal(signal.SIGINT, signal_handler)
    
    args = parser.parse_args()
    
    # Convertir los nombres de los tipos de mensaje en objetos TipoMensaje
    tipos_de_mensaje = [TipoMensaje[tip] for tip in args.tipos]  # Convierte los strings en TipoMensaje

    # Crear nodos
    lista_nodos = [
        Nodo(i, tipos_de_mensaje=tipos_de_mensaje, frecuencia=random.randint(20, 30), stop_event=stop_event)
        for i in range(1,args.nodos)
    ]
    print(f"{len(lista_nodos)} nodo/s creado/s. Publicando...")

    for nodo in lista_nodos:
        thread = threading.Thread(
            target=nodo.publicar,
            args=(config.topic,),
        )
        thread.start()
        time.sleep(random.randint(60, 120))