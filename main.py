from Iusuario import IUsuario
from Iproducto import IProducto
from factory import Factory
from automatizador_emails import AutomatizadorEmails
from monitor_global_module import MonitorGlobalCombinado  
import threading
from queue import Queue

def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Crear usuario")
    print("2. Listar usuarios")
    print("3. Crear producto")
    print("4. Listar productos")
    print("5. Suscribirse a producto")
    print("6. Eliminar usuario")
    print("7. Eliminar producto")
    print("8. Salir")

def ejecutar_opcion(opcion, IUsuario, IProducto):
    if opcion == "1":
        nickname = input("Nickname: ")
        nombre = input("Nombre: ")
        email = input("Email: ")
        contrasena = input("Contraseña: ")
        try:
            IUsuario.alta_usuario(nickname, email, contrasena, nombre)
            print("Usuario creado con éxito")
        except ValueError as e:
            print(e)

    elif opcion == "2":
        usuarios = IUsuario.listar_usuarios()
        print("Usuarios registrados:")
        for u in usuarios:
            print(f"- {u.nickname} ({u.email})\n")

    elif opcion == "3":
        nombre = input("Nombre del producto: ")
        url = input("URL del producto: ")
        precio_objetivo = float(input("Precio objetivo: "))
        try:
            IProducto.alta_producto(nombre, url, precio_objetivo)
            print("Producto creado con éxito")
        except ValueError as e:
            print(e)

    elif opcion == "4":
        productos = IProducto.listar_productos()
        print("Productos registrados:")
        for p in productos:
            print(f"- {p.nombre} precio objetivo ${p.precio_objetivo} | url {p.url}\n")

    elif opcion == "5":
        nickname = input("Tu nickname: ")
        nombre_producto = input("Nombre del producto a suscribirse: ")

        usuario = IUsuario.get_usuario(nickname)
        producto = IProducto.get_producto(nombre_producto)

        if usuario and producto:
            IProducto.agregar_observador(nickname, nombre_producto)
            print(f"{usuario.nickname} ahora está suscrito a {producto.nombre}")
        else:
            print("Usuario o producto no encontrado")

    elif opcion == "6":
        nickname = input("Nickname del usuario a eliminar: ")
        IUsuario.eliminar_usuario(nickname)

    elif opcion == "7":
        nombre = input("Nombre del producto a eliminar: ")
        IProducto.eliminar_producto(nombre)

    elif opcion == "8":
        print("Saliendo...")
        return False

    else:
        print("Opción inválida")

    return True

def main():
    try:
        # Inicializar el automatizador de mails
        automatizador = AutomatizadorEmails.get_instance(
            email="tu_email.com",#email admin (emial de envio)
            contrasena="tu_app_password_del_email"  #app password de email admin 
        )
        automatizador.conectar_servidor()
        print("Conectado al servidor SMTP")
    except Exception as e:
        print(f"No se pudo inicializar el sistema de correos: {e}")

    # Inicializar controladores
    IUsuario = Factory.get_controlador_usuarios()
    IProducto = Factory.get_controlador_producto()

    # Revisar precios inmediatamente y enviar mails
    monitor = MonitorGlobalCombinado(IProducto)
    print("Revisión inmediata de precios y envío de mails correspondientes...")
    monitor.revisar_todos(forzar_envio=True)

    # Iniciar monitoreo diario en un hilo separado
    hilo_monitor = threading.Thread(target=monitor.iniciar_monitoreo_diario, daemon=True)
    hilo_monitor.start()

    # Menú principal
    seguir = True
    while seguir:
        while not monitor.cola_alertas.empty():
         mensaje=monitor.cola_alertas.get()
         print(mensaje)
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        seguir = ejecutar_opcion(opcion, IUsuario, IProducto)

if __name__ == "__main__":
    main()
    
    