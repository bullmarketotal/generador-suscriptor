import sys
import threading
import time
from typing import Callable, Optional
import requests  
import paho.mqtt.client as paho


from retry_sender import reintentar_envio_buffer
from buffer_manager import guardar_paquete
from config import config

API_URL = "http://localhost:8000/suscriptor"  


class Subscriptor:
    def __init__(self, client: paho.Client) -> None:
        self.client = client
        self.message_counter = 0
        self.should_exit = False
        self.thread = None
        self.subscribed = False

        self.set_event_handlers()

    def set_event_handlers(self) -> None:
        def on_subscribe(_, userdata, mid, granted_qos) -> None:
            if not self.subscribed:
                print(f"✅SUSCRIPTOR 1 Suscrito a {config.topic}!")
                self.subscribed = True

        def on_message(_, userdata, msg) -> None:
            message = msg.payload.decode()
            self.message_counter += 1
            print(f" [{self.message_counter}] Mensaje recibido en SUS1: {message}")
            self.enviar_a_api(message)

        def on_connect(_, obj, flags, reason_code) -> None:
            if self.client.is_connected():
                print(" SUSCRIPTOR 1 conectado al broker!")
                if not self.subscribed:
                    self.subscribe(config.topic, 1)

        def on_disconnect(_, userdata, rc) -> None:
            print(f" Total mensajes recibidos por el SUS1: {self.message_counter}")
            print(" SUSCRIPTOR 1 Desconectado del broker.")
            self.should_exit = True

        self.client.on_connect = on_connect
        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

    def enviar_a_api(self, mensaje: str) -> None:
        try:
            response = requests.post(API_URL, data=mensaje)
            if response.status_code == 200:
                print(" Mensaje ENVIADO a la API correctamente desde SUS 1.")
            else:
                print(f" Error al enviar mensaje a API desde SUS 1. Status: {response.status_code}")
                guardar_paquete(mensaje)
        except Exception as e:
            print(f" Excepción al enviar mensaje a la API desde SUS 1: {e}")
            guardar_paquete(mensaje)

    def subscribe(self, topic: str, qos: int) -> None:
        self.client.subscribe(topic=topic, qos=qos)

    def connect(self, host: str, port: int, keepalive: int) -> None:
        try:
            self.client.connect(host, port, keepalive)
            print(" SUS 1 Conectando al broker...")
            self.thread = threading.Thread(target=self.run_loop, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f" Error al conectar con el broker MQTT desde SUS 1: {e}")
            sys.exit(1)

    def run_loop(self) -> None:
        while not self.should_exit:
            self.client.loop()

    def disconnect(self):
        self.client.disconnect()
        self.should_exit = True
        if self.thread and self.thread.is_alive():
            self.thread.join()


# --- Ejecución del subscriptor ---
if __name__ == "__main__":
    client = paho.Client()
    subscriptor = Subscriptor(client)
    subscriptor.connect(config.host, config.port, config.keepalive)

    buffer_thread = threading.Thread(
    target=reintentar_envio_buffer,
    args=(lambda: subscriptor.should_exit, "http://localhost:8000/suscriptor"),
    daemon=True
    )
    buffer_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Finalizando...")
        subscriptor.disconnect()
