#include "Wire.h"
#include "Kalman.h"
#include "I2Cdev.h"
#include "MPU6050.h"
#include "HMC5883L.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SoftEasyTransfer.h>

SoftwareSerial btSerial(10, 11); //rx,tx
SoftEasyTransfer ET;
// MASTER: +ADDR:2017:2:270343 ~ pulseira
// SLAVE: +ADDR:2017:2:270343 ~ sensor

unsigned long address = 0L;
unsigned long eeAddress = sizeof(unsigned long);
#define ARRAY_SIZE 10

struct artefatoStructuredData{
  int profileID = 1;
  int controlID = 93563;
} artefatoData;

struct sensorStructuredData{
  long sensorID;
  float sensorsDT;
  int altitude;
  int angle;
  int temperature;
  int humidity;
} sensorData;
//Dynamic arraY? -> int foo; int size = 10; foo = (int)malloc(size * sizeof(int)); free(foo);

// Create the Kalman instances
Kalman kalmanX, kalmanY, kalmanZ;
#define RESTRICT_PITCH 

//Create objects
HMC5883L compass;
Adafruit_BMP085_Unified bmp;
sensors_event_t event;
  
//relogio
double error;
const int vibrador = 3;

//Default address'
const uint8_t MPU6050 = 0x68; 
const uint8_t HMC5883L = 0x1E;
const uint8_t BMP085 = 0x77;

//9-DOF Data
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;
double magX, magY, magZ;
float temperature;

// Roll and pitch are calculated using the accelerometer while yaw is calculated using the magnetometer
double roll, pitch, yaw;
double gyroXangle, gyroYangle, gyroZangle;
double kalAngleX, kalAngleY, kalAngleZ;

//Clock & Timer variables
uint8_t i2cData[14];
uint32_t timer;
float timeToCheckpoint;
float timeReference;

#define MAG0MAX 603
#define MAG0MIN -578
#define MAG1MAX 542
#define MAG1MIN -701
#define MAG2MAX 547
#define MAG2MIN -556

float magOffset[3] = { (MAG0MAX + MAG0MIN) / 2, (MAG1MAX + MAG1MIN) / 2, (MAG2MAX + MAG2MIN) / 2 };
double magGain[3];

//==============================[ I2C: Read/Write ]==============================//
const uint16_t I2C_TIMEOUT = 1000;
uint8_t i2cWrite(uint8_t address, uint8_t registerAddress, uint8_t data, bool sendStop) {
  return i2cWrite(address, registerAddress, &data, 1, sendStop);
}

uint8_t i2cWrite(uint8_t address, uint8_t registerAddress, uint8_t *data, uint8_t length, bool sendStop) {
  Wire.beginTransmission(address);
  Wire.write(registerAddress);
  Wire.write(data, length);
  uint8_t rcode = Wire.endTransmission(sendStop);
  if (rcode) {
    Serial.print(F("i2cWrite failed: "));
    Serial.println(rcode);
  }
  return rcode;
}

uint8_t i2cRead(uint8_t address, uint8_t registerAddress, uint8_t *data, uint8_t nbytes) {
  uint32_t timeOutTimer;
  Wire.beginTransmission(address);
  Wire.write(registerAddress);
  uint8_t rcode = Wire.endTransmission(false); // Don't release the bus
  if (rcode) {
    Serial.print(F("i2cRead failed: "));
    Serial.println(rcode);
    return rcode;
  }
  Wire.requestFrom(address, nbytes, (uint8_t)true);
  for (uint8_t i = 0; i < nbytes; i++) {
    if (Wire.available())
      data[i] = Wire.read();
    else {
      timeOutTimer = micros();
      while (((micros() - timeOutTimer) < I2C_TIMEOUT) && !Wire.available());
      if (Wire.available())
        data[i] = Wire.read();
      else {
        Serial.println(F("i2cRead timeout"));
        return 5;
      }
    }
  }
  return 0;
}

//==============================[ MPU/BMP/HCM ]==============================//
void updateMPU6050() {
  while (i2cRead(MPU6050, 0x3B, i2cData, 14));
  accX = ((i2cData[0] << 8) | i2cData[1]);
  accY = -((i2cData[2] << 8) | i2cData[3]);
  accZ = ((i2cData[4] << 8) | i2cData[5]);
  temperature = (i2cData[6] << 8) | i2cData[7];
  gyroX = -(i2cData[8] << 8) | i2cData[9];
  gyroY = (i2cData[10] << 8) | i2cData[11];
  gyroZ = -(i2cData[12] << 8) | i2cData[13];
}

