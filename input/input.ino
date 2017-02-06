#include <Bridge.h>
#include <Console.h>
#include <YunMessenger.h>

Messenger m;
int buttonState = 0;

void setup() {

    // start-up the bridge
    Bridge.begin();

    delay(2000);
    Console.begin();
    while (!Console) {
      ; // wait for Console port to connect.
    }

    Console.buffer(64);
//    delay(2000);
}

void loop() {
  buttonState = digitalRead(2);
  if (buttonState == HIGH) {
    m.send("button_pressed", "true");
    delay(1000);
  }
}
