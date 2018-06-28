/*Libraries*/
#include <Bounce2.h>
#include <EEPROM.h>
#include <SoftEasyTransfer.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <I2Cdev.h>
#include <Kalman.h>
#include "MPU6050.h"
#include <HMC5883L.h>
#include "Adafruit_Sensor.h"
#include "Adafruit_BMP085_U.h"
#include "Time.h"

/*Create object instances: class objectName = classObject(*parameter)*/
//Bounce2 (debouncer):
Bounce dbButtonLeft = Bounce();
Bounce dbButtonRight = Bounce();
//SoftEasyTransfer + SoftwareSerial (bluetooth):
SoftwareSerial btSerial(10, 11);
SoftEasyTransfer btIncoming, btOutgoing;
//GY-88 modules' objects:
MPU6050 accelgyro;
MagnetometerScaled scaled;
HMC5883L compass;
Adafruit_BMP085_Unified bmp;
//Filters
Kalman kx, ky, kz;

/*Global constants:*/
#define LOOP 0
#define GUIDE_MODE 1
#define FOLLOWER_MODE 2
#define SENSOR_GUIDED_MODE 3
#define NO_DATA_COLLECTION_MODE 4
#define VIBRATOR_LEFT 5
#define VIBRATOR_RIGHT 6
//TBD: Varies from track to track
#define SENSORS_IN_TRACK 4
//
#define WALKING_ACC 33000 //acc. for wlaking
#define ACC_RUNNING 46000 //acc. for running
#define ACC_RUNNIN_REF 1300 //acc. for running //fixxxx

/*Global variables:*/
//GY-88/10-DOF data:
float ax, ay, az;
float gx, gy, gz;
float mx, my, mz;
float temperature, altitude, pressure;

/*Structured data:*/
struct smartbandStructuredData{
  unsigned long controlID = 9374;
  byte profileID = 51;
  byte misguidances = 0;
  float guideOrientation = 0;
  float followerOrientation = 0;
} smartbandData[1];

struct sensorStructuredData{
  unsigned long sensorID;
  int position;
  int angle;
  int sensorLap;
  float altitude;
  byte temperature;
  byte humidity;
} sensorData[SENSORS_IN_TRACK];

/*"Volatile" variables:*/
//UserMode configuration variables:
byte userMode, structArrayCounter = 0;
unsigned long buttonTimer;
bool timerOn = false, jumpToLoop = false, stroll = false, halfPass = false, sprint = false;

/*Setup Arduino & Modules*/
void setup(){
  //Arduino's modules' definitions
  pinMode(VIBRATOR_LEFT, INPUT);
  pinMode(VIBRATOR_RIGHT, INPUT);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  //Debouncer methods
  dbButtonLeft.attach(7);
  dbButtonLeft.interval(20);
  dbButtonRight.attach(8);
  dbButtonRight.interval(20);
  //Initialize modules
  Wire.begin();
  accelgyro.initialize();

/*   i.ADD WIRE TRANSMISSION ADDRESS'
 *  ii.DISABLE SLEEP TO TURN COMPASS ON
 * iii.Fix compass??
 *  vi.CHECK AHRS!
  compass = HMC5883L();
  compass.SetScale(1.3);
   = compass.SetMeasurementMode(Measurement_Continuous);
*/
   
  //Wait for BMP to begin
  if (!bmp.begin()) {
    while (1) {}
    }
  btSerial.begin(38400);
}

/*Device ______*/
void loop(){
  userMode = configUserMode();
  switch (userMode){
    //Case 1: Left button + short press
    case GUIDE_MODE:
        vibratorWarning(7, 1, 1000);
        //btIncoming.begin(details(sensorData), &btSerial);
        btIncoming.begin(details(smartbandData.followerOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData.guideOrientation), &btSerial);
      break;
    //Case 2: Left button + long press
    case FOLLOWER_MODE:
        vibratorWarning(7, 2, 1000);
        btIncoming.begin(details(smartbandData.guideOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData.followerOrientation), &btSerial);
      break;
    //Case 3: Right button + short press
    case SENSOR_GUIDED_MODE:
        vibratorWarning(7, 3, 1000);
        btIncoming.begin(details(sensorData), &btSerial);
      break;
    //Case 4: Right button + long press
    case NO_DATA_COLLECTION_MODE:
        vibratorWarning(7, 4, 1000);
      break;
    //Case 0: No buttons are being pressed...
    case LOOP:
      btOutgoing.sendData();
      if (Serial.available() > 0){ //smartbandDelay(); < sensorDelay();
        btIncoming.receiveData(); //Attempt to avoid buffer buildups: Rx rate > Tx rate
        eepromMethod("put band", structArrayCounter); }
        delay(10);
        }
}

