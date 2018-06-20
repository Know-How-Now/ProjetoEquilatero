#include "Wire.h"
#include "MPU6050.h"
#include "HMC5883L.h"
#include "BMP085.h"
#include "Kalman.h"

// Create the Kalman instances
Kalman kalmanX, kalmanY, kalmanZ; 

// Sensors' objects
MPU6050 mpu;
HMC5883L compass;
BMP085 bmp;

// Default address'
const uint8_t MPU6050 = 0x68;
const uint8_t HMC5883L = 0x1E;
const uint8_t BMP085 = 0x77;

// Create variables: optional
int16_t tempRaw;

// Create variables: orientation + motion
// Used by: Kalman.h -- edit these variablles names'
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;
double magX, magY, magZ;

// Roll & Pitch use accelerometer to be calculated
//Yaw uses accelerometer to be calculated
double roll, pitch, yaw;

// Create variables: angles (gyro only, complementary filter, kalman filter)
double gyroXangle, gyroYangle, gyroZangle; 
double compAngleX, compAngleY, compAngleZ; 
double kalAngleX, kalAngleY, kalAngleZ;

// Buffer for I2C data
uint32_t timer;
uint8_t i2cData[14];

#define LED_PIN 13
bool blinkState = false;

#define RESTRICT_PITCH 

// Create variables: magnometer
// Used by: HMC5883L
#define MAG0MAX 603
#define MAG0MIN -578
#define MAG1MAX 542
#define MAG1MIN -701
#define MAG2MAX 547
#define MAG2MIN -556

float magOffset[3] = { (MAG0MAX + MAG0MIN) / 2, (MAG1MAX + MAG1MIN) / 2, (MAG2MAX + MAG2MIN) / 2 };
double magGain[3];

// Create variables: calibration
int16_t ax, ay, az,gx, gy, gz;
int mean_ax,mean_ay,mean_az,mean_gx,mean_gy,mean_gz,state=0;
int ax_offset,ay_offset,az_offset,gx_offset,gy_offset,gz_offset;

// Create variables: calibration
int buffersize=1000; //Amount of readings used to average, make it higher to get more precision but sketch will be slower  (default:1000)
int acel_deadzone=8; //Acelerometer error allowed, make it lower to get more precision, but sketch may not converge  (default:8)
int giro_deadzone=1; //Giro error allowed, make it lower to get more precision, but sketch may not converge  (default:1)

//==============================[ KALMAN FILTER ]==============================//
const uint16_t I2C_TIMEOUT = 1000;

uint8_t i2cWrite(uint8_t address, uint8_t registerAddress, uint8_t data, bool sendStop) {
  return i2cWrite(address, registerAddress, &data, 1, sendStop); // Returns 0 on success
}

uint8_t i2cWrite(uint8_t address, uint8_t registerAddress, uint8_t *data, uint8_t length, bool sendStop) {
  Wire.beginTransmission(address);
  Wire.write(registerAddress);
  Wire.write(data, length);
  uint8_t rcode = Wire.endTransmission(sendStop); // Returns 0 on success
  if (rcode) {
    Serial.print(F("i2cWrite failed: "));
    Serial.println(rcode);
  }
  return rcode; // See: http://arduino.cc/en/Reference/WireEndTransmission
}

uint8_t i2cRead(uint8_t address, uint8_t registerAddress, uint8_t *data, uint8_t nbytes) {
  uint32_t timeOutTimer;
  Wire.beginTransmission(address);
  Wire.write(registerAddress);
  uint8_t rcode = Wire.endTransmission(false); // Don't release the bus
  if (rcode) {
    Serial.print(F("i2cRead failed: "));
    Serial.println(rcode);
    return rcode; // See: http://arduino.cc/en/Reference/WireEndTransmission
  }
  Wire.requestFrom(address, nbytes, (uint8_t)true); // Send a repeated start and then release the bus after reading
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
        return 5; // This error value is not already taken by endTransmission
      }
    }
  }
  return 0; // Success
}

