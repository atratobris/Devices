#include <Wire.h>
#include <ArduinoWiFi.h>
/*
on your borwser, you type http://<IP>/arduino/webserver/ or http://<hostname>.local/arduino/webserver/
 
http://www.arduino.org/learning/tutorials/webserverblink
 
*/
void setup() {
    pinMode(13,OUTPUT);
    Wifi.begin();
    Wifi.println("WebServer Server is up"); 
}
void loop() {
 
    while(Wifi.available()){
      process(Wifi);
    }
  delay(50);
}
 
void process(WifiData client) {
  // read the command
  String command = client.readStringUntil('/');
 
  // is "digital" command?
  if (command == "webserver") {
    WebServer(client);
  }
 
  if (command == "digital") {
    digitalCommand(client);
  }
}
 
void WebServer(WifiData client) {
 
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println();
  client.println("<html>");
  
  client.println("<head> </head>");
  client.print("<body>");
  printPinValues(client);
  client.print("</body>");
  client.println("</html>");
  client.print(DELIMITER); // very important to end the communication !!! 
  client.flush();
}

String printPinValues(WifiData client) {
//  for (int i = 12; i <= 13; i++) {
  client.print("<pin number=\"");
  client.print(13);
  client.print("\">");
  client.print(digitalRead(13));
  client.print("</pin");
//  }
}

void digitalCommand(WifiData client) {
  int pin, value;
 
  // Read pin number
  pin = client.parseInt();
 
  // If the next character is a '/' it means we have an URL
  // with a value like: "/digital/13/1"
  if (client.read() == '/') {
    value = client.parseInt();
    digitalWrite(pin, value);
  }
  // Send feedback to client
  client.println("Status: 200 OK\n");
  client.print(F("Pin D"));
  client.print(pin);
  client.print(F(" set to "));
  client.print(value);
  client.print(EOL);    //char terminator
  client.print(DELIMITER);
}
