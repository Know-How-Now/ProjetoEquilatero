// MASTER: +ADDR:2017:2:270343 ~ pulseira
// SLAVE: +ADDR:2017:2:270343 ~ sensor
#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SoftEasyTransfer.h>

SoftwareSerial btSerial(10, 11); //rx,tx
SoftEasyTransfer ET;

unsigned int eeAddress = 0L;
  
struct structuredData{
  unsigned long sensorID = 23785639;
  int angle = 314;
  int humidity = 28;
  int sensorPos = 5118;
  int temperature = 33;
} sensorData;

void setup() {
  btSerial.begin(38400);
  ET.begin(details(sensorData), &btSerial);
}

void clearEEPROM() {
  pinMode(2, OUTPUT);
  for (unsigned int i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.write(i, 0);
  }
  digitalWrite(2, HIGH);
}

void loop() {
  ET.sendData();
  delay(4000); //sensorDelay(); > smartbandDelay();
}
