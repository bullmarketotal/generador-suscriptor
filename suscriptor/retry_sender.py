import time
import requests
from buffer_manager import obtener_paquetes, limpiar_buffer

PING_URL = "http://localhost:8000/ping"

def esta_backend_disponible(url=PING_URL) -> bool:
    """Verifica si el backend está disponible"""
    print("SUSCRIPTOR 1 ENTRE A VERIFICAR")
    try:
        response = requests.get(url, timeout=2)
        print("SUSCRIPTOR 1 STATUS CODE",response.status_code)
        return response.status_code == 200
    except requests.RequestException:
        print("SUSCRIPTOR 1 FALSE PAPITO")
        return False

def reintentar_envio_buffer(should_exit_flag, endpoint=""):
    """
    Reintentar enviar los paquetes del buffer si el backend esta disponible juajujuaaa
    """
    while not should_exit_flag():
        if esta_backend_disponible():
            paquetes = obtener_paquetes()
            exito = True
            for paquete in paquetes:
                print(f"📤 SUSCRIPTOR 1 Reintentando enviar paquete: {paquete}")
                try:
                    response = requests.post(endpoint, data=paquete)
                    print(f"📤 SUSCRIPTOR 1 PAQUETE REENVIADO CON EXITO: {paquete}")
                    response.raise_for_status()
                except requests.RequestException as e:
                    print(f"❌ SUSCRIPTOR 1 Error reenviando paquete: {e}")
                    print(f"SUSCRIPTOR 1 PAKETE Q FALLO: {paquete}")
                    exito = False
                    break
            if exito:
                print("✅ SUSCRIPTOR 1 Todos los paquetes reenviados con éxito.")
                limpiar_buffer()
        else:
            print("⚠️ SUSCRIPTOR 1 Backend no disponible. Esperando para reintentar...")

        time.sleep(10)  
