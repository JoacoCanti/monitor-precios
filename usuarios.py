class Usuario:
    def __init__(self, nickname:str,contrasena:str,nombre:str,email:str):
        self._nickname = nickname
        self._contrasena = contrasena 
        self._nombre = nombre
        self._email = email

#getters
    @property
    def nickname(self):
        return self._nickname
    
    @property
    def contrasena(self):
        return self._contrasena
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    
#setters
    @nickname.setter
    def nickname(self,nick:str):
        self._nickname = nick
        
    @contrasena.setter
    def contrasena(self,contra:str):
        self._contrasena = contra
        
    @nombre.setter
    def nombre(self,nom:str):
        self._nombre = nom
        
    @email.setter
    def email(self,mail:str):
        self._email = mail
    
 