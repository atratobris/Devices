
#include <Bridge.h>

#include <LiquidCrystal.h>
#include <stdio.h>

// Here we will hold the values coming from Python via Bridge.
char D13value[255];
char D13valueOld[255];
char fittingString[17];
char test[] = "Hello world Hello world";
char testShort[] = "Hello world";
char *test_ptr; // Used to point to the text needed to be shown

const int loopDelay = 10; // chosen delay < 800
bool scrollStarted = false;
bool refreshLCD = true;
int loopIteration = 0;
int characterIndex = 0;

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {

 lcd.begin(16, 2);
 // Zero out the memory we're using for the Bridge.19
 memset(D13value, 0, 255);
 memset(D13valueOld, 0, 255);

 // Initialize digital pins 12 and 13 as output.
 pinMode(13, OUTPUT);
 test_ptr = testShort;
 // Start using the Bridge.
 Bridge.begin();
 blinkTwice();
}

void loop() {

 Bridge.get("LCD", D13value, 255);
 if ( 0 != strncmp(D13value, D13valueOld, 255)) {
  memcpy(D13valueOld, D13value, 255);
  test_ptr = D13value;
  scrollStarted = false;
  loopIteration = 0;
  characterIndex = 0;
  refreshLCD = true;
  lcd.noAutoscroll();
  lcd.clear();
 }
 //Only update if new value is read from the bridge
// lcd.print("Hello World Madame");
 if (scrollStarted) {
  if (loopIteration*loopDelay>=800) {
    loopIteration = 0;
    if ( characterIndex < strlen(test_ptr) ) {
      lcd.print(test_ptr[characterIndex]);
      characterIndex += 1;
    } else {
      lcd.noAutoscroll();
      lcd.clear();
      characterIndex = 0;
      scrollStarted = false;
    }
  } else {
    loopIteration += 1;
  }
 } else if (refreshLCD) {
   if (strlen(test_ptr) > 16) {
    strncpy(fittingString, test_ptr, 16);
    lcd.print(fittingString);
    lcd.autoscroll();
    scrollStarted = true;
    characterIndex = 16;
  } else {
    lcd.print(test_ptr);
    refreshLCD = false;
  }
 }


 // An arbitrary amount of delay to make the whole thing more reliable. YMMV
 delay(loopDelay);

}

void blinkTwice() {
  for (int i = 0; i < 2; i++) {
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    digitalWrite(13, HIGH);
  }
}

