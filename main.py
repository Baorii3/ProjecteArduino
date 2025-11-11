import os
import threading
import mysql.connector
from mysql.connector import Error
import time
import paho.mqtt.client as mqtt
import json

# Configuración
root_ca = os.path.join("D:\\Descargas", "AmazonRootCA1.pem")
cert_file = os.path.join("D:\\Descargas", "442a5096eea39dd4c2f8f49f020eef28afcf235d407510a60c6f06e28170469c-certificate.pem.crt")
key_file = os.path.join("D:\\Descargas", "442a5096eea39dd4c2f8f49f020eef28afcf235d407510a60c6f06e28170469c-private.pem.key")

client_id = "server_espnode01"
subscribe_topic = "iticbcn/espnode01/sub"
publish_topic = "iticbcn/espnode01/pub"

# DB
DB_CONFIG = {
    "host": "52.91.92.223",
    "user": "server",
    "password": "pirineus",
    "database": "Control",
    "port": 3306,
    "use_pure": True
}

# Crear conexión a DB
def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a la DB: {e}")
        return None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al MQTT")
        mqtt_client.subscribe(subscribe_topic)
    else:
        print(f"Error de conexión al MQTT, código: {rc}")

# Publicar mensaje
def publish_message(client, message):
    message = json.dumps(message)
    client.publish(publish_topic, message)

# Ejecutar consulta en la DB
def execute_query(coditarjeta, client):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la DB")
        return
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM TARGETA WHERE TARGETA.CODI = %s"
        cursor.execute(query, (coditarjeta,))
        result = cursor.fetchone()
        if result[0] > 0:
            publish_message(client, {"status": "True"})
        else:
            publish_message(client, {"status": "False"})
        print(f"Cantidad de tarjetas amb codi {coditarjeta}: {result[0]}")
        cursor.close()
    finally:
        connection.close()

# Callback cuando llega un mensaje
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        data = json.loads(message)  # convierte JSON string a dict
        print(f"Mensaje recibido en {msg.topic}: {data}")

        # Usar el campo 'tagID' para la consulta
        if "tagID" in data:
            coditarjeta = data["tagID"]
            execute_query(coditarjeta, client)
        else:
            print("Campo 'tagID' no encontrado en el mensaje")
    except json.JSONDecodeError:
        print(f"Error: mensaje no es JSON válido: {msg.payload}")


# Configuración del cliente MQTT
mqtt_client = mqtt.Client(client_id=client_id)

mqtt_client.tls_set(ca_certs=root_ca, certfile=cert_file, keyfile=key_file)

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Conectar al broker
mqtt_client.connect("a37i1kunen917o-ats.iot.us-east-1.amazonaws.com", 8883)

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
    mqtt_client.disconnect()
