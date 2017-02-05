#include <Process.h>
#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>
//runShellCommandAsynchronously
BridgeServer server;
void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13, LOW);
  Bridge.begin();
  digitalWrite(13, HIGH);
  
 // run various example processes
// runPython();
}

void loop() {
  // Get clients coming from server
  BridgeClient client = server.accept();

  // There is a new client?
  if (client) {
    // Process request
    process(client);

    // Close connection and free resources.
    client.stop();
  }

  delay(50); // Poll every 50ms
}

void process(BridgeClient client) {
  // read the command
  String command = client.readStringUntil('/');

  // is "digital" command?
  if (command == "digital") {
    digitalCommand(client);
  }
}

void runPython(){
  Process p;
  p.runShellCommand("python /root/client.py");
  while (p.available()>0) {
    char c = p.read();
    Serial.print(c);
  }
  Serial.print("finished\n");
 // Ensure the last bit of data is sent.
 Serial.flush();
}

void runCurl() {
 // Launch "curl" command and get Arduino ascii art logo from the network
 // curl is command line program for transferring data using different internet protocols
 Process p; // Create a process and call it "p"
 p.begin("curl"); // Process that launch the "curl" command
 p.addParameter("http://arduino.cc/asciilogo.txt"); // Add the URL parameter to "curl"
 p.run(); // Run the process and wait for its termination

 // Print arduino logo over the Serial
 // A process output can be read with the stream methods
 while (p.available()>0) {
 char c = p.read();
 Serial.print(c);
 }
 // Ensure the last bit of data is sent.
 Serial.flush();
}

void digitalCommand(BridgeClient client) {
  int pin, value;

  // Read pin number
  pin = client.parseInt();

  // If the next character is a '/' it means we have an URL
  // with a value like: "/digital/13/1"
  if (client.read() == '/') {
    value = client.parseInt();
    digitalWrite(pin, value);
  } else {
    value = digitalRead(pin);
  }

  // Send feedback to client
  client.print(F("Pin D"));
  client.print(pin);
  client.print(F(" set to "));
  client.println(value);

  // Update datastore key with the current pin value
  String key = "D";
  key += pin;
  Bridge.put(key, String(value));
}
