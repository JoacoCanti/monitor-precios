#  Sistema de Monitoreo de Precios

Este proyecto permite a los usuarios registrar **productos** y recibir **alertas por correo electrónico** cuando los precios bajan, usando **Python**, **SQLite** y el patrón **Observer**.

---

##  Características

- Registro de **usuarios** y **productos**.
- Suscripción de usuarios a productos para recibir alertas.
- Monitoreo automático diario de precios.
- Notificación por correo electrónico mediante `smtplib` y la clase `AutomatizadorEmails`.
- Persistencia de datos en **SQLite** (`database.db`).
- Menú interactivo simple y limpio.

---

##  Requisitos

- Python 3.8 o superior  
- Librerías externas:
  - `requests`
  - `beautifulsoup4`

Instalación:

```bash
pip install requests beautifulsoup4 
