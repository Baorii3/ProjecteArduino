#include <WiFi.h>
extern MFRC522 rfid; 

#define LED_VERDE 16
#define LED_ROJO 17
extern bool WifiConnected;

const char* ssid = "iPhone 16";
const char* password = "robowifi";


void SetupWifi() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();


  // Pines LEDs
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);


  // Conexión Wi-Fi
  Serial.print("Conectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  WifiConnected = true;
}


void CheckWifi() {
  if (WiFi.status() == WL_CONNECTED) {
    WifiConnected = true;
    return;
  }
  else {
    WifiConnected = false;
    return;
  }
}