void updateHMC5883L() {
  while (i2cRead(HMC5883L, 0x03, i2cData, 6));
  magX = ((i2cData[0] << 8) | i2cData[1]);
  magZ = ((i2cData[2] << 8) | i2cData[3]);
  magY = ((i2cData[4] << 8) | i2cData[5]);
/*  
  sensors_event_t event; 
  mag.getEvent(&event);
(event.magnetic.x);
(event.magnetic.y);
(event.magnetic.z);
float heading = atan2(event.magnetic.y, event.magnetic.x);
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI;*/
}

void updatePitchRoll() {
#ifdef RESTRICT_PITCH
  roll = atan2(accY, accZ) * RAD_TO_DEG;
  pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else
  roll = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  pitch = atan2(-accX, accZ) * RAD_TO_DEG;
#endif
}

void updateYaw() {
  magX *= -1;
  magZ *= -1;

  magX *= magGain[0];
  magY *= magGain[1];
  magZ *= magGain[2];

  magX -= magOffset[0];
  magY -= magOffset[1];
  magZ -= magOffset[2];

  double rollAngle = kalAngleX * DEG_TO_RAD;
  double pitchAngle = kalAngleY * DEG_TO_RAD;

  double Bfy = magZ * sin(rollAngle) - magY * cos(rollAngle);
  double Bfx = magX * cos(pitchAngle) + magY * sin(pitchAngle) * sin(rollAngle) + magZ * sin(pitchAngle) * cos(rollAngle);
  double declinationAngle = 0.38502;
  yaw = atan2(-Bfy, Bfx);
  yaw += declinationAngle;
  yaw = yaw * RAD_TO_DEG;
  yaw *= -1;
}

void calibrateMag() {
  i2cWrite(HMC5883L, 0x00, 0x11, true);
  delay(100);
  updateHMC5883L();

  int16_t magPosOff[3] = { magX, magY, magZ };

  i2cWrite(HMC5883L, 0x00, 0x12, true);
  delay(100);
  updateHMC5883L();

  int16_t magNegOff[3] = { magX, magY, magZ };

  i2cWrite(HMC5883L, 0x00, 0x10, true);

  magGain[0] = -2500 / float(magNegOff[0] - magPosOff[0]);
  magGain[1] = -2500 / float(magNegOff[1] - magPosOff[1]);
  magGain[2] = -2500 / float(magNegOff[2] - magPosOff[2]);

#if 0
  Serial.print("Mag cal: ");
  Serial.print(magNegOff[0] - magPosOff[0]);
  Serial.print(",");
  Serial.print(magNegOff[1] - magPosOff[1]);
  Serial.print(",");
  Serial.println(magNegOff[2] - magPosOff[2]);

  Serial.print("Gain: ");
  Serial.print(magGain[0]);
  Serial.print(",");
  Serial.print(magGain[1]);
  Serial.print(",");
  Serial.println(magGain[2]);
#endif
}
//==============================[ ORIENTATION CONTROL ]==============================//


//==============================[ EEPROM: Put, Get, Clear ]==============================//
void putEEPROM() {
  EEPROM.put(eeAddress, sensorData);
}

void getEEPROM() {
  sensorStructuredData sensorData;
  EEPROM.get(eeAddress, sensorData);
}

void clearEEPROM() {
  pinMode(2, OUTPUT);
  for (unsigned long i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.write(i, 0);
  }
  digitalWrite(2, HIGH);
}

//==============================[ BLUETOOTH: Receive data struct if paired ]==============================//
/*void checkArraySize(struct nameAttribute, String name, int teamIRCodes[], int numberOfCodes){
    _teamIRCodes = new int[numberOfCodes];
    // memcpy does the same thing as the for loop - copies the array
    memcpy(_teamIRCodes, teamIRCodes, sizeof(teamIRCodes[0]) * numberOfCodes);
}
}*/

void checkBT() {
  sensorStructuredData sensorData;
  //checkSizeOfArrays();
  btSerial.begin(38400);
  delay(100);
  ET.begin(details(sensorData), &btSerial);
  delay(500);
  if (btSerial.available() > 0) {
    sensorData.sensorsDT = float((timeToCheckpoint/60000) - (timeReference/60000));
    timeReference = timeToCheckpoint;
    if(ET.receiveData()){
      putEEPROM();
      delay(200);
      /*getEEPROM();
        Serial.println(sensorData.sensorID);
        delay(500);
        Serial.println(sensorData.sensorDT);
        delay(500);
        Serial.println(sensorData.altitude);
        delay(500);
        Serial.println(sensorData.angle);
        delay(500);
        Serial.println(sensorData.temperature);
        delay(500);
        Serial.println(sensorData.humidity);*/
      }
    delay(200); //smartbandDelay(); < sensorDelay();
    }
}