void setup() {
  // Wait for sensors to get ready
  delay(100);
  Serial.begin(115200);
  Wire.begin();
  TWBR = ((F_CPU / 400000L) - 16) / 2; // Set I2C frequency to 400kHz
  
  mpu.setI2CMasterModeEnabled(false);
  mpu.setI2CBypassEnabled(true) ;
  mpu.setSleepEnabled(false);
 
  // initialize device
  mpu.initialize();
  delay(100);
  bmp.initialize();
  
  // reset offsets
  mpu.setXAccelOffset(0);
  mpu.setYAccelOffset(0);
  mpu.setZAccelOffset(0);
  mpu.setXGyroOffset(0);
  mpu.setYGyroOffset(0);
  mpu.setZGyroOffset(0);
  
  runCalibration();
  
  i2cData[0] = 7; // Set the sample rate to 1000Hz - 8kHz/(7+1) = 1000Hz
  i2cData[1] = 0x00; // Disable FSYNC and set 260 Hz Acc filtering, 256 Hz Gyro filtering, 8 KHz sampling
  i2cData[2] = 0x00; // Set Gyro Full Scale Range to ±250deg/s
  i2cData[3] = 0x00; // Set Accelerometer Full Scale Range to ±2g
  
  while (i2cWrite(MPU6050, 0x19, i2cData, 4, false)); // Write to all four registers at once
  while (i2cWrite(MPU6050, 0x6B, 0x01, true)); // PLL with X axis gyroscope reference and disable sleep mode
  
  while (i2cRead(MPU6050, 0x75, i2cData, 1));
  if (i2cData[0] != 0x68) {
    Serial.print(F("Error reading sensor"));
    while (1);
  }
  
  while (i2cWrite(HMC5883L, 0x02, 0x00, true)); // Configure device for continuous mode
  calibrateMag();
  delay(100);
  
  /* Set kalman and gyro starting angle */
  updateMPU6050();
  updateHMC5883L();
  updatePitchRoll();
  updateYaw();

  // Set starting angle
  kalmanX.setAngle(roll);
  gyroXangle = roll;
  compAngleX = roll;

  kalmanY.setAngle(pitch);
  gyroYangle = pitch;
  compAngleY = pitch;

  kalmanZ.setAngle(yaw);
  gyroZangle = yaw;
  compAngleZ = yaw;

  bmp.loadCalibration();
  timer = micros();
}

void loop() {
  updateMPU6050();
  updateHMC5883L();

  double dt = (double)(micros() - timer) / 1000000; // Calculate delta time

  updatePitchRoll();
  double gyroXrate = gyroX / 131.0;
  double gyroYrate = gyroY / 131.0;

// Fix accelerometer angle jumps between -180 and 180 degrees
#ifdef RESTRICT_PITCH
  if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
    kalmanX.setAngle(roll);
    compAngleX = roll;
    kalAngleX = roll;
    gyroXangle = roll;
  } else // Calculate the angle using a Kalman filter
    kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt);
    
   // Invert rate, so it fits the restricted accelerometer reading
  if (abs(kalAngleX) > 90)
    gyroYrate = -gyroYrate;
  kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt);
#else
  if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
    kalmanY.setAngle(pitch);
    compAngleY = pitch;
    kalAngleY = pitch;
    gyroYangle = pitch;
  } else
    kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt); // Calculate the angle using a Kalman filter
  
  // Invert rate, so it fits the restricted accelerometer reading
  if (abs(kalAngleY) > 90)
    gyroXrate = -gyroXrate;
  // Calculate the angle using a Kalman filter
  kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt);
