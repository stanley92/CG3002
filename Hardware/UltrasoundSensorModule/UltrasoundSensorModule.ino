/*
HC-SR04 Ping sonar distance sensor]
VCC to arduino 5v GND to arduino GND
Echo to Arduino pin 10 Trig to Arduino pin 9
*/

#define trigger 9
#define echo 10

//returns value that corresponds to the distance of the detected object
int sonarValue(int trigPin, int echoPin)
{
  long duration;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  duration = duration / 59;
  if ((duration < 2) || (duration > 300)) return false;
  return duration;
}

void setup()
{
  digitalWrite( trigger , LOW );
  Serial.begin(9600);
}

void loop()
{
  float val = 0;
  val =  sonarValue( trigger , echo );
  Serial.println(val);
}

