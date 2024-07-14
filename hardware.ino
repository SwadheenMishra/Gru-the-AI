#include <Servo.h>

Servo myservo;

const int ledPin1 = 8;
const int servoPin = 9;
const int buzzerPin1 = 10;

int x;
int pos = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  myservo.attach(servoPin);

  pinMode(ledPin1, OUTPUT);
  pinMode(buzzerPin1, OUTPUT);
}

void  loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  
  if (x == 1){
      digitalWrite(ledPin1, HIGH);
  }
  else if (x == 0){
      digitalWrite(ledPin1, LOW);
  }
  else if (x == 3) {
    for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(1);                       // waits 15ms for the servo to reach the position
    }
    for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
    }
  }
  else if (x == 4){
    for (int i = 0; i < 10; i++){
      digitalWrite(buzzerPin1, HIGH);
      digitalWrite(ledPin1, HIGH);
      delay(500);
      digitalWrite(buzzerPin1, LOW);
      digitalWrite(ledPin1, LOW);
      delay(500);
    }
  }
}