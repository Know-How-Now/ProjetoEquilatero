#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <HMC5883L.h>
#include <Adafruit_BMP085.h>
//#include <Kalman.h>
#include <Bounce2.h>
#include <EEPROM.h>
#include <SoftEasyTransfer.h>
#include <SoftwareSerial.h>

/*Create object instances: class objectName = classObject(*parameter)*/
//Debouncer):
Bounce dbButtonLeft = Bounce();
Bounce dbButtonRight = Bounce();
//Bluetooth:
SoftwareSerial btSerial(10, 11);
SoftEasyTransfer btGuideIN, btGuideOUT, btFollowerIN, btFollowerOUT, btSensorIN, btBetaUser;
//GY-88:
MPU6050 mpu;
HMC5883L compass;
Adafruit_BMP085 bmp;
//Kalman: 
//Kalman kx, ky, kz;

/*Define constant variables:*/
#define DEFAULT_MODE 0
#define GUIDE_MODE 1
#define FOLLOWER_MODE 2
#define SENSOR_GUIDED_MODE 3
#define NO_DATA_COLLECTION_MODE 4
#define VIBRATOR_LEFT 5
#define VIBRATOR_RIGHT 6
#define SENSORS_IN_TRACK 4
#define DECLINATION_ANGLE -0.3843
#define SEA_LEVEL_PRESSURE 101700

/*Structured data:*/
struct smartbandStructuredData{
  unsigned long CONTROL_ID = 9374;
  byte PROFILE_ID = 51;
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

/*Global Variables*/
//MPU, HMC, BMP
float ax, ay, az;
float gx, gy, gz;
float mx, my, mz;
float heading, altitude, temperature;

/*Pedometer -- FUTURE IMPLEMENTATION
stroll = false, halfPass = false, sprint = false;
*/

/*"Volatile" variables:*/
//Configuration-related
byte userMode, prevUserMode = 0;

//Counter-related variables
byte structArrayCounter = 0;
bool timerOn = false;
unsigned long buttonTimer, lapTimer;

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
  Wire.begin();
  Serial.begin(38400);
  //Initialize & configure MPU6050 (accelerometer)
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)){
    delay(500); }
  mpu.setI2CMasterModeEnabled(false);
  mpu.setI2CBypassEnabled(true) ;
  mpu.setSleepEnabled(false);
  while (!compass.begin()){
    delay(500); }
  compass.setRange(HMC5883L_RANGE_1_3GA); //Range in gauss
  compass.setMeasurementMode(HMC5883L_CONTINOUS); //Set compass. to measure continuously
  compass.setDataRate(HMC5883L_DATARATE_30HZ); //Rate of compass. data collectioon
  compass.setSamples(HMC5883L_SAMPLES_8); //Num. of samples to average
  compass.setOffset(0, 0); //Mag. calibration
  while (!bmp.begin()){
    delay(500); }
  btSerial.begin(38400);
  btGuideIN.begin(details(smartbandData[0].followerOrientation), &btSerial);
  btGuideOUT.begin(details(smartbandData[0].guideOrientation), &btSerial);
  btFollowerIN.begin(details(smartbandData[0].guideOrientation), &btSerial);
  btFollowerOUT.begin(details(smartbandData[0].followerOrientation), &btSerial);
  btSensorIN.begin(details(sensorData), &btSerial);
  //btBetaUser.begin(details(betaData), &btSerial);
  Serial.begin(38400);
  if (Serial.available() > 0){
    sendDataToPython();
  }
}

