
#include <Bridge.h>
#include <stdio.h>

// Here we will hold the values coming from Python via Bridge.
char D12value[2];
char D13value[2];

void setup() {
 // Zero out the memory we're using for the Bridge.
 memset(D12value, 0, 2);
 memset(D13value, 0, 2);

 // Initialize digital pins 12 and 13 as output.
 pinMode(12, OUTPUT);
 pinMode(13, OUTPUT);

 // Start using the Bridge.
 Bridge.begin();

 blinkTwice();
}

void loop() {
 // Write current value of D12 to the pin (basically turning it on or off).
 Bridge.get("D12", D12value, 2);
 int D12int = atoi(D12value);
 digitalWrite(12, D12int);

 // An arbitrary amount of delay to make the whole thing more reliable. YMMV
 delay(10);

 // Write current value of D13 to the pin (basically turning it on or off).
 Bridge.get("D13", D13value, 2);
 int D13int = atoi(D13value);
 digitalWrite(13, D13int);

 // An arbitrary amount of delay to make the whole thing more reliable. YMMV
 delay(10);
}

void blinkTwice() {
  for (int i = 0; i < 2; i++) {
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    digitalWrite(13, HIGH);
  }
}
