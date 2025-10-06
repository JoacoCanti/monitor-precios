from abc import ABC, abstractmethod

class IUsuario(ABC):

    @abstractmethod
    def listar_usuarios(self):
        pass

    @abstractmethod
    def get_usuario(self, nickname):
        pass

    @abstractmethod
    def alta_usuario(self, nickname, email, contrasena, nombre):
        pass

    @abstractmethod
    def eliminar_usuario(self, nickname):
        pass







