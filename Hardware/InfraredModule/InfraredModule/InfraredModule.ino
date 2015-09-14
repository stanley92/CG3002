//Infrared Module
//  Noah Stahl
//  5/25/2011
//  http://arduinomega.blogspot.com
//  Arduino Mega 2560
//This sketch is used to test the Sharp Long Range Infrared Sensor.
//The sensor output is attached to analog pin 15. Once the distance
//is calculated, it is printed out to the serial monitor.

//The Sharp IR Range Finder works by the process of triangulation. 
//A pulse of light (wavelength range of 850nm +/-70nm) is emitted and then reflected back 
//(or not reflected at all). When the light returns it comes back at an angle that is
//dependent on the distance of the reflecting object. Triangulation works by detecting 
//this reflected beam angle - by knowing the angle, distance can then be determined. "

//note: this sensor is effective wwithin the range of 20cm - 150cm

#define sensorIR 15               //Must be an analog pin
float sensorValue, inches, cm;    //Must be of type float for pow()

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(sensorIR);
  //inches = 4192.936 * pow(sensorValue,-0.935) - 3.937;
  cm = 10650.08 * pow(sensorValue,-0.935) - 10;
  delay(100);
  //Serial.print("Inches: ");
  //Serial.println(inches);
  Serial.print("Cm: ");
  Serial.println(cm);
}
