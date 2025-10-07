from manejador_usuario import ManejadorUsuarios
from usuario import Usuario


class ControladorUsuarios:
    def __init__(self):
        self.manejador = ManejadorUsuarios.get_instance()

    def alta_usuario(self, nickname, email, contrasena, nombre):
        usuario = Usuario(nickname, contrasena, nombre, email)
        if not self.manejador.add_usuario(usuario):
            raise ValueError("El nickname ya existe")
        return usuario

    def get_usuario(self, nickname):
        return self.manejador.get_usuario_por_nickname(nickname)

    def listar_usuarios(self):
        return self.manejador.get_usuarios()

    def eliminar_usuario(self, nickname):
        self.manejador.eliminar_usuario(nickname)
        return True