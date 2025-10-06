from abc import ABC, abstractmethod

class IProducto(ABC):

    @abstractmethod
    def alta_producto(self, nombre, url, precio):
        pass

    @abstractmethod
    def get_producto(self, nombre):
        pass

    @abstractmethod
    def listar_productos(self):
        pass

    @abstractmethod
    def eliminar_producto(self, nombre):
        pass


    @abstractmethod
    def notificar(self, precio_actual,producto):
        pass

    @abstractmethod
    def agregar_observador(self, nickname, nombre_producto): 
       pass
