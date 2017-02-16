
#include <Bridge.h>

#include <LiquidCrystal.h>
#include <stdio.h>

// Here we will hold the values coming from Python via Bridge.
char D13value[255];
char D13valueOld[255];

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {

 lcd.begin(16, 2);
 // Zero out the memory we're using for the Bridge.19
 
 memset(D13value, 0, 255);
 memset(D13valueOld, 0, 255);

 // Initialize digital pins 12 and 13 as output.
 pinMode(13, OUTPUT);

 // Start using the Bridge.
 Bridge.begin();

 blinkTwice();
}

void loop() {

 Bridge.get("D13", D13value, 255);
 //Only update if new value is read from the bridge
 if ( strcmp(D13value, D13valueOld)) {
  memcpy(D13valueOld, D13value, 255);
  lcd.setCursor(0, 0);
  lcd.print(D13value);
 }

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

