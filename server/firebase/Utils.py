import firebase_admin
from firebase_admin import credentials, messaging
import os

# Ruta absoluta al archivo de credenciales
ruta_credenciales = os.path.join(os.path.dirname(__file__), "credenciales.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(ruta_credenciales)
    firebase_admin.initialize_app(cred)

def enviar_notificacion_fcm(token, titulo, mensaje):
    try:
        mensaje_envio = messaging.Message(
            notification=messaging.Notification(
                title=titulo,
                body=mensaje
            ),
            token=token,
        )
        respuesta = messaging.send(mensaje_envio)
        return {"success": True, "response": respuesta}
    except Exception as e:
        return {"success": False, "error": str(e)}