//==============================[ PYTHON: Send/Receive data struct if paired ]==============================//
void checkPY() {
  unsigned long startPython = 99999997;
  unsigned long flagPython = 99999998;
  unsigned long endPython = 99999999;
  if (Serial.available() > 0); {
    delay(100);
    sensorStructuredData sensorData;
    EEPROM.get(eeAddress, sensorData);
        /*Serial.println(sensorData.sensorID);
        delay(500);
        Serial.println(sensorData.sensorDT);
        delay(500);
        Serial.println(sensorData.altitude);
        delay(500);
        Serial.println(sensorData.angle);
        delay(500);
        Serial.println(sensorData.temperature);
        delay(500);
        Serial.println(sensorData.humidity);*/
    artefatoStructuredData artefatoData;
    EEPROM.get(eeAddress, artefatoData);
        /*Serial.println(artefatoData.profileID);
        delay(500);
        Serial.println(sensorData.controlID);
        delay(500);*/
    Serial.println(flagPython);
    delay(500);
    //if (readPython == 'b') {
      //for (unsigned long i = 0 ; i < EEPROM.length() ; i++) {
        //EEPROM.write(i, 0);
        //}
      //}
    Serial.println(endPython);
    }
}
//==============================[ PEDOMETER ATTEMPT ]==============================//
/*void steps() {
  int m = 0;

  if (hour() > 1) dayrefresh = true;
  if ((hour() == 0) && (minute() == 0) && (dayrefresh)) {
    for (m = 0; m < (NUM2 - 1); m++) {
      KcalD[m] = KcalD[m + 1];
      stepD[m] = stepD[m + 1];
    }
    KcalD[NUM2] = calorie;
    KcalMed = 0;
    stepMed = 0;
    for (m = 0; m < NUM2; m++) {
      KcalMed = KcalMed + KcalD[m] / NUM2;
      stepMed = stepMed + stepD[m] / NUM2;
    }
    stepT = stepT + passo;
    KcalT = KcalT + calorie;
    calorie = 0;
    stepD[NUM2] = passo;
    passo = 0;
    dayrefresh = false;
  }
}

void pedometer() {
  int m = 0;

  PdXYZ[k] = abs((signed long int) (ax)) + abs((signed long int) (ay)) + abs((signed long int) (az));
  PdXYZant = PdXYZat;
  PdXYZat = PdXYZ[k];

  if (k == (NUM3 - 1)) {
    PdXYZmax[y] = 0;
    for (m = 0; m < NUM3; m++) {
      if (PdXYZmax[y] < PdXYZ[m]) {
        PdXYZmax[y] = PdXYZ[m];
      }
    }
  }
  if (y == (NUM4 - 1)) {
    PdXYZmed = 0;
    for (m = 0; m < NUM4; m++) {
      PdXYZmed = PdXYZmed + PdXYZmax[m] / NUM4;
    }
  }

  if (PdXYZmed > NUM5) {
    if (PdXYZmed > NUM6) {
      correndo = true;
      andando = false;
    } else {
      correndo = false;
      andando = true;
    }
    if ((PdXYZat > (PdXYZant + NUM7)) && (!meiopasso)) {
      meiopasso = true;
      timerpasso = millis();
    }
    if ((PdXYZat < (PdXYZant - NUM7)) && (meiopasso)) {
      activestep++;
      if ((millis() - timer_step) >= 10000) {
        if ((activestep - actstep) >= 10) {
          if (!active) {
            active = true;
            passo = passo + (activestep - actstep);
            calorie = calorie + (correndo * KcalRun + andando * KcalWalk) * (activestep - actstep);
          }
          active = true;
        }
        else {
          active = false;
        }
        actstep = activestep;
        timer_step = millis();
      }
      if (active) {
        passo++;
        calorie = calorie + correndo * KcalRun + andando * KcalWalk;
      }
      meiopasso = false;
    }
  } else {
    correndo = false;
    andando = false;
  }

  if ((millis() - timerpasso) >= 1000) {
    meiopasso = false;
    correndo = false;
    andando = false;
  }

  k++;
  if (k >= NUM3) k = 0;
  y++;
  if (y >= NUM4) y = 0;
}*/

