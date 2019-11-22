#include <Stepper.h>

int inputSpeed = 10; //Speed 1-10 1 slow, 10 fast

const int stepX = 2;
const int stepY = 3;
const int Solenoid = 4;
const int dirX  = 5;
const int dirY  = 6;
const int enPin = 8;
const int xStop = 11;
const int yStop = 10;


const int CalibrationSpeed = 500; //1000
int Speed = int(1000 / inputSpeed);
int xCoord = 0;
int yCoord = 0;

int newxCoord = 0;
int newyCoord = 0;

const int gearTeeth = 60;
const int mmPerTooth = 2;
const int stepsPerRotation = 6400;
double stepsPerMM = stepsPerRotation / (gearTeeth*mmPerTooth);

int xDistance = 0;
int yDistance = 0;
int numStepsX = 0;
int numStepsY = 0;
int StartMessage = 0;
const int numCoords = 50;
int coords[numCoords][2];
bool notDone = true;

void setup() {
  //Open Serial Port
  Serial.begin(115200);

  // Sets pin modes
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(stepY, OUTPUT);
  pinMode(dirY, OUTPUT);
  pinMode(enPin, OUTPUT);
  pinMode(Solenoid, OUTPUT);
  pinMode(xStop, INPUT_PULLUP);
  pinMode(yStop, INPUT_PULLUP);
  digitalWrite(enPin, LOW);
  digitalWrite(dirX, HIGH);
  digitalWrite(dirY, HIGH);


  //Initiallize Dotter at 0,0
  initialize();
  delay(500);

}



void loop() {
  while (Serial.available() > 0) {
    //delay(1000);
    StartMessage = Serial.parseInt();
    while (StartMessage == 1) {

      while (digitalRead(xStop) == 1 && digitalRead(yStop) == 1 && notDone) {
        readData(); //coords = readData(coords);
        for (int i = 0; i < numCoords; i++) {
          newxCoord = coords[i][0];
          newyCoord = coords[i][1];
          //Set X motor Direction based on direction to next point
          if (newxCoord - xCoord < 0) {
            digitalWrite(dirX, HIGH);
          }
          else {
            digitalWrite(dirX, LOW);
          }

          //Calculate number of steps to go in the X direction
          xDistance = abs(newxCoord - xCoord);
          numStepsX = int(xDistance * stepsPerMM);

          //Move to new X-location
          moveX(numStepsX);

          //Set Y motor Direction based on direction to next point
          if (newyCoord - yCoord < 0) {
            digitalWrite(dirY, HIGH);
          }
          else {
            digitalWrite(dirY, LOW);
          }

          //Calculate number of steps to go in the Y direction
          yDistance = abs(newyCoord - yCoord);
          numStepsY = int(yDistance * stepsPerMM);

          //Move to new Y-Location
          moveY(numStepsY);
          //Activate Solenoid to Dot
          delay(200);
          digitalWrite(Solenoid, HIGH);
          delay(250);
          digitalWrite(Solenoid, LOW);


          //Send message to python that point complete
          //ADD CODE HERE

          //Set current Coords to newCoords
          xCoord = newxCoord;
          yCoord = newyCoord;
          //delay(1000);
        }
      }
    }
  }
}




void readData() {
  //int a[50][2];
  Serial.println("Send New Coords");
  for ( int i = 0; i < numCoords && notDone; i++ ) {
    for ( int j = 0; j < 2 && notDone; j++ ) {
      if (Serial.available() == 0) {
        notDone = false;
        break;
      }
      coords[ i ][ j ] = Serial.parseInt();
    }
    //  return a;
  }
}

void initialize() {
  while (digitalRead(xStop) == 1) {
    digitalWrite(dirX, HIGH);
    digitalWrite(stepX, HIGH);
    delayMicroseconds(CalibrationSpeed); //Adjust Delay for speed
    digitalWrite(stepX, LOW);
    delayMicroseconds(CalibrationSpeed);
  }
  while (digitalRead(xStop) == 0) {
    digitalWrite(dirX, LOW);
    digitalWrite(stepX, HIGH);
    delayMicroseconds(1000); //Adjust Delay for speed
    digitalWrite(stepX, LOW);
    delayMicroseconds(1000);
  }
  xCoord = 0;

  while (digitalRead(yStop) == 1) {
    digitalWrite(dirY, HIGH);
    digitalWrite(stepY, HIGH);
    delayMicroseconds(CalibrationSpeed);
    digitalWrite(stepY, LOW);
    delayMicroseconds(CalibrationSpeed);
  }
  while (digitalRead(yStop) == 0) {
    digitalWrite(dirY, LOW);
    digitalWrite(stepY, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepY, LOW);
    delayMicroseconds(1000);
  }
  yCoord = 0;
}

void moveX(int numStepsX) {
  for (int x = 0; x < numStepsX; x++) {
    if (digitalRead(xStop) == 1 && digitalRead(yStop) == 1) {
      digitalWrite(stepX, HIGH);
      delayMicroseconds(Speed);
      digitalWrite(stepX, LOW);
      delayMicroseconds(Speed);
    }
    else {
      exit(0);
    }
  }
}

void moveY(int numStepsY) {
  for (int x = 0; x < numStepsY; x++) {
    if (digitalRead(xStop) == 1 && digitalRead(yStop) == 1) {
      digitalWrite(stepY, HIGH);
      delayMicroseconds(Speed);
      digitalWrite(stepY, LOW);
      delayMicroseconds(Speed);
    }
    else {
      exit(0);
    }
  }
}
