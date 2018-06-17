// MASTER: +ADDR:2017:2:270343 ~ pulseira
// SLAVE: +ADDR:2017:2:270343 ~ sensor
#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SoftEasyTransfer.h>
SoftwareSerial btSerial(10, 11); //rx,tx
SoftEasyTransfer ET;

int vibrador = 3;
char readPython;

unsigned long address = 0L;
unsigned long startPython = 999999997;
unsigned long flagPython = 999999998;
unsigned long endPython = 999999999;

struct artefatoStructuredData{
  int userID = 1; // Apenas em casos de Gamification
  int controlID = 93563;
  int sensorIDs[];
} artefatoData;

struct sensorStructuredData{
  unsigned long sensorID;
  int angle;
  int humidity;
  int sensorPos;
  int temperature;
} sensorData;

void sensorToPython() {
  unsigned long eeAddress = sizeof(unsigned long);
  sensorStructuredData sensorData;
  EEPROM.get(eeAddress, sensorData);
      Serial.println(sensorData.sensorID);
      delay(1000);
      Serial.println(sensorData.angle);
      delay(1000);
      Serial.println(sensorData.humidity);
      delay(1000);
      Serial.println(sensorData.sensorPos);
      delay(1000);
      Serial.println(sensorData.temperature);
  delay(1000);
  Serial.println(flagPython);
  delay(1000);
  //if (readPython == 'b') {
    //for (int16_t i = 0 ; i < EEPROM.length() ; i++) {
      //EEPROM.write(i, 0);
      //}
    //}
  Serial.println(endPython);
}
void setup() { 
  pinMode(vibrador,OUTPUT);
  digitalWrite(vibrador,LOW);
  Serial.begin(38400);
  btSerial.begin(38400);
  delay(1000);
  if (btSerial.available() > 0); {
    delay(1000);
    sensorToPython();
    }
  ET.begin(details(sensorData), &btSerial);
}

void clearEEPROM() {
  pinMode(2, OUTPUT);
  for (unsigned long i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.write(i, 0);
  }
  digitalWrite(2, HIGH);
}

void putEEPROM() {
  unsigned long eeAddress = sizeof(unsigned long);
  EEPROM.put(eeAddress, sensorData);
}

void getEEPROM() {
  unsigned long eeAddress = sizeof(unsigned long);
  sensorStructuredData sensorData;
  EEPROM.get(eeAddress, sensorData);
}

void loop() {
  int i = 0;
  if (btSerial.available() > 0); {
    digitalWrite(vibrador,HIGH);
    if(ET.receiveData()){
      digitalWrite(vibrador,LOW);
      putEEPROM();
      delay(200);
      getEEPROM();
      Serial.println(sensorData.sensorID);
      delay(200);
      Serial.println(sensorData.angle);
      delay(200);
      Serial.println(sensorData.humidity);
      delay(200);
      Serial.println(sensorData.sensorPos);
      delay(200);
      Serial.println(sensorData.temperature);
      i = i + 1;
      }
    delay(200); //smartbandDelay(); < sensorDelay();
    }
}