//==============================[ MAIN: Setup & Loop ]==============================//
void setup() {
  pinMode(vibrador,OUTPUT);
  digitalWrite(vibrador,LOW);
  Serial.begin(115200);
  Wire.begin();
  delay(100);
  bmp.begin();
  delay(100);
  
  TWBR = ((F_CPU / 400000L) - 16) / 2; // Set I2C frequency to 400kHz
  
  i2cData[0] = 7;
  i2cData[1] = 0x00;
  i2cData[2] = 0x00;
  i2cData[3] = 0x00;
  
  while (i2cWrite(MPU6050, 0x19, i2cData, 4, false));
  while (i2cWrite(MPU6050, 0x6B, 0x01, true));

  while (i2cWrite(HMC5883L, 0x02, 0x00, true));

  calibrateMag();
  compass.SetScale(1.3);
  error = compass.SetMeasurementMode(Measurement_Continuous);
  delay(100);
  
  /* Set Kalman and gyro starting angle */
  updateMPU6050();
  updateHMC5883L();
  updatePitchRoll();
  updateYaw();

  kalmanX.setAngle(roll);
  gyroXangle = roll;

  kalmanY.setAngle(pitch);
  gyroYangle = pitch;

  kalmanZ.setAngle(yaw);
  gyroZangle = yaw;

  timeToCheckpoint = micros();
  timer = micros();
}

void loop() {
  updateMPU6050();
  updateHMC5883L();

  //Delta Timer
  double dt = (double)(micros() - timer) / 1000000;
  timer = micros();

  updatePitchRoll();
  double gyroXrate = gyroX / 131.0; 
  double gyroYrate = gyroY / 131.0;

#ifdef RESTRICT_PITCH
  if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
    kalmanX.setAngle(roll);
    kalAngleX = roll;
    gyroXangle = roll;
  } else
    kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt);

  if (abs(kalAngleX) > 90)
    gyroYrate = -gyroYrate;
  kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt);
#else
  if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
    kalmanY.setAngle(pitch);
    kalAngleY = pitch;
    gyroYangle = pitch;
  } else
    kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt); 

  if (abs(kalAngleY) > 90)
    gyroXrate = -gyroXrate; 
  kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt);
#endif

  updateYaw();
  double gyroZrate = gyroZ / 131.0;
  if ((yaw < -90 && kalAngleZ > 90) || (yaw > 90 && kalAngleZ < -90)) {
    kalmanZ.setAngle(yaw);
    kalAngleZ = yaw;
    gyroZangle = yaw;
  } else
    kalAngleZ = kalmanZ.getAngle(yaw, gyroZrate, dt); // Calculate the angle using a Kalman filter

  gyroXangle += kalmanX.getRate() * dt;
  gyroYangle += kalmanY.getRate() * dt;
  gyroZangle += kalmanZ.getRate() * dt;

  // Reset the gyro angles when they has drifted too much
  if (gyroXangle < -180 || gyroXangle > 180)
    gyroXangle = kalAngleX;
  if (gyroYangle < -180 || gyroYangle > 180)
    gyroYangle = kalAngleY;
  if (gyroZangle < -180 || gyroZangle > 180)
    gyroZangle = kalAngleZ;

  bmp.getEvent(&event);
  bmp.getTemperature(&temperature);
  double altitude = bmp.pressureToAltitude(1017,event.pressure,event.temperature);  

#if 1
  // Roll = X (frente/tras)
  //Serial.print(roll); Serial.print("\t");
  Serial.print(kalAngleX); Serial.print("\t");

  Serial.print("\t");

  // Pitch = Y (esquerda/direita)
  //Serial.print(pitch); Serial.print("\t");
  Serial.print(kalAngleY); Serial.print("\t");

  Serial.print("\t");
  // Yaw = Z (cima/baixo)
  //Serial.print(yaw); Serial.print("\t");
  Serial.print(kalAngleZ); Serial.print("\t");
#endif

#if 0
// In gauss
  Serial.print(accX / 16384.0); Serial.print("\t");
  Serial.print(accY / 16384.0); Serial.print("\t");
  Serial.print(accZ / 16384.0); Serial.print("\t");
// degrees/sec
  Serial.print(gyroXrate); Serial.print("\t");
  Serial.print(gyroYrate); Serial.print("\t");
  Serial.print(gyroZrate); Serial.print("\t");
// Compensated
  Serial.print(magX); Serial.print("\t");
  Serial.print(magY); Serial.print("\t");
  Serial.print(magZ); Serial.print("\t");
#endif

#if 0
  Serial.print(temperature); Serial.print("\t");
  Serial.print(event.pressure); Serial.print("\t");
  Serial.print(altitude); Serial.print("\t");
#endif

  Serial.println();
  delay(10);
}
