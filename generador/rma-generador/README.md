# rma-generador
Generador de datos sintéticos para Red de Monitoreo Ambiental

### Cómo ejecutar:
0. Renombrar .env.template a .env
1. Crear un entorno virtual con [venv](https://docs.python.org/3/library/venv.html): `python -m venv ~/Envs/rma-generador`. La carpeta `Envs` debiera existir mientras que `rma-generador` será creada por venv.
2. Activar el entorno virtual, ver cómo activarlo según nuestro SO en la [tabla](https://docs.python.org/3/library/venv.html#how-venvs-work). 
3. Instalar las dependencias con: `pip install -r requirements.txt` .
4. En una terminal ejecutar el script `main.py`: `python main.py`
5. En otra terminal, ejecutar el suscriptor `sub.py`: `python mqtt/sub.py`, si estamos en la carpeta raíz del proyecto. 

**Observaciones:**
Para que el proyecto funcione se necesita tener `mosquitto` instalado en el sistema. Se puede descargar desde el siguiente enlace: [https://mosquitto.org/download/](https://mosquitto.org/download/). 
Una vez instalado, verificar que el servicio de mosquitto ha iniciado. Caso contrario, iniciar manualmente.
La conexión por defecto se hará en `localhost:1883` con el topic `test_topic` tal como lo indica el archivo `.env`.
Iniciar el publicador antes que el suscriptor puede ocasionar la pérdida de mensajes por parte del suscriptor.

#### Múltiples publicadores en simultáneo:

Para simular el funcionamiento de múltiples nodos publicando al mismo tiempo, ejecutar `python main.py -n <cant_nodos>` (default=1).


#### Personalizar comportamiento ante la llegada de un mensaje:

Al instanciar un suscriptor es posible asignarle una función callback que implementa comportamiento personalizado. La función callback recibirá el mensaje por parámetros. Por ejemplo:

```python
#...
from mqtt.config import config
from mqtt.sub import Subscriptor

def mi_callback(mensaje: str) -> None:
    print(f"he recibido: {mensaje}")

#...
sub = Subscriptor(client=paho.Client(), on_message_callback=mi_callback)
sub.connect(config.host, config.port, config.keepalive)

```
