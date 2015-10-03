//AccelerometerCompassModule
//ACHeading
#include <Wire.h>
#include <LSM303.h>
#include <Keypad.h>
#include <LPS.h>
#include <L3G.h>
#include <NewPing.h>


LSM303 compass;
LPS ps;
L3G gyro;

#define MOTOR 52
#define TRIGGER_PIN  22  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     24  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
//#define ECHO_PIN2 38
//#define TRIGGER_PIN2 39
//NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
//NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2,MAX_DISTANCE); //sensor2 
int maximumRange = 200; // Maximum range needed
int minimumRange = 0; // Minimum range needed
long duration, distance; // Duration used to calculate distance


#define sensorIR 15  //Must be an analog pin A15
float distFromStart=0;
int step=0;
long newTime=0;
long deltaTime=0;
long oldTime=0;
long oldXaVal=0;
long oldDis=0;
long oldVelocity=0;
float sensorValue, cm;    //Must be of type float for pow()

/*********************** 
keypad setting
pin 30 - 36
************************/
const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

//row and col are adjustable
byte rowPins[ROWS] = {33, 32, 31, 30}; //connect to the row pinouts of the keypad;
byte colPins[COLS] = {36, 35, 34}; //connect to the column pinouts of the keypad;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );





void setup() {
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
  ps.enableDefault();
  gyro.init();
  gyro.enableDefault();
  pinMode(MOTOR, OUTPUT);
   pinMode(TRIGGER_PIN, OUTPUT);
 pinMode(ECHO_PIN, INPUT);
  /*
  Calibration values; the default values of +/-32767 for each axis
  lead to an assumed magnetometer bias of 0. Use the ACCalibrate 
  program to determine appropriate values for your particular unit.
  */
  //compass.m_min = (LSM303::vector<int16_t>){-32767, -32767, -32767};
  //compass.m_max = (LSM303::vector<int16_t>){+32767, +32767, +32767};
  
  //LSM303::vector<int16_t> running_min = {-2872, -3215, -1742}, running_max = {+3019, +3108, +3570}; //calibration init data for compass 
  compass.m_min = (LSM303::vector<int16_t>){-2872, -3215, -1742};
  compass.m_max = (LSM303::vector<int16_t>) {+3019, +3108, +3570};

}

