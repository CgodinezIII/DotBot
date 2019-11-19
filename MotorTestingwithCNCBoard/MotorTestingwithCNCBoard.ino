// defines pins numbers
#include <Stepper.h>

int inputSpeed = 5; //Speed 1-10 1 slow, 10 fast




const int stepX = 2;
const int stepY = 3;
const int Solenoid = 4;
const int dirX  = 5;
const int dirY  = 6;
const int enPin = 8;
const int xStop = 11;
const int yStop = 10;

int c;

const int CalibrationSpeed = 500; //1000
int Speed = int(1000/inputSpeed);
int xCoord = 0;
int yCoord = 0;

int newxCoord = 1;
int newyCoord = 1;

const int gearTeeth = 60;
const int mmPerTooth = 2;
const int stepsPerRotation = 6400;
double stepsPerMM = stepsPerRotation/(gearTeeth*mmPerTooth);

int xDistance = 0;
int yDistance = 0;
int numStepsX = 0;
int numStepsY = 0;


void setup() {
//Open Serial Port
  Serial.begin(9600);

// Sets pin modes
  pinMode(stepX,OUTPUT);
  pinMode(dirX,OUTPUT);
  pinMode(stepY,OUTPUT);
  pinMode(dirY,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(Solenoid,OUTPUT);
  pinMode(xStop, INPUT_PULLUP);
  pinMode(yStop, INPUT_PULLUP);
  digitalWrite(enPin,LOW);
  digitalWrite(dirX,HIGH);
  digitalWrite(dirY,HIGH);

  
//Initiallize Dotter at 0,0
  while(digitalRead(xStop) == 1){
    digitalWrite(dirX,HIGH);
    digitalWrite(stepX,HIGH);
    delayMicroseconds(CalibrationSpeed); //Adjust Delay for speed
    digitalWrite(stepX,LOW);
    delayMicroseconds(CalibrationSpeed);
  }
  while(digitalRead(xStop) == 0){
    digitalWrite(dirX,LOW);
    digitalWrite(stepX,HIGH);
    delayMicroseconds(1000); //Adjust Delay for speed
    digitalWrite(stepX,LOW);
    delayMicroseconds(1000);
  }
  xCoord = 0;
  
  while(digitalRead(yStop) == 1){
    digitalWrite(dirY,HIGH);
    digitalWrite(stepY,HIGH);
    delayMicroseconds(CalibrationSpeed);
    digitalWrite(stepY,LOW);
    delayMicroseconds(CalibrationSpeed);
  }
    while(digitalRead(yStop) == 0){
    digitalWrite(dirY,LOW);
    digitalWrite(stepY,HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepY,LOW);
    delayMicroseconds(1000);
  }
  yCoord = 0;
  delay(1000);
/*
//Read New x and Y coordinates
//ADD CODE HERE
     if(Serial.available() > 0) // If there is data to read
   {
   c = Serial.parseInt(); // Get a character

   delay(50);}
  newxCoord = c/2;
  newyCoord = c;
  
 */ 
 newxCoord = 3;
 newyCoord = 3;
}
void loop() {
while(digitalRead(xStop) == 1 && digitalRead(yStop) == 1){
//Set X motor Direction based on direction to next point
  if(newxCoord - xCoord < 0){
  digitalWrite(dirX,HIGH);
  }
  else{
  digitalWrite(dirX,LOW); 
  }

//Calculate number of steps to go in the X direction  
  xDistance = abs(newxCoord - xCoord);
  numStepsX = int(xDistance * stepsPerMM); 

//Move to new X-location
  for(int x = 0; x < numStepsX; x++) {
    if(digitalRead(xStop) == 1 && digitalRead(yStop) == 1){
    digitalWrite(stepX,HIGH);
    delayMicroseconds(Speed); //Adjust Delay for speed
    digitalWrite(stepX,LOW);
    delayMicroseconds(Speed); //Adjust Delay for speed
  }
  else{ 
    exit(0);
  }
  }

//Set Y motor Direction based on direction to next point
  if(newyCoord - yCoord < 0){
  digitalWrite(dirY,HIGH);
  }
  else{
  digitalWrite(dirY,LOW); 
  }
  
//Calculate number of steps to go in the Y direction
  yDistance = abs(newyCoord - yCoord);
  numStepsY = int(yDistance * stepsPerMM);

//Move to new Y-Location
  for(int x = 0; x < numStepsY; x++) {
    if(digitalRead(xStop) == 1 && digitalRead(yStop) == 1){
    digitalWrite(stepY,HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepY,LOW);
    delayMicroseconds(Speed);
   }
   else{ 
    exit(0);
  }
  }
//Activate Solenoid to Dot
  //ADD CODE HERE
  digitalWrite(Solenoid, HIGH);
  Serial.println("Solenoid Down");
  delay(500);
  digitalWrite(Solenoid, LOW);
  Serial.println("Solenoid");
  
  

//Send message to python that point complete
  //ADD CODE HERE

//Set current Coords to newCoords
  xCoord = newxCoord;
  yCoord = newyCoord;
  
  newxCoord = xCoord+10;
  newyCoord = yCoord+10;
 
/*
//Read New x and Y coordinates
  //ADD CODE HERE
     if(Serial.available() > 0) // If there is data to read
   {
   c = Serial.parseInt(); // Get a character

   delay(50);}
  newxCoord = c/2;
  newyCoord = c;
 */
 delay(1000);
 }
}