#endif

  updateYaw();
  double gyroZrate = gyroZ / 131.0; // Convert to deg/s
  // This fixes the transition problem when the yaw angle jumps between -180 and 180 degrees
  if ((yaw < -90 && kalAngleZ > 90) || (yaw > 90 && kalAngleZ < -90)) {
    kalmanZ.setAngle(yaw);
    compAngleZ = yaw;
    kalAngleZ = yaw;
    gyroZangle = yaw;
  } else
    kalAngleZ = kalmanZ.getAngle(yaw, gyroZrate, dt); // Calculate the angle using a Kalman filter
   
  /* Estimate angles using gyro only */
  // Calculate gyro angle without any filter
  //gyroXangle += gyroXrate * dt;
  //gyroYangle += gyroYrate * dt;
  //gyroZangle += gyroZrate * dt;
  // Calculate gyro angle using the unbiased rate from the Kalman filter
  gyroXangle += kalmanX.getRate() * dt; 
  gyroYangle += kalmanY.getRate() * dt;
  gyroZangle += kalmanZ.getRate() * dt;

  /* Estimate angles using complimentary filter */
  compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll;
  compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;
  compAngleZ = 0.93 * (compAngleZ + gyroZrate * dt) + 0.07 * yaw;

  // Reset the gyro angles when they has drifted too much
  if (gyroXangle < -180 || gyroXangle > 180)
    gyroXangle = kalAngleX;
  if (gyroYangle < -180 || gyroYangle > 180)
    gyroYangle = kalAngleY;
  if (gyroZangle < -180 || gyroZangle > 180)
    gyroZangle = kalAngleZ;
    
#if 1
  // Roll = X (frente/tras)
  Serial.print(roll); Serial.print("\t");
  //Serial.print(gyroXangle); Serial.print("\t");
  //Serial.print(compAngleX); Serial.print("\t");
  Serial.print(kalAngleX); Serial.print("\t");

  Serial.print("\t");
  // Pitch = Y (esquerda/direita)
  Serial.print(pitch); Serial.print("\t");
  //Serial.print(gyroYangle); Serial.print("\t");
  //Serial.print(compAngleY); Serial.print("\t");
  Serial.print(kalAngleY); Serial.print("\t");

  Serial.print("\t");
  // Yaw = Z (cima/baixo)
  Serial.print(yaw); Serial.print("\t");
  //Serial.print(gyroZangle); Serial.print("\t");
  //Serial.print(compAngleZ); Serial.print("\t");
  Serial.print(kalAngleZ); Serial.print("\t");
#endif

#if 0 // Set to 1 to print the IMU data
  // Converted into g's
  Serial.print(accX / 16384.0); Serial.print("\t");
  Serial.print(accY / 16384.0); Serial.print("\t");
  Serial.print(accZ / 16384.0); Serial.print("\t");

  // Converted into degress per second
  Serial.print(gyroXrate); Serial.print("\t");
  Serial.print(gyroYrate); Serial.print("\t");
  Serial.print(gyroZrate); Serial.print("\t");

  // After gain and offset compensation
  Serial.print(magX); Serial.print("\t");
  Serial.print(magY); Serial.print("\t");
  Serial.print(magZ); Serial.print("\t");
#endif

#if 1 // Set to 1 to print the temperature
  Serial.print("\t");
  double temperature2 = tempRaw / 340.0 + 36.53;
  double temperature = bmp.getTemperatureC(); //Get the temperature, bmp180ReadUT MUST be called first
  double pressure = bmp.getPressure();//Get the temperature
  double altitude = bmp.getAltitude(pressure); //Uncompensated caculation - in Meters
  double atm = pressure / 101325;
  //Serial.print(temperature2); Serial.print("\t");
  Serial.print(pressure); Serial.print("t");
  Serial.print(temperature); Serial.print("\t");
  Serial.print(altitude); Serial.print("\t");
  //Serial.print(atm); Serial.print("\t");
#endif
  Serial.println();
  delay(10);
}

//==============================[ CALIBRATION ]==============================//
void meansensors(){
  long i=0, buff_ax=0, buff_ay=0, buff_az=0, buff_gx=0, buff_gy=0, buff_gz=0;

  while (i < (buffersize + 101)){
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    if (i > 100 && i <= (buffersize+100)){ //First 100 measures are discarded
      buff_ax=buff_ax+ax;
      buff_ay=buff_ay+ay;
      buff_az=buff_az+az;
      buff_gx=buff_gx+gx;
      buff_gy=buff_gy+gy;
      buff_gz=buff_gz+gz;
    }
    if (i == (buffersize+100)){
      mean_ax=buff_ax/buffersize;
      mean_ay=buff_ay/buffersize;
      mean_az=buff_az/buffersize;
      mean_gx=buff_gx/buffersize;
      mean_gy=buff_gy/buffersize;
      mean_gz=buff_gz/buffersize;
    }
    i++;
    delay(2); //Needed so we don't get repeated measures
  }
}

