#include <Bridge.h>

int buttonState = 0;

void setup() {
  // Bridge startup
  pinMode(13, OUTPUT);
  Bridge.begin();

  blinkTwice();

}

void loop() {
  buttonState = digitalRead(2);
  if (buttonState == HIGH) {
    Bridge.put("BP", "true"); // BP - Button Pressed
    delay(500);
  }
}


void blinkTwice() {
  for (int i = 0; i < 2; i++) {
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    digitalWrite(13, HIGH);
  }
}
