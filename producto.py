class Producto:
    def __init__(self, nombre, url,precio_objetivo):
        self.nombre = nombre
        self.url = url
        self.precio_objetivo = precio_objetivo
       
 
# getters
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def url(self):
        return self._url
    
    @property
    def precio_objetivo(self):
        return self._precio_objetivo
    
  
    
# setters
    @nombre.setter
    def nombre(self,nom:str):
        self._nombre = nom
        
    @url.setter
    def url(self,u:str):
        self._url = u
        
    @precio_objetivo.setter
    def precio_objetivo(self,p:str):
        self._precio_objetivo = p
    