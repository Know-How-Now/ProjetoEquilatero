/*====================[ CONVERT INCOMING SERIAL DATA ]====================*/

// Create variables: angles
final int minAngle = -180;
final int maxAngle = 180;

// Convert serial data from 'ASCii_string' to 'float':
  // Steps: if != null > 'trim' (whitespace) > convert to 'float' > map to 'height' > save
void convert() {
  /* Gyro: x-axis */
  if (stringGyroX != null) { // Check if null value
    stringGyroX = trim(stringGyroX); // Trim
    gyroX[gyroX.length - 1] = map(float(stringGyroX), minAngle, maxAngle, 0, height); // Convert > map > save
  }

  /* Gyro: y-axis */
  if (stringGyroY != null) {
    stringGyroY = trim(stringGyroY);
    gyroY[gyroY.length - 1] = map(float(stringGyroY), minAngle, maxAngle, 0, height);
  }

  /* Accelerometer: x-axis */
  if (stringAccX != null) {
    stringAccX = trim(stringAccX);
    accX[accX.length - 1] = map(float(stringAccX), minAngle, maxAngle, 0, height);
  }

  /* Accelerometer: y-axis */
  if (stringAccY != null) {
    stringAccY = trim(stringAccY);
    accY[accY.length - 1] = map(float(stringAccY), minAngle, maxAngle, 0, height); 
  }

  /* Complementary filter: y-axis */
  if (stringCompX != null) {
    stringCompX = trim(stringCompX);
    compX[compX.length - 1] = map(float(stringCompX), minAngle, maxAngle, 0, height);
  }

  /* Complementary filter: x-axis */
  if (stringCompY != null) {
    stringCompY = trim(stringCompY);
    compY[compY.length - 1] = map(float(stringCompY), minAngle, maxAngle, 0, height); 
  }

  /* Kalman filter: x-axis */
  if (stringKalmanX != null) {
    stringKalmanX = trim(stringKalmanX);
    kalmanX[kalmanX.length - 1] = map(float(stringKalmanX), minAngle, maxAngle, 0, height);
  }

  /* Kalman filter: y-axis */
  if (stringKalmanY != null) {
    stringKalmanY = trim(stringKalmanY);
    kalmanY[kalmanY.length - 1] = map(float(stringKalmanY), minAngle, maxAngle, 0, height);
  }
}