void loop(){
  Vector acc = mpu.readScaledAccel();
  Vector mag = compass.readNormalize();
  lapTimer = micros();
  
  userMode = configUserMode();
  switch (userMode){
    //Case 0: No buttons are being pressed...
    case DEFAULT_MODE:
      //userMode = prevUserMode;
      break;
    //Case 1: Left button + short press
    case GUIDE_MODE:
      if(prevUserMode != userMode){ 
        vibratorWarning(7, 1, 1000); }
      tiltCompensation(mag, acc);
      smartbandData[0].guideOrientation = (int)(heading * 180/M_PI);
      btGuideOUT.sendData();
      if (btSerial.available() > 0){
        btGuideIN.receiveData(); 
        if (abs(smartbandData[0].guideOrientation) != (abs(smartbandData[0].followerOrientation) +- 15)){
          vibratorWarning(7, 3, 200); }
        }
        break;
    //Case 2: Left button + long press
    case FOLLOWER_MODE:
      if(prevUserMode != userMode){ 
        vibratorWarning(7, 2, 1000); }
      tiltCompensation(mag, acc);
      smartbandData[0].followerOrientation = (int)(heading * 180/M_PI);
      btFollowerOUT.sendData();
      if (btSerial.available() > 0){
        btFollowerIN.receiveData(); 
        if (abs(smartbandData[0].followerOrientation) != (abs(smartbandData[0].guideOrientation)) +- 15){
          vibratorWarning(7, 3, 200); }
        }
      break;
    //Case 3: Right button + short press
    case SENSOR_GUIDED_MODE:
      if(prevUserMode != userMode){ 
        vibratorWarning(7, 3, 1000); }
      if (btSerial.available() > 0){ 
        if(btSensorIN.receiveData()){
        double sensorLap = (double)(micros() - lapTimer) / 1000000;
        temperature = bmp.readTemperature();
        altitude = bmp.readAltitude(SEA_LEVEL_PRESSURE);
        sensorData[structArrayCounter].temperature = temperature;
        sensorData[structArrayCounter].altitude = altitude;
        sensorData[structArrayCounter].humidity = 88; //random humidity
        sensorData[structArrayCounter].sensorLap = (float)(micros() - lapTimer) / 100000000;
        eepromMethod("sens put", structArrayCounter);
        structArrayCounter++; }
        }
      break;
    //Case 4: Right button + long press
    case NO_DATA_COLLECTION_MODE:
      if(prevUserMode != userMode){ 
        vibratorWarning(7, 4, 1000); }
      break;
    }    
   prevUserMode = userMode;
      
  delay(500);
}

byte configUserMode(){
  byte buttonPressRight, buttonPressLeft;
  userMode = DEFAULT_MODE;
  dbButtonLeft.update();
  dbButtonRight.update();
  
  /*Left Button*/
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
    
  return userMode;
}

void vibratorWarning(int side, byte duration, int interval){
  for (byte i; i<duration; i++){
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

void eepromMethod(String method, byte index){
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

float tiltCompensation(Vector mag, Vector normAccel){
  float roll = asin(normAccel.YAxis);
  float pitch = asin(-normAccel.XAxis);
  
  float cosRoll = cos(roll);
  float sinRoll = sin(roll);  
  float cosPitch = cos(pitch);
  float sinPitch = sin(pitch);
                
  float Xh = mag.XAxis * cosPitch + mag.ZAxis * sinPitch;
  float Yh = mag.XAxis * sinRoll * sinPitch + mag.YAxis * cosRoll - mag.ZAxis * sinRoll * cosPitch;
  
  heading = atan2(Yh, Xh);
  return heading;
}

void sendDataToPython(){
  byte index;
  char pythonFlag = Serial.read();  
  //Collect profile data
  if(pythonFlag == 'b'){ 
    eepromMethod("get band", 1); delay(100);
    Serial.println(smartbandData[index].CONTROL_ID); delay(100);
    Serial.println(smartbandData[index].PROFILE_ID); delay(100);
    Serial.println(smartbandData[index].misguidances); delay(100);
    Serial.println("\t"); }
  //Collect sensor data
  if(pythonFlag == 's'){
    for(index = 0; index < SENSORS_IN_TRACK; index++){
      eepromMethod("sens get", index); delay(100);
      Serial.println(sensorData[index].sensorID); delay(100);
      Serial.println(sensorData[index].position); delay(100);
      Serial.println(sensorData[index].angle); delay(100);
      Serial.println(sensorData[index].sensorLap); delay(100);
      Serial.println(sensorData[index].altitude); delay(100);
      Serial.println(sensorData[index].temperature); delay(100);
      Serial.println(sensorData[index].humidity); delay(100);
      Serial.println("\t"); } } 
  //Clear Smartband EEPROM
  if(pythonFlag = 'e'){
    for (index = 0; index < EEPROM.length() ; index++){
      EEPROM.write(index, 0); 
      Serial.println("\t"); } }
  //Configure Smartband
  if(pythonFlag = 'c'){
    smartbandData[0].CONTROL_ID = Serial.read(); delay(100);
    smartbandData[0].PROFILE_ID = Serial.read(); delay(100);
    eepromMethod("band put", 0); delay(1000);
    Serial.println("\t"); }
}
