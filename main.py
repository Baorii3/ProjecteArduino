from mqttClient import create_mqtt_client 

mqtt_client = create_mqtt_client()


try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
    mqtt_client.disconnect()
