#include "secrets.h"
#include <WiFiClientSecure.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#define THINGNAME "espnode01"

#define AWS_IOT_SUBSCRIBE_TOPIC"iticbcn/espnode01/pub"
#define AWS_IOT_PUBLISH_TOPIC "iticbcn/espnode01/sub"
WiFiClientSecure net = WiFiClientSecure();
MQTTClient client = MQTTClient(256);

extern bool AWSConnected;

void SetupAWS(){
  Serial.begin(115200);
  //Actualitzar la variable d'estat AWSConnected
  AWSConnected = false;
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
  client.onMessage(messageReceived);
  client.begin(AWS_IOT_ENDPOINT, 8883, net);
}
void CheckAWS(){
  if (!client.connected()) {
    //Connectar-se a AWS.
    client.connect(THINGNAME);
    //Comprovar Si està connectat
    if (client.connected()) {
      Serial.println("Connected to AWS IoT");
    } else {
      Serial.print("AWS IoT Connection failed! Error code = ");
      Serial.println(client.lastError());
      AWSConnected = false;
      return;
    }
    //Actualitzar la variable d'estat AWSConnected
    AWSConnected = true;
    //Subscriure al topic
    client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
  }else{
    //Actualitzar la variable d'estat AWSConnected
    AWSConnected = true;
    client.loop();
  }
}

void messageReceived(String &topic, String &payload){
  Serial.print("Mensaje recibido en topic: ");
  Serial.println(topic);
  Serial.print("Contenido: ");
  Serial.println(payload);

  payload.replace("True", "true");
  payload.replace("False", "false");

  StaticJsonDocument<200> doc;
  // Convertir el String a JSON
  DeserializationError error = deserializeJson(doc, payload);

  if (error) {
    Serial.print("Error al parsear JSON: ");
    Serial.println(error.c_str());
    return;
  }
  if (doc.containsKey("status")) {
      bool status;
    if (doc["status"].is<bool>()) {
        status = doc["status"];
    } else if (doc["status"].is<const char*>()) {
        String s = doc["status"].as<const char*>();
        s.toLowerCase();
        status = (s == "true");
    }
    handlerStatus(status);
  }
}

void handlerStatus(bool status){
  if (status){
    accesPermitido();
  }else{
    accesDenegado();
  }
}

void accesPermitido(){
  digitalWrite(ledPinGreen,HIGH);
  digitalWrite(ledPinRed,LOW);
  delay(1000);
  digitalWrite(ledPinGreen,LOW);
}

void accesDenegado(){
  digitalWrite(ledPinGreen,LOW);
  digitalWrite(ledPinRed,HIGH);
  delay(1000);
  digitalWrite(ledPinRed,LOW);
}

void PublicaTag(String tagID){
  //un cop tenim el tag en un string el podem publicar a AWS
  // el topic pot ser quelcom com "iticbcn/node01/pub"
  if (client.connected()) {
    String payload = "{\"tagID\":\"" + tagID + "\"}";
    client.publish(AWS_IOT_PUBLISH_TOPIC, payload);
    Serial.print("Publicado: ");
    Serial.println(tagID);
  } else {
    Serial.println("No conectado a MQTT, no se pudo publicar");
  }
  delay(1000);
}
void PublicaError(String Error){
  //un cop tenim el tag en un string el podem publicar a AWS
  // el topic pot ser quelcom com "iticbcn/node01/pub"
  if (client.connected()) {
    String payload = "{\"Error\":\"" + Error + "\"}";
    client.publish(AWS_IOT_PUBLISH_TOPIC, payload);
    Serial.print("Publicado: ");
    Serial.println(Error);
  } else {
    Serial.println("No conectado a MQTT, no se pudo publicar");
  }
  delay(1000);
}