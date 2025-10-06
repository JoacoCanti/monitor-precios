from manejador_producto import ManejadorProductos
from producto import Producto

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

  






