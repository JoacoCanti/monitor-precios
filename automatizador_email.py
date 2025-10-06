import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AutomatizadorEmails:
    _instance = None  # atributo de clase para el singleton

    @staticmethod
    def get_instance(email=None, contrasena=None):
        if AutomatizadorEmails._instance is None:
            if email is None or contrasena is None:
                raise ValueError("Primera vez debes pasar email y contraseña")
            AutomatizadorEmails._instance = AutomatizadorEmails(email, contrasena)
        return AutomatizadorEmails._instance
    
    def __init__(self, email, contrasena):
        if AutomatizadorEmails._instance is not None:
            raise Exception("Esta clase es un singleton, usá get_instance()")
        self.email = email                #email del administrador
        self.contrasena = contrasena      #app password de email administrador 
        self.server = None
    
    
    
    
    def conectar_servidor(self):
        try:
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.email, self.contrasena)
            print("Conectado al servidor SMTP")
        except Exception as e:
            print(f"Error al conectar: {e}")



    def enviar_alerta(self, usuario, producto, precio_actual):
     if not self.server:
        raise RuntimeError("Servidor SMTP no conectado. Llamar a conectar_servidor() primero.")
     try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = usuario.email
            msg['Subject'] = f"¡Oferta! {producto.nombre} bajó de precio"

            contenido = f"""
            <html>
            <body>
                <h2>Hola {usuario.nickname}</h2>
                <p>Tu producto <b>{producto.nombre}</b> está a <b>${precio_actual}</b>.</p>
                <p>Podés verlo acá: <a href="{producto.url}">{producto.url}</a></p>
            </body>
            </html>
            """
            msg.attach(MIMEText(contenido, 'html','utf-8'))
            self.server.send_message(msg)
        
     except Exception as e:
            print(f"Error enviando mail a {usuario.email}: {e}")

    def cerrar_conexion(self):
        if self.server:
            self.server.quit()