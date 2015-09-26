/*
HC-SR04 Ping sonar distance sensor]
VCC to arduino 5v GND to arduino GND
Echo to Arduino pin 10 Trig to Arduino pin 9
*/

#include <NewPing.h>
#define TRIGGER_PIN  22  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     24  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.


#define ECHO_PIN2 38
#define TRIGGER_PIN2 39
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2,MAX_DISTANCE); //sensor2 
void setup() {
  Serial.begin(9600); // Open serial monitor at 9600 baud to see ping results.
}

void loop() {
  delay(50);                      // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
  Serial.print("Sonar 1: ");
  Serial.print(sonar.convert_cm(uS)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
  Serial.println("cm");
  
  Serial.print("Sonar 2: ");
  Serial.print(sonar2.convert_cm(uS));
  Serial.println("cm");
}
