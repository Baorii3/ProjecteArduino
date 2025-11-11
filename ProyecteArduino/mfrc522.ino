extern MFRC522 rfid; 

void SetupRFID() {
  Serial.begin(115200);
  SPI.begin();          
  rfid.PCD_Init();      
}

String CheckRFID() {
  // Si no hay nueva tarjeta, salir
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return "";
  }

  // Si hay tarjeta, imprimir UID
  String result = "";
  Serial.print("Tarjeta detectada: ");
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) Serial.print("0"); // Formato hexadecimal con 2 dígitos
    Serial.print(rfid.uid.uidByte[i], HEX);
    result += String(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();
  return result;
}
