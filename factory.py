
from controlador_usuario import ControladorUsuarios
from controlador_producto import ControladorProductos

_controlador_usuarios = None
_controlador_productos = None

class Factory:
    @staticmethod
    def get_controlador_usuarios():
        global _controlador_usuarios
        if _controlador_usuarios is None:
            _controlador_usuarios = ControladorUsuarios()
        return _controlador_usuarios

    @staticmethod
    def get_controlador_producto():
        global _controlador_productos
        if _controlador_productos is None:
            # Obtener el controlador de usuarios primero
            IUsuario = Factory.get_controlador_usuarios()
            _controlador_productos = ControladorProductos(IUsuario)
        return _controlador_productos
