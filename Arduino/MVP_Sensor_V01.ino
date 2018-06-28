#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SoftEasyTransfer.h>

SoftwareSerial btSerial(10, 11);
SoftEasyTransfer btOutgoing;

bool configMode = false;

struct sensorStructuredData{
  unsigned long sensorID;
  int position;
  int angle;
  int sensorLap;
  float altitude;
  byte temperature;
  byte humidity;
} sensorData[1];

/*Setup device*/
void setup() {
  Serial.begin(38400);
  btSerial.begin(38400);
  btOutgoing.begin(details(sensorData), &btSerial);
}

void loop(){ //sensorDelay(); > smartbandDelay();
  btOutgoing.sendData();
  delay(300);
  if (Serial.available()>0 && configMode == false){
    Serial.println("Inicializando opções de configuração...");
    configMode = true;
    pythonConfigSensor(); }
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
  else if (method == "clear"){
    for (eeAddress = 0; eeAddress < EEPROM.length() ; eeAddress++){
    EEPROM.write(eeAddress, 0); }
    }
}

void pythonConfigSensor(){
  byte index;
  char incomingFlag = Serial.read();
  /*Display configuration menu options*/
  Serial.println("Modo de configuração ativado.");
  Serial.println("Envie 'V' para visualizar os dados do sensor...");
  Serial.println("Envie 'A' para apagar dados do sensor...");
  Serial.println("Para reconfigurar o sensor, apague os dados atuais ('A') e envie 'C'...");
  Serial.println("Aperte 'Q' para sair");
  /*Quit configuration menu option*/
  if(incomingFlag == 'q'){ //Quit configuration mode 
    configMode == false; }
  /*Send present data/settings to python*/ 
  if(incomingFlag == 'v'){ //Visualize collected data
    Serial.println("Enviando dados do sensor...");
    eepromMethod("sens get", 0); delay(100);
    Serial.println(sensorData[0].sensorID); delay(100);
    Serial.println(sensorData[0].position); delay(100);
    Serial.println(sensorData[0].angle); delay(100);
    Serial.println(sensorData[0].sensorLap); delay(100);
    Serial.println(sensorData[0].altitude); delay(100);
    Serial.println(sensorData[0].temperature); delay(100);
    Serial.println(sensorData[0].humidity); delay(100);
    Serial.println("Dados enviados com êxito!"); }
  /*Erase EEPROM data*/
  if(incomingFlag == 'a'){
    Serial.println("Apagando dados do sensor...");
    eepromMethod("clear", 1);
    Serial.println("Dados apagados com êxito!"); }
  /*Write incoming python data in EEPROM*/ 
  if(incomingFlag == 'c'){ //Start 'Configuration'
    Serial.println("Reconfigurando sensor...");
    sensorData[0].sensorID = Serial.read();
    sensorData[0].position = Serial.read();
    sensorData[0].angle = Serial.read();
    sensorData[0].sensorLap = Serial.read();
    sensorData[0].altitude = Serial.read();
    sensorData[0].temperature = Serial.read();
    sensorData[0].humidity = Serial.read();
    eepromMethod("sens put", 0);
    Serial.println("Sensor configurado com êxito!"); }
}
