/*Libraries*/
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <HMC5883L.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_HMC5883_U.h"
#include "Adafruit_BMP085_U.h"
#include <Kalman.h>
#include <Bounce2.h>
#include <EEPROM.h>
#include <SoftEasyTransfer.h>
#include <SoftwareSerial.h>

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
Adafruit_HMC5883_Unified mag;
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
#define SENSORS_IN_TRACK 4
#define DECLINATION_ANGLE -0.38502
#define SEA_LEVEL_PRESSURE 1017

/*Global variables:*/
//GY-88/10-DOF data:
int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;

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
unsigned long buttonTimer, lapTimer;
bool setupDone = false, timerOn = false, jumpToLoop = false, stroll = false, halfPass = false, sprint = false;
float altitude, temperature, pressure;

/*Setup Arduino & Modules*/
void setup(){
  Serial.begin(38400);
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
  Wire.begin();delay(50);
  accelgyro.initialize();delay(50);
  mag.begin();delay(50);
  bmp.begin();delay(50);
  btSerial.begin(38400);
  //compass = HMC5883L();
  //compass.SetScale(1.3);
  //compass.SetMeasurementMode(Measurement_Continuous);
  for (int i = 0; i >= 10; i++) {
  userMode = configUserMode();
  switch (userMode){
    //Case 1: Left button + short press
    case GUIDE_MODE:
        vibratorWarning(7, 1, 1000);
        btIncoming.begin(details(smartbandData[0].followerOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData[0].guideOrientation), &btSerial);
      break;
    //Case 2: Left button + long press
    case FOLLOWER_MODE:
        vibratorWarning(7, 2, 1000);
        btIncoming.begin(details(smartbandData[0].guideOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData[0].followerOrientation), &btSerial);
      break;
    //Case 3: Right button + short press
    case SENSOR_GUIDED_MODE:
        vibratorWarning(7, 3, 1000);
        btIncoming.begin(details(sensorData), &btSerial);
      break;
    //Case 4: Right button + long press
    case NO_DATA_COLLECTION_MODE:
      vibratorWarning(7, 4, 1000);
      setupDone = false;
      break;
    //Case 0: No buttons are being pressed...
    case LOOP:
      continue;
  }
}


/*Device ______*/
void loop(){
  /*userMode = configUserMode();
  switch (userMode){
    //Case 1: Left button + short press
    case GUIDE_MODE:
        vibratorWarning(7, 1, 1000);
        btIncoming.begin(details(smartbandData[0].followerOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData[0].guideOrientation), &btSerial);
      break;
    //Case 2: Left button + long press
    case FOLLOWER_MODE:
        vibratorWarning(7, 2, 1000);
        btIncoming.begin(details(smartbandData[0].guideOrientation), &btSerial);
        btOutgoing.begin(details(smartbandData[0].followerOrientation), &btSerial);
      break;
    //Case 3: Right button + short press
    case SENSOR_GUIDED_MODE:
        vibratorWarning(7, 3, 1000);
        btIncoming.begin(details(sensorData), &btSerial);
      break;
    //Case 4: Right button + long press
    case NO_DATA_COLLECTION_MODE:
      vibratorWarning(7, 4, 1000);
      setupDone = false;
      break;
    //Case 0: No buttons are being pressed...
    case LOOP:*/
      sensors_event_t event;
      mag.getEvent(&event);
      bmp.getEvent(&event);
      
      float heading = atan2(event.magnetic.y, event.magnetic.x);
      heading += DECLINATION_ANGLE;
      if(heading < 0)
        heading += 2*PI;
      if(heading > 2*PI)
        heading -= 2*PI;
        
      float headingDegrees = heading * 180/M_PI; 
      
      Serial.print(headingDegrees);
      //accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
      //ax = abs(ax);
      //ay = abs(ay);
      //az = abs(az);
      
      if (structArrayCounter == 0){
          lapTimer = micros(); 
          }
      
      btOutgoing.sendData();
      if (btSerial.available() > 0){ //smartbandDelay(); < sensorDelay();
        btIncoming.receiveData(); //Attempt to avoid buffer buildups: Rx rate > Tx rate
        double sensorLap = (double)(micros() - lapTimer) / 1000000;
        bmp.getPressure(&pressure);
        bmp.getTemperature(&temperature);
        bmp.pressureToAltitude(1017, event.pressure, event.temperature);
        
        sensorData[structArrayCounter].temperature = temperature;
        sensorData[structArrayCounter].altitude = altitude;
        sensorData[structArrayCounter].humidity = 88;
        sensorData[structArrayCounter].sensorLap = (float)(micros() - lapTimer) / 100000000;
        
        eepromMethod("put band", structArrayCounter);
        lapTimer = micros();
        }
        
        delay(10);
        }        
//}

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
  char pythonFlag = Serial.read();

  if (setupDone = false){
  if(pythonFlag = 't'){ //Python flag to Arduino: start collected data 'Transmission'
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
    
    if(pythonFlag = 'e') {}
      for (index = 0; index < EEPROM.length() ; index++){
        EEPROM.write(index, 0); }
    }
    
  if(pythonFlag = 'c'){ //Python flag: start 'Configuration'
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
      smartbandData[0].controlID = Serial.read();
      smartbandData[0].profileID = Serial.read();
      smartbandData[0].misguidances = Serial.read();
      eepromMethod("put band", 1); delay(1000);
      Serial.println('b'); //Arduino flag: all structured data saved on EEPROM
      }
   setupDone == true;
  }
}
