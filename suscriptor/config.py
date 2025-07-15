import os, json
from collections import namedtuple

from dotenv import load_dotenv

load_dotenv()

Config = namedtuple("Config", ["topic", "host", "port", "keepalive"])
config = Config(
    topic=os.getenv("MQTT_TOPIC"),
    host=os.getenv("MQTT_HOST"),
    port=int(os.getenv("MQTT_PORT")),
    keepalive=int(os.getenv("MQTT_KEEPALIVE")),
)



# Umbrales de alerta y validez
CONFIG = {}


def get_config_alertas():
    global CONFIG
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    if os.path.exists(ruta):
        with open(ruta, "r") as archivo:
            CONFIG = json.load(archivo)
            return CONFIG
    else:
        print("Advertencia: config.json no encontrado.")
