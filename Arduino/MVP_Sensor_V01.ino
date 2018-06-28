#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SoftEasyTransfer.h>

SoftwareSerial btSerial(10, 11);
SoftEasyTransfer btOutgoing;

struct sensorStructuredData{
  unsigned long sensorID = 28101014;
  int position = 3200;
  int angle;
  int sensorLap;
  float altitude;
  byte temperature;
  byte humidity = 88;
} sensorData[1];

/*Setup device*/
void setup() {
  btSerial.begin(38400);
  btOutgoing.begin(details(sensorData), &btSerial);
}

void loop(){ //sensorDelay(); > smartbandDelay();
  btOutgoing.sendData();
  delay(500);
}


void eepromMethod(char method[8], byte index){
  unsigned long eeAddress = 0;
  eeAddress += sizeof(unsigned long);
  //Write data in EEPROM address:
  if (method == "sens put"){
    EEPROM.put(eeAddress, sensorData[index]); }
  //Access data written in EEPROM address:
  else if (method == "sens get"){
    EEPROM.get(eeAddress, sensorData[index]); }
}


void sensorConfig(){
  byte index;
  static bool , setupDone = false;
  
  Serial.begin(38400);
  if (Serial.available() > 0 && Serial.read() == 'x'){
    setupDone = false; }
  
  /*Send present data/settings to python*/ 
while (Serial.available() > 0 && setupDone == false){
    if(Serial.read() == 't'){ //Python flag to Arduino: start collected data 'Transmission'
      for(index = 0; index < 1; index++){
        eepromMethod("get sens", index); delay(10);
        Serial.println(sensorData[index].sensorID); delay(10);
        Serial.println(sensorData[index].position); delay(10);
        Serial.println(sensorData[index].humidity); delay(10);
        Serial.println('s'); } //Arduino flag: last data from index sent
      while (pythonFlag != 'e') {} //Python flag: 'Erase' EEPROM
        for (index = 0; index < EEPROM.length() ; index++){
          EEPROM.write(index, 0); }
      }
          
    /*Write incoming python data in EEPROM*/ 
    if(pythonFlag == 'c'){ //Python flag: start 'Configuration'
        sensorData[0].sensorID = Serial.read(); delay(10);
        sensorData[0].position = Serial.read(); delay(10);
        sensorData[0].angle = Serial.read(); delay(10);
        sensorData[0].sensorLap = Serial.read(); delay(10);
        sensorData[0].altitude = Serial.read(); delay(10);
        sensorData[0].temperature = Serial.read(); delay(10);
        sensorData[0].humidity = Serial.read(); delay(10);
        eepromMethod("put sens", 1);
        Serial.println('s'); } //Arduino flag: last sensor from index saved
        }
   setupDone == true;
  }
}
}
