//#include <Boards.h>
//#include <Firmata.h>

/*

This example show the interaction between the Ciao Library and the Thingspeak Cloud.
To run the example you need to register an account on thingspeak.com and create a
new channel by clicking "Channels" section in the website (Channels -> My Channels -> New Channel).
In the new channel you need to add two fields. The first one refers to the humidity data and the second one to the temperature value.
After that, replace the "XXXXXXXXX" value of APIKEY_THINGSPEAK with "Write API key" value reported in the API Keys section of the channel.

*/
#include <Wire.h>
#include <Ciao.h>

#define CONNECTOR     "rest"
#define SERVER_ADDR   "b8705ba2.ngrok.io"

#define APIKEY_THINGSPEAK  "PJK7BHBC97P8C1S9" //Insert your API Key

short hum = 60;
short temp = 22;
int buttonState = 0;
void setup() {

  Ciao.begin(); // CIAO INIT
  pinMode(13, OUTPUT);
}

void loop() {
    int newState = digitalRead(2);
    
    if (newState == HIGH) {
      buttonState = 1;
      String uri = "/api/board/" + String(buttonState);

      Ciao.println("Send data on ThingSpeak Channel");
  
      CiaoData data = Ciao.read(CONNECTOR, SERVER_ADDR, uri);
  
      if (!data.isEmpty()){
        Ciao.println( "State: " + String (data.get(1)) );
        Ciao.println( "Response: " + String (data.get(2)) );
        Ciao.println( "Button: " + String(digitalRead(2)));
  
      }
      else{
        Ciao.println("Write Error");
      }

    } else {
      delay(1000);
      buttonState = 0; 
    }
 
}
