import requests
from bs4 import BeautifulSoup
from producto import Producto

class MonitorPrecios:
    def __init__(self, producto,controlador_productos,):
        self.producto = producto
        self.controlador_productos = controlador_productos

    def obtener_precio(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(self.producto.url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
 
             #Encuentra el bloque principal del precio.
            precio_div = soup.find('div', class_='ui-pdp-price__second-line')
            if not precio_div:
                print(f"No se encontró el precio para {self.producto.nombre}")
                return None

             #Dentro de ese div, busca el span específico que contiene el número.
            precio_elemento = precio_div.find('span', class_='andes-money-amount__fraction')
            if not precio_elemento:
                print(f"No se encontró el precio para {self.producto.nombre}")
                return None

            precio_texto = precio_elemento.text.strip()
            precio = float(precio_texto.replace('.', ''))
            return precio

        except Exception as e:
            print(f"Error obteniendo precio: {e}")
            return None




    def revisar_precio(self):
       precio_actual = self.obtener_precio()
       if precio_actual is not None and precio_actual <= self.producto.precio_objetivo:
            print(f"[ALERTA] {self.producto.nombre} bajó a ${precio_actual}")
            self.controlador_productos.notificar(precio_actual, self.producto)
       return precio_actual