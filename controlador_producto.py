from manejador_producto import ManejadorProductos
from producto import Producto
from automatizador_email import AutomatizadorEmails

class ControladorProductos:
    def __init__(self, IUsuario):
        self.IUsuario = IUsuario
        self.manejador = ManejadorProductos.get_instance()

    def alta_producto(self, nombre, url, precio):
        producto = Producto(nombre, url, precio)
        if not self.manejador.add_producto(producto):
            raise ValueError("El producto ya existe")
        return producto

    def get_producto(self, nombre):
        return self.manejador.get_producto_por_nombre(nombre)

    def listar_productos(self):
        return self.manejador.get_productos()

    def eliminar_producto(self, nombre):
        self.manejador.eliminar_producto(nombre)
        return True

    def notificar(self, precio_actual, producto):
        if self.manejador.alerta_ya_enviada(producto.nombre):
            return  
        usuarios = self.manejador.get_observadores_por_producto(producto.nombre)
        automatizador = AutomatizadorEmails.get_instance()
        print(f"notificando {producto.nombre} a {len(usuarios)} usuarios")
        for usuario in usuarios:
            automatizador.enviar_alerta(usuario, producto, precio_actual)
        self.manejador.marcar_alerta_enviada(producto.nombre)

    def agregar_observador(self, nickname, nombre_producto):
     agregado = self.manejador.agregar_observador(nickname, nombre_producto)
     if agregado:
        producto = self.get_producto(nombre_producto)
        if producto:
            from monitor_precios import MonitorPrecios
            monitor = MonitorPrecios(producto, self)  # pasamos self como controlador
            precio_actual = monitor.obtener_precio()
            if precio_actual is not None and precio_actual <= producto.precio_objetivo:
                print(f"[ALERTA INMEDIATA] {producto.nombre} bajó a ${precio_actual}")
                self.notificar(precio_actual, producto)
     return agregado



