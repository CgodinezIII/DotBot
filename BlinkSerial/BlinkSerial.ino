int line;
int X;
int Y;
int garbage;
int start = 0;
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(LED_BUILTIN, OUTPUT);
digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
while(Serial.available() > 0){
Serial.println("Send X");
  X = Serial.parseInt();
}
Serial.println(X);
Serial.println("Send Y");
while(Serial.available() > 0){
  Y = Serial.parseInt();
}
Serial.println(Y);
 */ 

while(Serial.available() > 0){
  delay(1000);
  garbage = Serial.parseInt();
  while(garbage == 1){
  Serial.println("Send New Coord");
  delay(2000);
  X = Serial.parseInt();
  Serial.println(X);
  Serial.println("Send Y");
  delay(2000);
  Y = Serial.parseInt();
  Serial.println(Y);
  
  
  if(X == 28){
  digitalWrite(LED_BUILTIN, HIGH);
  
}
else{
  digitalWrite(LED_BUILTIN, LOW);
}
}
}
}
