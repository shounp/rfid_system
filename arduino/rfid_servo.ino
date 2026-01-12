#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN 5
#define SS_PIN 10

Servo sg90;
MFRC522 mfrc522(SS_PIN, RST_PIN);

String comando = "";

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  sg90.attach(3);
  sg90.write(0);
}

void loop() {
  // 1. Lê comandos vindos do Python
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      comando.trim();

      if (comando == "OPEN") {
        sg90.write(90);   // abre
      }
      else if (comando == "CLOSE") {
        sg90.write(0);    // fecha
      }

      comando = "";
    } else {
      comando += c;
    }
  }

  // 2. Lê cartão RFID e manda SOMENTE o UID
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();

  Serial.println(uid);   // <-- só isso vai para o Python

  mfrc522.PICC_HaltA();
  delay(1500);           // evita leituras duplicadas
}
