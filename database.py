import sqlite3

class Database:
    _instance = None

    def __init__(self, db_name="database.db"):
        if Database._instance is not None:
            raise Exception("Singleton ya existe")
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        Database._instance = self
        self.crear_tablas()

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database()
        return Database._instance

    def crear_tablas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nombre TEXT UNIQUE NOT NULL,
           url TEXT NOT NULL,
           precio REAL NOT NULL,
           alerta_enviada INTEGER DEFAULT 0  -- nota: 0 = no enviada, 1 = enviada
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS observadores (
            usuario_id INTEGER,
            producto_id INTEGER,
            PRIMARY KEY (usuario_id, producto_id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
        """)
        self.conn.commit()