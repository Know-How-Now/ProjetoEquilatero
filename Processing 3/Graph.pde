/*====================[ GRAPH MPU6050 DATA ]====================*/
import processing.serial.*;
Serial serial;

/*[INCOMING SERIAL DATA]*/
String stringGyroX, stringGyroY;
String stringAccX, stringAccY;
String stringCompX, stringCompY;
String stringKalmanX, stringKalmanY;

final int width = 600;
final int height = 400;

/*[ARRAY OF CONVERTED DATA]*/
float[] gyroX = new float[600];
float[] gyroY = new float[600];

float[] accX = new float[600];
float[] accY = new float[600];

float[] compX = new float[600];
float[] compY = new float[600];

float[] kalmanX = new float[600];
float[] kalmanY = new float[600];

boolean drawValues  = false;

/*===[ MAIN SETUP ]===*/
void setup() {
  size(600, 400);
  serial = new Serial(this, Serial.list()[1], 115200); // Set this to your serial port obtained using the line above
  serial.bufferUntil('\n'); // Buffer until line feed
  
  // center all variables
  for (int i = 0; i < width; i++) {
    gyroX[i] = height/2;
    gyroY[i] = height/2;
    accX[i] = height/2;
    accY[i] = height/2;
    compX[i] = height/2;
    compY[i] = height/2;
    kalmanX[i] = height/2;
    kalmanY[i] = height/2;
  }

  drawGraph(); // Draw graph at startup
}

/*===[CHECK IF BLOCK OF DATA WAS SENT]===*/
void draw() {
  /* Draw Graph */
  if (drawValues) {
    drawValues = false;
    drawGraph();
  }
}

/*===[ DRAW GRAPH ]===*/
void drawGraph() {
  background(255); // White
  for (int i = 0; i < width/10; i++) {
    stroke(200); // Grey
    line((-frameCount%10)+i*10, 0, (-frameCount%10)+i*10, height);
    line(0, i*10, width, i*10);
  }

  stroke(0); // Black
  for (int i = 1; i <= 3; i++)
    line(0, height/4*i, width, height/4*i); // Draw line, indicating -90 deg, 0 deg and 90 deg

  convert();
  drawAxisX();
  drawAxisY();
}

/*===[ RECEIVE BLOCKS OF INCOMING DATA ]===*/
void serialEvent (Serial serial) {
  // Get the ASCII strings:
  stringAccX = serial.readStringUntil('\t');
  stringGyroX = serial.readStringUntil('\t');
  stringCompX = serial.readStringUntil('\t');
  stringKalmanX = serial.readStringUntil('\t');

  serial.readStringUntil('\t');

  stringAccY = serial.readStringUntil('\t');
  stringGyroY = serial.readStringUntil('\t');
  stringCompY = serial.readStringUntil('\t');
  stringKalmanY = serial.readStringUntil('\t');

  serial.clear(); // Clear buffer
  drawValues = true; // Draw the graph

  //printAxis();
}

/*===[ PRINT INCOMING DATA: DEBUGGING ]===*/
void printAxis() {
  print(stringGyroX);
  print(stringAccX);
  print(stringCompX);
  print(stringKalmanX);

  print('\t');

  print(stringGyroY);
  print(stringAccY);
  print(stringCompY);
  print(stringKalmanY);

  println();
}