void calibration(){
  ax_offset=-mean_ax/8;
  ay_offset=-mean_ay/8;
  az_offset=(16384-mean_az)/8;
 
  gx_offset=-mean_gx/4;
  gy_offset=-mean_gy/4;
  gz_offset=-mean_gz/4;
  while (1){
    int ready = 0;
    mpu.setXAccelOffset(ax_offset);
    mpu.setYAccelOffset(ay_offset);
    mpu.setZAccelOffset(az_offset);
 
    mpu.setXGyroOffset(gx_offset);
    mpu.setYGyroOffset(gy_offset);
    mpu.setZGyroOffset(gz_offset);

    meansensors();
    
    if (abs(mean_ax) <= acel_deadzone) ready++;
    else ax_offset = ax_offset - mean_ax/acel_deadzone;

    if (abs(mean_ay) <= acel_deadzone) ready++;
    else ay_offset = ay_offset - mean_ay/acel_deadzone;

    if (abs(16384-mean_az) <= acel_deadzone) ready++;
    else az_offset = az_offset + (16384-mean_az)/acel_deadzone;

    if (abs(mean_gx) <= giro_deadzone) ready++;
    else gx_offset = gx_offset - mean_gx/(giro_deadzone+1);

    if (abs(mean_gy) <= giro_deadzone) ready++;
    else gy_offset = gy_offset-mean_gy/(giro_deadzone+1);

    if (abs(mean_gz) <= giro_deadzone) ready++;
    else gz_offset = gz_offset-mean_gz/(giro_deadzone+1);

    if (ready==6) break;
  }
}

void runCalibration() {
  if (state==0){
    meansensors();
    state++;
    delay(1000);
  }
  if (state==1){
    calibration();
    state++;
    delay(1000);
  }
  if (state==2){
    meansensors();
  }
}

void updateMPU6050(){
  while (i2cRead(MPU6050, 0x3B, i2cData, 14));
  // Get accelerometer and gyroscope values
  accX = (int16_t)((i2cData[0] << 8) | i2cData[1]);
  accY = (int16_t)((i2cData[2] << 8) | i2cData[3]);
  accZ = (int16_t)((i2cData[4] << 8) | i2cData[5]);
  tempRaw = (int16_t)((i2cData[6] << 8) | i2cData[7]);
  gyroX = (int16_t)((i2cData[8] << 8) | i2cData[9]);
  gyroY = (int16_t)((i2cData[10] << 8) | i2cData[11]);
  gyroZ = (int16_t)((i2cData[12] << 8) | i2cData[13]);
}

void updateHMC5883L() {
  while (i2cRead(HMC5883L, 0x03, i2cData, 6));
  // Get magnetometer values
  magX = (int16_t)((i2cData[0] << 8) | i2cData[1]);
  magZ = (int16_t)((i2cData[2] << 8) | i2cData[3]);
  magY = (int16_t)((i2cData[4] << 8) | i2cData[5]);
}
void updatePitchRoll() {
#ifdef RESTRICT_PITCH
  double roll = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else
  double roll = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
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
  yaw = atan2(-Bfy, Bfx) * RAD_TO_DEG;

  yaw *= -1;
}

void calibrateMag() { 
  i2cWrite(HMC5883L, 0x00, 0x11, true);
  delay(100);
  updateHMC5883L(); // Read positive bias values

  int16_t magPosOff[3] = { magX, magY, magZ };

  i2cWrite(HMC5883L, 0x00, 0x12, true);
  delay(100); // Wait for sensor to get ready
  updateHMC5883L(); // Read negative bias values

  int16_t magNegOff[3] = { magX, magY, magZ };

  i2cWrite(HMC5883L, 0x00, 0x10, true); // Back to normal

  magGain[0] = -2500 / double(magNegOff[0] - magPosOff[0]);
  magGain[1] = -2500 / double(magNegOff[1] - magPosOff[1]);
  magGain[2] = -2500 / double(magNegOff[2] - magPosOff[2]);

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
