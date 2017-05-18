#define trigPin 4
#define echoPin 3
#define led 2
#define led2 13

#define pendingLED 6
#define pendingButton 3
                                       
#include <Bridge.h>

char pending[10];
int in_pending = 0;

void setup() {
  Serial.begin (9600);

  memset(pending, 0, 10);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);

  pinMode(pendingLED, OUTPUT);

  digitalWrite(pendingLED, LOW);

  Serial.println("Starting");

  Bridge.begin();

  Serial.println("Started");

  blinkTwice();
}

void loop() {
  long duration, distance;

  int triggered;

  Bridge.get("pending", pending, 10);

  while (0 == strcmp(pending, "true")) {
    if (in_pending == 0) {
      Serial.println("pended");
      digitalWrite(pendingLED, HIGH);
      in_pending = 1;
    }
    triggered = loop_iteration("BP");
    if (triggered) {
      Serial.println("why");
      Bridge.put("pending", "false");
    }
    Bridge.get("pending", pending, 10);
    
  }
  in_pending = 0;
  digitalWrite(pendingLED, LOW);
  triggered = loop_iteration("BP");
}

int loop_iteration(String channel) {
  long duration, distance;
  int triggered = 0;

  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(trigPin, HIGH);
  //  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;
  if (distance < 10) {  // This is where the LED On/Off happens
    digitalWrite(led, HIGH); // When the Red condition is met, the Green LED should turn off
    Bridge.put(channel, "true");
    digitalWrite(led2, LOW);
    triggered = 1;
    delay(1000);
  }
  else {
    digitalWrite(led, LOW);
    digitalWrite(led2, HIGH);
  }
//  if (distance >= 200 || distance <= 0) {
////    Serial.println("Out of range");
//  }
//  else {
//    Serial.print(distance);
//    Serial.println(" cm");
//  }
  return triggered;
}

void blinkTwice() {
  for (int i = 0; i < 2; i++) {
    delay(500);
    digitalWrite(led2, LOW);
    delay(500);
    digitalWrite(led2, HIGH);
  }
}
