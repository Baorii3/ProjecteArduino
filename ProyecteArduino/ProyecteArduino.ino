//Variables d'estat
bool WifiConnected=false;
bool AWSConnected=false;

#include <SPI.h>
#include <MFRC522.h>
#define RST_PIN 22  
#define SS_PIN 21
MFRC522 rfid(SS_PIN, RST_PIN);

String RFIDTag="";
int ledPinGreen = 15;
int ledPinRed = 16;

String payload = "";

void setup() {
  SetupWifi();
  SetupAWS();
  SetupRFID();
  Serial.begin(115200);
  pinMode(ledPinGreen,OUTPUT);
  pinMode(ledPinRed,OUTPUT);
}
void loop() {
  // put your main code here, to run repeatedly:
  CheckWifi();
  if (WifiConnected) {
    //Si estem conectats a wifi, connectem a AWS.
    CheckAWS();
    if (AWSConnected) {
      //Si estem connectats a AWS mirem si hi ha tarja per llegir
      RFIDTag = CheckRFID();
        //Si estem connectats a AWS i hi ha tarja per llegir,
      if (RFIDTag.length() > 0) {
        //Publica Tag
        PublicaTag(RFIDTag);
        
      }
    }
  }
}
