from monitor_precios import MonitorPrecios
from automatizador_emails import AutomatizadorEmails
from manejador_producto import ManejadorProductos
from datetime import datetime
import time
from queue import Queue

class MonitorGlobalCombinado:
    def __init__(self,  controlador_productos, intervalo=60):
        self.manejador = ManejadorProductos.get_instance()
        self.controlador_productos = controlador_productos
        self.automatizador = AutomatizadorEmails.get_instance()
        self.intervalo = intervalo
        self.cola_alertas = Queue()

    def revisar_todos(self, forzar_envio=False): # el forzar envio es para hacer algunas pruebas
     productos = self.manejador.get_productos()
     for producto in productos:
        monitor = MonitorPrecios(producto, self.controlador_productos)          
        precio_actual = monitor.obtener_precio()

        if precio_actual is None:
            continue  # no hay precio, seguimos con el próximo

        # Si subió, reseteamos alerta
        if precio_actual > producto.precio_objetivo:
            self.manejador.marcar_alerta_no_enviada(producto.nombre)

        # Si bajó y aún no se envió (o estamos forzando)
        elif (not self.manejador.alerta_ya_enviada(producto.nombre)) or forzar_envio:
            usuarios = self.manejador.get_observadores_por_producto(producto.nombre)
            if not forzar_envio:
             self.manejador.marcar_alerta_enviada(producto.nombre)
            
            
            for usuario in usuarios:
                mensaje=f"\n[ALERTA] Enviando mail a {usuario.email} por {producto.nombre} (${precio_actual})"
               
                self.cola_alertas.put(mensaje)
                self.automatizador.enviar_alerta(usuario, producto, precio_actual)

            # Marcamos que ya se mandó
            if forzar_envio:
             self.manejador.marcar_alerta_enviada(producto.nombre)



    def iniciar_monitoreo_diario(self):
     print(f"Iniciando monitoreo diario de precios a las 09:00...")
     while True:
        ahora = datetime.now().strftime("%H:%M")
        if ahora == "9:00":  
            self.revisar_todos(forzar_envio=True)
            time.sleep(60)  # esperamos un minuto para no disparar varias veces en el mismo minuto
        time.sleep(10)  # chequea cada segundo

