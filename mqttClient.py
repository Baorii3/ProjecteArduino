import os
import paho.mqtt.client as mqtt
import json
from db import execute_query

# Configuración
root_ca = os.path.join("D:\\Descargas", "AmazonRootCA1.pem")
cert_file = os.path.join("D:\\Descargas", "442a5096eea39dd4c2f8f49f020eef28afcf235d407510a60c6f06e28170469c-certificate.pem.crt")
key_file = os.path.join("D:\\Descargas", "442a5096eea39dd4c2f8f49f020eef28afcf235d407510a60c6f06e28170469c-private.pem.key")

client_id = "server_espnode01"
subscribe_topic = "iticbcn/espnode01/sub"
publish_topic = "iticbcn/espnode01/pub"

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al MQTT")
        mqtt_client.subscribe(subscribe_topic)
    else:
        print(f"Error de conexión al MQTT, código: {rc}")

# Publicar mensaje
def publish_message(client, message):
    message = json.dumps(message)
    client.publish(publish_topic, message)

# Callback cuando llega un mensaje
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        data = json.loads(message)  # convierte JSON string a dict
        print(f"Mensaje recibido en {msg.topic}: {data}")

        # Usar el campo 'tagID' para la consulta
        if "tagID" in data:
            coditarjeta = data["tagID"]
            num = execute_query(coditarjeta, client)
            if num == 1:
                publish_message(client, {"status": "True"})
            elif num == 0:
                publish_message(client, {"status": "registered"})
            else:
                publish_message(client, {"status": "False"})
        else:
            print("Campo 'tagID' no encontrado en el mensaje")
    except json.JSONDecodeError:
        print(f"Error: mensaje no es JSON válido: {msg.payload}")

def create_mqtt_client():
    mqtt_client = mqtt.Client(client_id=client_id)
    mqtt_client.tls_set(ca_certs=root_ca, certfile=cert_file, keyfile=key_file)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("a37i1kunen917o-ats.iot.us-east-1.amazonaws.com", 8883)
    return mqtt_client