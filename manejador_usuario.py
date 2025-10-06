from usuario import Usuario
from database import Database

class ManejadorUsuarios:
    _instance = None

    def __init__(self):
        if ManejadorUsuarios._instance is not None:
            raise Exception("Singleton ya existe")
        self.db = Database.get_instance()
        ManejadorUsuarios._instance = self

    @staticmethod
    def get_instance():
        if ManejadorUsuarios._instance is None:
            ManejadorUsuarios()
        return ManejadorUsuarios._instance

    def add_usuario(self, usuario: Usuario):
        try:
            self.db.cursor.execute(
                "INSERT INTO usuarios (nickname, contrasena, nombre, email) VALUES (?, ?, ?, ?)",
                (usuario.nickname, usuario.contrasena, usuario.nombre, usuario.email)
            )
            self.db.conn.commit()
            return True
        except:
            return False

    def eliminar_usuario(self, nickname):
       try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE nickname = ?", (nickname,))
            if not self.db.cursor.fetchone():
              print(f" El usuario '{nickname}' no existe.")
              return
            else:
             self.db.cursor.execute("DELETE FROM suscripciones WHERE usuario = ?", (nickname,))
             self.db.cursor.execute("DELETE FROM usuarios WHERE nickname=?", (nickname,))
             self.db.conn.commit()
             print (f"Usuario {nickname} eliminado correctamente.")
       except Exception as e:
           print(f"[Error] No se pudo eliminar el usuario{nickname}:{e}")    
        
        

    def get_usuarios(self):
        self.db.cursor.execute("SELECT nickname, contrasena, nombre, email FROM usuarios")
        rows = self.db.cursor.fetchall()
        return [Usuario(*row) for row in rows]

    def get_usuario_por_nickname(self, nickname):
        self.db.cursor.execute("SELECT nickname, contrasena, nombre, email FROM usuarios WHERE nickname=?", (nickname,))
        row = self.db.cursor.fetchone()
        return Usuario(*row) if row else None