void loop() {

  
  
  /***********************************
  **        reading sensors
  ************************************/
  compass.read();
  float heading = compass.heading();
  float XaVal, YaVal, ZaVal, fXa, fYa,fZa, pitch, roll,pitch_print, roll_print;
  const float alpha = 0.15;
  XaVal = compass.a.x/16.0; //Acceleration data registers contain a left-aligned 12-bit number, so values should be shifted right by 4 bits (divided by 16)
  YaVal = compass.a.y/16.0; //unit is in cm/s2
  ZaVal = compass.a.z/16.0;
  /*
   
  /***********************************
  **       keypad
  ************************************/
  char key = keypad.getKey();

  //print out the key that is pressed 
  if (key != NO_KEY){
    Serial.print("You have pressed ");
    Serial.println(key);
  }

  /***********************************
  **       altitude
  ************************************/
  float pressure = ps.readPressureMillibars() + 248.5;
  float altitude = ps.pressureToAltitudeMeters(pressure);
  
  Serial.print("Pressure is ");
  Serial.print(pressure);
  Serial.println(" mbar");
  Serial.print("Altitude is ");
  Serial.print(altitude);
  Serial.println(" m.");
  
  /******************************************************
  **  gyro meter reading
  ******************************************************/
  gyro.read();
  Serial.println("Gyro meter ");
  Serial.print("X: ");
  Serial.print((int)gyro.g.x * 8.75 /1000);
  Serial.println(" degree/second");
  Serial.print("Y: ");
  Serial.print((int)gyro.g.y * 8.75 /1000);
  Serial.println(" degree/second");
  Serial.print("Z: ");
  Serial.print((int)gyro.g.z * 8.75 /1000);
  Serial.println(" degree/second");
  Serial.println("");




 /*******************************************************************
                          get Headings
  When given no arguments, the heading() function returns the angular
  difference in the horizontal plane between a default vector and
  north, in degrees.
  /*
  When given no arguments, the heading() function returns the angular
  difference in the horizontal plane between a default vector and
  north, in degrees.
  
  The default vector is chosen by the library to point along the
  surface of the PCB, in the direction of the top of the text on the
  silkscreen. This is the +X axis on the Pololu LSM303D carrier and
  the -Y axis on the Pololu LSM303DLHC, LSM303DLM, and LSM303DLH
  carriers.
  
  To use a different vector as a reference, use the version of heading()
  that takes a vector argument; for example, use
  
    compass.heading((LSM303::vector<int>){0, 0, 1});
  
  to use the +Z axis as a reference.
  
  *******************************************************************/
  String direction = "";
  if(heading>=340 || heading <= 20)
    direction = "North";
  else if (heading>=70 && heading <= 110)
    direction = "East";
    else if (heading>=160 && heading <= 200)
    direction = "South";
    else if (heading>=250 && heading <= 290)
    direction = "West";
    
    
    else if (heading>20 && heading < 70)
    direction = "North East";
    else if (heading>110 && heading < 160)
    direction = "South East";
    else if (heading>200 && heading < 250)
    direction = "South West";
    else if (heading>290 && heading < 340)
    direction = "North West";
  
  Serial.print("Heading is ");
  Serial.println(direction);
  //Serial.println("degree.");
 
 
 /******************************************************
  **  Method 1 to calculate distance: using steps
  ******************************************************/
 
  // a step and  distance using Z-ACCELERATION
  if(ZaVal<-965){
    distFromStart+=33;  //1 step is 33 cm
    step++; 
  } 

  
  Serial.print("X accel is ");Serial.print(XaVal); Serial.print(" cm/s2"); Serial.println(" "); 
  Serial.print("Y accel is ");Serial.print(YaVal); Serial.print(" cm/s2"); Serial.println(" "); 
  Serial.print("Z accel is ");Serial.print(ZaVal);Serial.print(" cm/s2"); Serial.println(" "); 
   
 
  Serial.print("1. You have walked ");
  Serial.print(step);
  Serial.print(" steps and distance is ");
  Serial.print(distFromStart);
  Serial.println(" cm from start");
  
 /******************************************************
  **  pitch and roll
  ******************************************************/
    // Low-Pass filter accelerometer
  fXa = XaVal * alpha + (fXa * (1.0 - alpha));
  fYa = YaVal * alpha + (fYa * (1.0 - alpha));
  fZa = ZaVal * alpha + (fZa * (1.0 - alpha));

  Serial.print("Low pass X accel is ");Serial.print(fXa); Serial.print(" cm/s2"); Serial.println(" "); 
  Serial.print("Low pass Y accel is ");Serial.print(fYa); Serial.print(" cm/s2"); Serial.println(" "); 
  Serial.print("Low pass Z accel is ");Serial.print(fZa);Serial.print(" cm/s2"); Serial.println(" ");    
    
  roll  = atan2(fYa, sqrt(fXa*fXa + fZa*fZa));
  pitch = atan2(fXa, sqrt(fYa*fYa + fZa*fZa));
  
  roll_print = roll*180.0/M_PI;
  pitch_print = pitch*180.0/M_PI;
  Serial.print("pitch(Y) is ");
  Serial.print(pitch_print);
  Serial.println("degree ");

  Serial.print("roll(X) is ");
  Serial.print(roll_print);
  Serial.println("degree ");
  
 /******************************************************
  **  Method 2 to calculate distance: using accelerations
  ******************************************************/
  newTime = millis();
  deltaTime = newTime - oldTime;
  
   XaVal = XaVal - (1000 * (sin(pitch)));//offsetting pitch 
  
  // estimate the average acceleration since the previous sample, by averaging the two samples
  long avgAccel = (oldXaVal + XaVal) / 2;
  
  //if ((XaVal < 50 && XaVal > -50) && (oldXaVal < 50 && oldXaVal > -50)) 
  //  avgAccel = 0;
  
 
  
  Serial.print("the avgAccel is ");
  Serial.print(avgAccel);
  Serial.println(" cm/s2");
  // integrate the average accel and add it to the previous speed to calculate the new speed
  long newVelocity = oldVelocity + (avgAccel  * deltaTime/1000);
 
   
  //estimate the average speed since the previous sample, by averaging the two speeds
  long avgVelocity = (oldVelocity + newVelocity) / 2;
  
  //  if ((XaVal < 50 && XaVal > -50) && (oldXaVal < 50 && oldXaVal > -50)) 
  //  avgVelocity = 0;
  
  
  // integrate the average speed and add it to the previous displacement to get the new displacement
  long newDisplacement = oldDis + (avgVelocity * deltaTime/1000);
  
  oldTime = newTime;
  oldVelocity = newVelocity ;
  oldDis = newDisplacement;
  oldXaVal = XaVal;
  Serial.print("2. You have walked ");
  Serial.print(newDisplacement);
  Serial.println("cm from start");  
   


  /******************************************************
  **  IR sensor meter reading
  ******************************************************/
  sensorValue = analogRead(sensorIR);
  cm = 10650.08 * pow(sensorValue,-0.935) - 10;
  Serial.print("IR sensor reads ");
  Serial.print(cm);
  Serial.println(" Cm");
  
  
  
    /***********************************
  **        reading sensors
  ************************************/
  /*
  //digitalWrite(ECHO_PIN2 ,LOW);
  unsigned int uS2 = sonar2.ping();

  
  Serial.print("Sonar 2: ");
  Serial.print(sonar2.convert_cm(uS2));
  Serial.println("cm");

    if(sonar2.convert_cm(uS2)<50){
    digitalWrite(MOTOR, HIGH);     // waits for a second
        // sets the LED off
    //delay(1000);                  // waits for a second
  }
  else{
   digitalWrite(MOTOR, LOW);
  }
  //delay(100);
*/
/* The following trigPin/echoPin cycle is used to determine the
 distance of the nearest object by bouncing soundwaves off of it. */ 
 digitalWrite(TRIGGER_PIN, LOW); 
 delayMicroseconds(2); 

 digitalWrite(TRIGGER_PIN, HIGH);
 delayMicroseconds(10); 
 
 digitalWrite(TRIGGER_PIN, LOW);
 duration = pulseIn(ECHO_PIN, HIGH);
 
 //Calculate the distance (in cm) based on the speed of sound.
 distance = duration/58.2;
 Serial.print("sonar distance is ");
 Serial.println(distance);
 Serial.println();
 if (distance >= 10 && distance <= 70){
 /* Send a negative number to computer and Turn LED ON 
 to indicate "out of range" */
 //Serial.println("-1");
 digitalWrite(MOTOR, HIGH); 
 }
 else {
 /* Send the distance to the computer using Serial protocol, and
 turn LED OFF to indicate successful reading. */
 //Serial.println(distance);
 digitalWrite(MOTOR, LOW); 
 }
 
 //Delay 50ms before next reading.
 delay(50);

}
