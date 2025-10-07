from producto import Producto
from database import Database
from usuarios import Usuario
class ManejadorProductos:
    _instance = None

    def __init__(self):
        if ManejadorProductos._instance is not None:
            raise Exception("Singleton ya existe")
        self.db = Database.get_instance()
        ManejadorProductos._instance = self

    @staticmethod
    def get_instance():
        if ManejadorProductos._instance is None:
            ManejadorProductos()
        return ManejadorProductos._instance

    def add_producto(self, producto: Producto):
        try:
            self.db.cursor.execute(
                "INSERT INTO productos (nombre, url, precio) VALUES (?, ?, ?)",
                (producto.nombre, producto.url, producto.precio_objetivo)
            ) 
            self.db.conn.commit()
            return True
        except:
            return False

    def eliminar_producto(self, nombre):
        try:
            self.db.cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
            if not self.db.cursor.fetchone():
             print(f" El producto '{nombre}' no existe.")
             return
            else:
             self.cursor.execute("DELETE FROM suscripciones WHERE producto = ?", (nombre,))
             self.db.cursor.execute("DELETE FROM productos WHERE nombre=?", (nombre,))
             self.db.conn.commit()
        except Exception as e:
            print (f"[Error] No se pudo eliminar el producto {nombre} : {e} ")
                

    def get_productos(self):
        self.db.cursor.execute("SELECT nombre, url, precio FROM productos")
        rows = self.db.cursor.fetchall()
        return [Producto(*row) for row in rows]

    def get_producto_por_nombre(self, nombre):
        self.db.cursor.execute("SELECT nombre, url, precio,alerta_enviada FROM productos WHERE nombre=?", (nombre,))
        row = self.db.cursor.fetchone()
        if row:
          producto = Producto(row[0], row[1], row[2])
          producto.alerta_enviada = bool(row[3])  # convertir a booleano para simplificar su uso 
          return producto
        return None
        
    
    
    
    def agregar_observador(self, nickname, nombre_producto):
        
     try:
        # Obtener ID de usuario
        self.db.cursor.execute("SELECT id FROM usuarios WHERE nickname=?", (nickname,))
        row = self.db.cursor.fetchone()
        if not row:
            print(f"Usuario {nickname} no encontrado")
            return False
        uid = row[0]

        # Obtener ID de producto
        self.db.cursor.execute("SELECT id FROM productos WHERE nombre=?", (nombre_producto,))
        row = self.db.cursor.fetchone()
        if not row:
            print(f"Producto {nombre_producto} no encontrado")
            return False
        pid = row[0]

        # Insertar observador
        self.db.cursor.execute(
            "INSERT OR IGNORE INTO observadores (usuario_id, producto_id) VALUES (?, ?)",
            (uid, pid)
        )
        self.db.conn.commit()
        print(f" {nickname} ahora observa {nombre_producto}")
        return True
     except Exception as e:
        print(f"ERROR agregar_observador: {e}")
        return False  
        
        
   
    def eliminar_observador(self, usuario_id, producto_id):
     self.db.cursor.execute(
        "DELETE FROM observadores WHERE usuario_id=? AND producto_id=?",
        (usuario_id, producto_id)
     )
     self.db.conn.commit()
     
     
    def get_observadores_por_producto(self, nombre_producto):
        
     try:
        query = """
            SELECT u.nickname, u.contrasena, u.nombre, u.email
            FROM usuarios u
            JOIN observadores o ON u.id = o.usuario_id
            JOIN productos p ON p.id = o.producto_id
            WHERE p.nombre = ?
        """
        self.db.cursor.execute(query, (nombre_producto,))
        rows = self.db.cursor.fetchall()
       
        return [Usuario(*row) for row in rows]
     except Exception as e:
        print(f"ERROR get_observadores_por_producto: {e}")
        return [] 
        
    
    def marcar_alerta_no_enviada(self, nombre_producto):
     self.db.cursor.execute(
        "UPDATE productos SET alerta_enviada = 0 WHERE nombre = ?",
        (nombre_producto,)
     )
     self.db.conn.commit()    
        
    
    
    def marcar_alerta_enviada(self, nombre_producto):
     self.db.cursor.execute(
        "UPDATE productos SET alerta_enviada = 1 WHERE nombre = ?",
        (nombre_producto,)
     )
     self.db.conn.commit()

    def alerta_ya_enviada(self, nombre_producto):
     self.db.cursor.execute(
        "SELECT alerta_enviada FROM productos WHERE nombre = ?",
        (nombre_producto,)
     )
     row = self.db.cursor.fetchone()
     return row[0] == 1 if row else False
    
    
    def _get_usuario_obj(self, nickname):
     self.db.cursor.execute("SELECT nickname, contrasena, nombre, email FROM usuarios WHERE nickname=?", (nickname,))
     row = self.db.cursor.fetchone()
     return Usuario(*row) if row else None