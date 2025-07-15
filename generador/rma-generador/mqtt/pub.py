# mqtt/pub.py
import sys
import time
import random
import threading
import paho.mqtt.client as paho
from typing import Optional, List  # Importar List para manejar lista de tipos
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel
from mqtt import TipoMensaje
from mqtt.config import config

class Mensaje(BaseModel):
    id: int
    type: int
    data: str
    time: int

@dataclass
class Nodo:
    id: int
    stop_event: threading.Event
    cliente: paho.Client = paho.Client()
    tipos_de_mensaje: List[TipoMensaje] = None  # Agregar lista de tipos de mensajes
    frecuencia: int = 120  # Cambiar la frecuencia por defecto a 30 segundos
    mensajes_enviados: int = 0

    def __post_init__(self) -> None:
        self.setear_manejadores_de_eventos()

    def setear_manejadores_de_eventos(self) -> None:

        def on_connect(_, obj, flags, reason_code) -> None:
            if self.cliente.is_connected():
                print("Publicador conectado!")

        self.cliente.enable_logger()
        self.cliente.on_connect = on_connect

    def publicar(
        self,
        topic: str,
        qos: int = 1,
    ) -> None:
        if not self.cliente.is_connected():
            self.conectar()

        while not self.stop_event.is_set():
            for tipo in self.tipos_de_mensaje:
                # Generar el mensaje dependiendo del tipo
                message = self.generar_valor(tipo)

                mensaje = self.formatear_mensaje(
                    topic,
                    tipo,
                    message,
                )

                res = self.cliente.publish(
                    topic,
                    mensaje,
                    qos,
                )

                try:
                    res.wait_for_publish()
                    if res.is_published():
                        self.cliente.logger.warn(f"{res.mid} - {mensaje}")
                        self.mensajes_enviados += 1
                    else:
                        print(f"El mensaje n° {res.mid} no fue publicado.")
                except RuntimeError as re:
                    print(f"El cliente se ha desconectado con el mensaje: {res.rc}.")
                    break

                time.sleep(self.frecuencia / len(self.tipos_de_mensaje))  # Ajustar la frecuencia para distribuirla entre los tipos de mensajes

        self.cliente.loop_stop()
        self.desconectar()

    def conectar(self) -> None:
        if self.cliente.connect(config.host, config.port, config.keepalive) != 0:
            print("Ha ocurrido un error al conectar al broker MQTT")
        print("Conectado al broker MQTT!")
        self.cliente.loop_start()

    def desconectar(self):
        self.cliente.disconnect()
        print(f"Desconectado! - mensajes enviados: {self.mensajes_enviados}")
        sys.exit(0)

    def formatear_mensaje(self, topic: str, tipo: TipoMensaje, mensaje: str) -> str:
        mensaje = Mensaje(
            id=self.id, 
            type=int(tipo), 
            data=mensaje, 
            time=int(datetime.now().timestamp()) 
        ).model_dump()
        return str(mensaje)

    def generar_valor(self, tipo: TipoMensaje) -> str:
        """Genera un valor aleatorio según el tipo de mensaje."""
        if tipo == TipoMensaje.TEMP_T:
            # Genera un valor de temperatura entre -30 y 60°C
            return str(random.uniform(-30.0, 60.0))
        elif tipo == TipoMensaje.HUMIDITY_T:
            # Genera un valor de humedad relativa entre 20 y 100%
            return str(random.uniform(20.0, 100.0))
        elif tipo == TipoMensaje.PRESSURE_T:
            # Genera un valor de presión atmosférica entre 500 y 1050 hPa
            return str(random.uniform(500.0, 1050.0))
        elif tipo == TipoMensaje.WINDSPD_T:
            # Genera un valor de velocidad de viento entre 0 y 100 km/h
            return str(random.uniform(0.0, 160.0))
        elif tipo == TipoMensaje.VOLTAGE_T:
            # Genera un valor entre 10.5V y 13.5V
            return str(random.uniform(10.0, 13.5))
        elif tipo == TipoMensaje.RAINFALL_T:
            return str(random.uniform(0.0, 170.0))
        elif tipo == TipoMensaje.LEVEL_T:
            return str(random.uniform(0.0, 250))
        else:
            # Por defecto, devuelve un número aleatorio
            return str(random.uniform(0.0, 100.0))