byte configUserMode(){
  userMode = LOOP;
  byte buttonPressRight, buttonPressLeft;
  dbButtonLeft.update();
  dbButtonRight.update();
  
  /*Left Button*/
  //Start timer if...
  if (dbButtonLeft.fell()){
    buttonTimer = millis();
    timerOn = true; }
  if (dbButtonLeft.rose()){
    buttonPressLeft = (millis() - buttonTimer);
    timerOn = false; }
  //Case 1 (short press): Guider mode = 1
  if (buttonPressLeft > 0 && buttonPressLeft <= 250){
    userMode = GUIDE_MODE;
    buttonPressLeft = 0; }
  //Case 2: Follower mode = 2
  if (timerOn == true && (millis() - buttonPressLeft) > 3000){
    userMode = FOLLOWER_MODE;
    timerOn = false;
    buttonPressLeft = 0; }
  
  /*Right button*/
  //Start timer if...
  if (dbButtonRight.fell()){
    buttonTimer = millis();
    timerOn = true; }
  if (dbButtonRight.rose()){
    buttonPressRight = (millis() - buttonTimer);
    timerOn = false; }
  //Case 3 (short press): Sensor guided mode = 3
  if (buttonPressRight > 0 && buttonPressRight <= 250){
    userMode = SENSOR_GUIDED_MODE;
    buttonPressRight = 0; }
  //Case 4 (long press): Display data only, none collected = 4
  if (timerOn == true && (millis() - buttonPressRight) > 3000){
    userMode = NO_DATA_COLLECTION_MODE;
    timerOn = false;
    buttonPressRight = 0; }
  
  //Return result
  return userMode;
}

void vibratorWarning(int side, byte intensity, int interval){
  for (byte i; i<intensity; i++){
    if (side == 7){
      digitalWrite(VIBRATOR_LEFT,HIGH);
      digitalWrite(VIBRATOR_RIGHT, HIGH);
      delay(interval);
      digitalWrite(VIBRATOR_LEFT, LOW);
      digitalWrite(VIBRATOR_RIGHT,LOW); }
    else{
      digitalWrite(side,HIGH);
      delay(interval);
      digitalWrite(side,LOW);}
    }
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
  else if (method == "band put"){
    EEPROM.put(eeAddress, smartbandData[index]); }
  else if (method == "band get"){
    EEPROM.get(eeAddress, smartbandData[index]); }
}

//FIX: Enviar structs...
void sendDataToPython(){
  byte index;
  static bool setupDone = false;

  /*Reset static bool if python says to do so*/ 
  Serial.begin(38400);
  if (Serial.available() > 0 && Serial.read() == 'x'){
    setupDone = false; }
  
  /*Send present data/settings to python*/ 
  while (Serial.available() > 0 && setupDone == false){
    if(Serial.read() == 't'){ //Python flag to Arduino: start collected data 'Transmission'
      for(index = 0; index < SENSORS_IN_TRACK; index++){
        eepromMethod("get sens", index); delay(10);
        Serial.println(sensorData[index].sensorID); delay(10);
        Serial.println(sensorData[index].position); delay(10);
        Serial.println(sensorData[index].angle); delay(10);
        Serial.println(sensorData[index].sensorLap); delay(10);
        Serial.println(sensorData[index].altitude); delay(10);
        Serial.println(sensorData[index].temperature); delay(10);
        Serial.println(sensorData[index].humidity); delay(10);
        Serial.println('s'); } //Arduino flag: last data from index sent
      
      Serial.println('b'); delay(10); //Arduino flag: type 'smartBand' data is being sent
        eepromMethod("get band", 1); delay(10);
        Serial.println(smartbandData[index].controlID); delay(10);
        Serial.println(smartbandData[index].profileID); delay(10);
        Serial.println(smartbandData[index].misguidances); delay(10);
        Serial.println('b'); //Arduino flag: all structured data sent
      
      if(Serial.read() == 'e') {}
        for (index = 0; index < EEPROM.length() ; index++){
          EEPROM.write(index, 0); }
      }
      
    /*Write incoming python data in EEPROM*/ 
    while (!Serial.available()) {}
    if(Serial.read() =  'c'){ //Python flag: start 'Configuration'
      for(index = 0; index < SENSORS_IN_TRACK; index++){
        sensorData[index].sensorID = Serial.read(); delay(10);
        sensorData[index].position = Serial.read(); delay(10);
        sensorData[index].angle = Serial.read(); delay(10);
        sensorData[index].sensorLap = Serial.read(); delay(10);
        sensorData[index].altitude = Serial.read(); delay(10);
        sensorData[index].temperature = Serial.read(); delay(10);
        sensorData[index].humidity = Serial.read(); delay(10);
        eepromMethod("put sens", index); delay(1000);
        Serial.println('s'); } //Arduino flag: last sensor from index saved
      
      Serial.println('b'); //Arduino flag: type 'smartBand' data is being saved on EEPROM
        Serial.read() = (smartbandData[0].controlID); delay(10);
        Serial.read() = (smartbandData[0].profileID); delay(10);
        Serial.read() = (smartbandData[0].misguidances); delay(10);
        eepromMethod("put band", 1); delay(1000);
        Serial.println('b'); //Arduino flag: all structured data saved on EEPROM
      }
   setupDone == true;
  }
}
  
