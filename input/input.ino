#include <Bridge.h>
#include <Console.h>
#include <Process.h>
#include <YunMessenger.h>

Messenger m;
int buttonState = 0;
Process p;

void setup() {
  // Bridge startup
  pinMode(13, OUTPUT);
  Bridge.begin();
  delay(2000);
  Console.begin();
  while (!Console) {
    ; // wait for Console port to connect.
  }
  blinkTwice();
  Console.buffer(64);
  runPython();
}

void loop() {
  buttonState = digitalRead(2);
  if (buttonState == HIGH) {
    m.send("button_pressed", "true");
    delay(1000);
  }
}

void runPython(){
  p.runShellCommandAsynchronously("python /root/input.py");
  while (p.available()>0) {
    char c = p.read();
    Serial.print(c);
  }
  blinkTwice();
  Serial.print("finished\n");
  Serial.flush();
}

void blinkTwice() {
  for (int i = 0; i < 2; i++) {
    digitalWrite(13, LOW);
    delay(500);
    digitalWrite(13, HIGH);
  } 
}
