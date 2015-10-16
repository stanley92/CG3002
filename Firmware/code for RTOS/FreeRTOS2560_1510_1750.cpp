/*
 * FreeRTOS2560.cpp
 *
 * Created: 20/9/2015 10:59:40 PM
 *  Author: Laksh
 */ 
/*

#include <avr/io.h>
#include <FreeRTOS.h>
#include <task.h>
#include <Arduino.h>

void task1(void *p)
{
	while(1)
	{
		
		digitalWrite(12,HIGH);
		vTaskDelay(500);
		digitalWrite(12,LOW);
		vTaskDelay(500);
	}
}

void task2(void *p)
{
	while(1)
	{
		
		digitalWrite(13,HIGH);
		vTaskDelay(250);
		digitalWrite(13,LOW);
		vTaskDelay(250);
	}
}
#define STACK_DEPTH 64

void vApplicationIdleHook()
{
	
}

int main(void)
{
   init();
   pinMode(13,HIGH);
   while(1)
   {
	   
	   digitalWrite(13,HIGH);
	   vTaskDelay(250);
	   digitalWrite(13,LOW);
	   vTaskDelay(250);
   }
   */
   
   /*pinMode(12,OUTPUT);
   pinMode(13,OUTPUT);
   TaskHandle_t t1,t2;
   
   //Create Tasks
   xTaskCreate(task1,"Task 1", STACK_DEPTH, NULL, 6, &t1);
   xTaskCreate(task2,"Task 2", STACK_DEPTH, NULL, 5, &t2);
   
   vTaskStartScheduler();*/
//}

/*
 * FreeRTOS2560.cpp
 *
 * Created: 9/9/2015 11:16:44 PM
 *  Author: Laksh
 */ 
/*

#include <avr/io.h>

int main(void)
{
    while(1)
    {
        //TODO:: Please write your application code 
    }
}*/

#include <avr/io.h>
#include <FreeRTOS.h>
#include <task.h>
#include <Arduino.h>
#include <Keypad.h>
#include <serial.h>
#include <NewPing.h>
//#include <stdarg.h>

/*baro code*/
#include <LPS.h>
/*baro code*/

/*accelerometer code*/
#include <LSM303.h>
/*accelerometer code*/

/*gyro code*/
#include <Wire.h>
#include <L3G.h>
#include <math.h>
/*gyro code*/

LSM303 compass;
LPS ps;
L3G gyro;


#define MOTOR 52


#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define ECHO_PIN    42  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define ECHO_PIN2	36	
#define ECHO_PIN3	39
#define ECHO_PIN4	44
#define ECHO_PIN5	6
#define TRIGGER_PIN  41  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define TRIGGER_PIN2 37
#define TRIGGER_PIN3 40
#define TRIGGER_PIN4 43
#define TRIGGER_PIN5 7
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2,MAX_DISTANCE); //sensor2
NewPing sonar3(TRIGGER_PIN3, ECHO_PIN3, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar4(TRIGGER_PIN4, ECHO_PIN4,MAX_DISTANCE); //sensor2
NewPing sonar5(TRIGGER_PIN5, ECHO_PIN5, MAX_DISTANCE); // NewPing setup of pins and maximum distance.



#define ID_DATA_KEYPAD	0
#define ID_DATA_HEADING	1
#define ID_DATA_DIST	2
#define ID_DATA_SONAR1	3
#define ID_DATA_SONAR2  4
#define ID_DATA_SONAR3  5
#define ID_DATA_SONAR4	6
#define ID_DATA_SONAR5	7

#define ID_DATA_SONAR6	8

#define DATA_MAX_SIZE 9


#define sensorIR 15  //Must be an analog pin A15
float distFromStart=0;
int step=0;

int taskDelay = 50;

int data[DATA_MAX_SIZE];

/*
long newTime=0;
long deltaTime=0;
long oldTime=0;
long oldXaVal=0;
long oldDis=0;
long oldVelocity=0;*/
float sensorValue, cm;    //Must be of type float for pow()

int maximumRange = 200; // Maximum range needed
int minimumRange = 0; // Minimum range needed
float duration, distance; // Duration used to calculate distance

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
byte rowPins[ROWS] = {45, 46, 47, 48}; //connect to the row pinouts of the keypad;
byte colPins[COLS] = {50, 49, 51}; //connect to the column pinouts of the keypad;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

int handshaken = 0;




/*sonar code
#define TRIGGER_PIN  22  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     24  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
/*sonar code*/

/*Keypad code
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
/*keypad code

char data[12];
/*keypad code*/

/*IR code
#define sensorIR 15               //Must be an analog pin
float sensorValue, inches, cm;    //Must be of type float for pow()
/*IR code*/

/*gyro code
L3G gyro;
/*gyro code*/

/*baro code
LPS ps;
/*baro code*/

/*accelerometer code
LSM303 compass;
char report[80];
/*accelerometer code*/

char debugBuffer[1024];
//char debugBuffer[2048];
void debugPrint(const char *str)
{
	Serial.println(str);
	Serial.flush();
}
void dprintf(const char *fmt, ...)
{
	va_list argptr;
	va_start(argptr, fmt);
	vsprintf(debugBuffer, fmt, argptr);
	va_end(argptr);
	debugPrint(debugBuffer);
}
int sendData(int id, const char *fmt, ...){
	int inByte;
	char dataBuffer[1024];
	va_list argptr;
		va_start(argptr, fmt);
		vsprintf(dataBuffer, fmt, argptr);
		va_end(argptr);		
		/*vsprintf(dataBuffer,"0 %d 1 %d 2 %d 3 %d 4 %d 5 %d 6 %d 7 %d", data[ID_DATA_KEYPAD],
		data[ID_DATA_HEADING],
		data[ID_DATA_DIST],
		data[ID_DATA_SONAR1],
		data[ID_DATA_SONAR2],
		data[ID_DATA_SONAR3],
		data[ID_DATA_SONAR4],
		data[ID_DATA_SONAR5]);*/
	
	while(handshaken) {
		//dprintf("l");
		Serial1.write(4);
		Serial1.write(id);
		Serial1.write(dataBuffer,strlen(dataBuffer));
		//dprintf("%d sizeof",(int)sizeof(dataBuffer));
		Serial1.flush();
			Serial.println("stuck");
	//	Serial1.write("data");
		inByte = Serial1.read();
		if (inByte == 0) { //receive 0ACK
			//debugPrint("$");
			dprintf("$");
			break;
		}
	}
	
}

int freeRAM () {
	extern int __heap_start;
	extern int *__brkval;
	int v;
	dprintf("%d _hs  %d_brkval %d _vStart",(int)&__heap_start,(int)&__brkval,(int)&v);
	if(__brkval == 0){
		return (int)&v - (int)&__heap_start;
	}
	return (int)&v - (int)__brkval;
	//return ((int) &v) – ((__brkval == 0 ? (int) &__heap_start : (int) __brkval));
}

void printArray(void* p){
	while(1){
		/*int s;
		int end;
		dprintf("%d_s %d_end",(int)&s,(int)&end);*/
		//freeRAM();
		dprintf("%d", freeRAM());
		vTaskDelay(1000);
	}
}
	/*int i;
	//data [1] = 123;
	char canRead = '0';
	while(1){
		if(Serial.available()){
			canRead = Serial.read();
		}
		if(canRead -'0'){
			//for(i = 1;i<10;i++){
				Serial.println(/*data[1]213);
				Serial.print('\r');
			}
		Serial.println(freeRAM());
			canRead = '0';
		}
		vTaskDelay(500);
	}
}
*/
		
void task_sensor_poll(void* p){
	
  while(1){
  
  /***********************************
  **        reading sensors
  ************************************/
  compass.read();
 /* float heading = compass.heading();
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
  
/*  Serial.print("Pressure is ");
  Serial.print(pressure);
  Serial.println(" mbar");
  Serial.print("Altitude is ");
  Serial.print(altitude);
  Serial.println(" m.");
  
  /******************************************************
  **  gyro meter reading
  ******************************************************/
  gyro.read();
/*  Serial.println("Gyro meter ");
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
 /* String direction = "";
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
/*  if(ZaVal<-965){
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
/*  fXa = XaVal * alpha + (fXa * (1.0 - alpha));
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
  //newTime = millis();
 /* deltaTime = newTime - oldTime;
  
   XaVal = XaVal - (1000 * (sin(pitch)));//offsetting pitch 
  
  // estimate the average acceleration since the previous sample, by averaging the two samples
  long avgAccel = (oldXaVal + XaVal) / 2;
  
  //if ((XaVal < 50 && XaVal > -50) && (oldXaVal < 50 && oldXaVal > -50)) 
  //  avgAccel = 0;
  
 
  
/*  Serial.print("the avgAccel is ");
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
/*  Serial.print("IR sensor reads ");
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
 dprintf("%d",(int)distance);
/* Serial.print("sonar distance is ");
 Serial.println(distance);
 Serial.println();*/
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
}
void setup(){
	
	Serial.begin(115200);
	Serial1.begin(115200);
	Serial1.flush();
	Wire.begin(); //gyro code
	gyro.init();//gyro code
	gyro.enableDefault(); //gyro code
	ps.enableDefault(); //baro code
	
	 handshaken = 0;
		
		/*accelerometer code*/
		compass.init();
		compass.enableDefault();
		/*accelerometer code*/
		/*sonar code*/
		pinMode(TRIGGER_PIN, OUTPUT);
		pinMode(ECHO_PIN, INPUT);
		
		pinMode(TRIGGER_PIN2, OUTPUT);
		pinMode(ECHO_PIN2, INPUT);
		pinMode(TRIGGER_PIN3, OUTPUT);
		pinMode(ECHO_PIN3, INPUT);
		pinMode(TRIGGER_PIN4, OUTPUT);
		pinMode(ECHO_PIN4, INPUT);
		pinMode(TRIGGER_PIN5, OUTPUT);
		pinMode(ECHO_PIN5, INPUT);
		
		/*sonar code*/
		   pinMode(MOTOR, OUTPUT);
		   
		   
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

void task_baro(void* p){
	/*baro code*/ 
	while(1)
	{
		float pressure = ps.readPressureMillibars();
		//dprintf("raw pressure is %d",(int) ((float)ps.readPressureRaw()/ 4096));
		float altitude = ps.pressureToAltitudeMeters(pressure);
		float temperature = ps.readTemperatureC();
		//dprintf("p: ");
		//dprintf("%d",pressure);
		//dprintf(" mbar\ta: ");
		//dprintf("%d",(int)altitude);
		//dprintf(" m\tt: ");
		//dprintf("%d",temperature);
		//dprintf(" deg C");
	//	dprintf("%d is pressure, %d is altitude, %d is temperature",(int) pressure,(int)  altitude,(int) temperature);
		//dprintf("%d alt",(int)altitude);
		/*
		Serial.print("p: ");
		Serial.print(pressure);
		Serial.print(" mbar\ta: ");
		Serial.print(altitude);
		Serial.print(" m\tt: ");
		Serial.print(temperature);
		Serial.println(" deg C");
*/		//delay(1000);
		vTaskDelay(taskDelay);
		//delay(100);
	}
	/*baro code*/
}
void task_keypad(void* p){
	
	/*KeyPad code*/
	while(1)
	{
		//if(handshaken){
		char key = keypad.getKey();
	//Serial.println("key");
		//print out the key that is pressed
		if (key != NO_KEY){
			dprintf("%c",key);
			/*dprintf*/sendData(ID_DATA_KEYPAD, "%c",key);
			data[ID_DATA_KEYPAD] = (int) key;
			
		}
		//Serial.println("---------------------");
		vTaskDelay(taskDelay);
	//}
	}
	/*KeyPad Code*/
	
}
void task_accelerometer(void* p){
	
	
	/*accelerometer code*/
	while(1)
	{
		
		compass.read();
		//snprintf(report, sizeof(report), "A: %6d %6d %6d    M: %6d %6d %6d",
		//compass.a.x, compass.a.y, compass.a.z,
		//compass.m.x, compass.m.y, compass.m.z);
		//Serial.println(report);
		//dprintf( "A: %6d %6d %6d    M: %6d %6d %6d",
		//compass.a.x, compass.a.y, compass.a.z,
		//compass.m.x, compass.m.y, compass.m.z);
		//dprintf("%d",compass.a.x);
		//dprintf("%d",compass.a.x);
		//Serial.print(compass.a.x);
	//	Serial.print("1");
		//delay(1000);
		vTaskDelay(taskDelay);
	}
	/*accelerometer code*/
	
}
/*void task1(void* p)
{
	
	while(1)
	{
		digitalWrite(12,HIGH);
		vTaskDelay(1000);
		digitalWrite(12,LOW);
		vTaskDelay(1000);
	}
	
}*/

void task_ir(void* p){
	/*Infared code*/
	while(1){
		
		sensorValue = analogRead(sensorIR);
		//inches = 4192.936 * pow(sensorValue,-0.935) - 3.937;
		cm = 10650.08 * pow(sensorValue,-0.935) - 10;
		//delay(100);
		dprintf("%d", (int)cm);
		//delay(1000);
		vTaskDelay(10000);
		//Serial.print("Inches: ");
		//Serial.println(inches);
		
		
		//Serial.println(" Cm");
	}
		/*infrared code*/
}
void task_sonar1(void* p){
	
	while(1){
		 digitalWrite(TRIGGER_PIN, LOW);
		  delayMicroseconds(2);

		  digitalWrite(TRIGGER_PIN, HIGH);
		  delayMicroseconds(10);
		  
		  digitalWrite(TRIGGER_PIN, LOW);
		  pinMode(ECHO_PIN,INPUT);
		  duration = pulseIn(ECHO_PIN, HIGH);
		  
		  //Calculate the distance (in cm) based on the speed of sound.
		  distance = duration/58.2;
		  /*
		 pinMode(ECHO_PIN,INPUT);
		 digitalWrite(TRIGGER_PIN,HIGH);
		 delayMicroseconds(1000);
		 digitalWrite(TRIGGER_PIN,LOW);
		 duration = pulseIn(ECHO_PIN,HIGH);
		 distance = (duration/2)/29.1;*/
		/*  if(distance>10 && distance < 60){
			  digitalWrite(MOTOR, HIGH);   // sets the LED on
			  //  delay(100);                  // waits for a second
			  //digitalWrite(MOTOR, LOW);    // sets the LED off
			  //delay(1000);                  // waits for a second
			  }else{
			  digitalWrite(MOTOR, LOW);
			  // delay(100);
		  }*/
		  
		  dprintf("%d",(int)distance);
		  delay(50);
	}
	
	while(1){
		 /* digitalWrite(TRIGGER_PIN, LOW);
		  delayMicroseconds(2);

		  digitalWrite(TRIGGER_PIN, HIGH);
		  delayMicroseconds(10);
		  
		  digitalWrite(TRIGGER_PIN, LOW);
		  duration = pulseIn(ECHO_PIN, HIGH);
		  
		  //Calculate the distance (in cm) based on the speed of sound.
		  distance = duration/58.2;*/
		 pinMode(ECHO_PIN,INPUT);
		 digitalWrite(TRIGGER_PIN,HIGH);
		 delayMicroseconds(1000);
		 digitalWrite(TRIGGER_PIN,LOW);
		 duration = pulseIn(ECHO_PIN,HIGH);
		 distance = (duration/2)/29.1;
		  if(distance>10 && distance < 60){
			  digitalWrite(MOTOR, HIGH);   // sets the LED on
			  //  delay(100);                  // waits for a second
			  //digitalWrite(MOTOR, LOW);    // sets the LED off
			  //delay(1000);                  // waits for a second
			  }else{
			  digitalWrite(MOTOR, LOW);
			  // delay(100);
		  }
		  
		  dprintf("%d dis",(int)distance);
		  delay(500);
	}
	
	/*sonar code*/
		/*while(1){
		float duration, distance;
		digitalWrite(22, LOW);  // Added this line
		delayMicroseconds(2); // Added this line
		digitalWrite(22, HIGH);
		//  delayMicroseconds(1000); - Removed this line
		delayMicroseconds(10); // Added this line
		digitalWrite(22, LOW);
		duration = pulseIn(24, HIGH);
		distance = (duration/2) / 29.1;
		dprintf("%d",(int)distance);
		delay(100);
	}*/
	/*while(1){
		delay(50);                      // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
		unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
		//Serial.print("Ping: ");
		dprintf("%d",(int)sonar.convert_cm(uS));
		//sonar.convert_cm(uS);
		vTaskDelay(500);
	}
	/*sonar code*/
	
}

void task_gyro(void* p){
	
	
	/*gyro code*/
	while(1){
		
		gyro.read();// once gyro read is inside, code stops output. without gyro.read(), output is 0
	//	dprintf("X is %d, Y is %d, Z is %d", (int)gyro.g.x,(int)gyro.g.y,(int)gyro.g.z);
		//delay(1000);
		vTaskDelay(taskDelay);
		
	}

	/* gyro code*/
}
/*void task2(void* p)
{
		
	
		while(1)
	{
		dprintf("%d",2);
		digitalWrite(12,HIGH);
		vTaskDelay(250);
		digitalWrite(12,LOW);
		vTaskDelay(250);
	}
}
void task1(void* p)
{
	
	
	while(1)
	{
		dprintf("%d",1);
		digitalWrite(13,HIGH);
		vTaskDelay(500);
		digitalWrite(13,LOW);
		vTaskDelay(500);
	}
}*/
/*
void task1(void* p){

	//char report[1024];
	while(1){
		//Serial.println(123);
		//snprintf(report,1024, "%d",1);
		//Serial.println(report);
		//compass.a.x, compass.a.y, compass.a.z,
		//compass.m.x, compass.m.y, compass.m.z);
		//Serial.println("1");
		//puts("1");
		//dprintf("%d",1);
		//for(int i = 0; i< 1024; i++)
		//debugBuffer[i] = '/0';
//	Serial.print;
	delay(100);
		vTaskDelay(1000);
		//for(int i = 0; i< 1024; i++)
		//debugBuffer[i] = '/0';
	}
}
void task2(void* p){
	
	
	while(1){
	//	snprintf(report,1024, "%d",2);
		Serial.println(456);
		//puts("2");
		//Serial.println("2");
		//dprintf("%d",2);
		//for(int i = 0; i< 1024; i++)
		//debugBuffer[i] = '/0';
		delay(2000);
		vTaskDelay(2000);
		
	}
}*/
float sonar_read(int trigger, int echo){	 
	 
	 
	 digitalWrite(trigger, LOW);
	 delayMicroseconds(5);

	 digitalWrite(trigger, HIGH);
	 delayMicroseconds(50);
	 
	 digitalWrite(trigger, LOW);
	 pinMode(echo,INPUT);
	 duration = pulseIn(echo, HIGH,100000);
	 
	 //Calculate the distance (in cm) based on the speed of sound.
	 distance = duration/58.2;
	 return distance;
}


void task_poll_sensor(void* p){

	while(1){
		//unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
		//unsigned int uS2 = sonar2.ping();
		/* Serial.print("Sonar 1: ");
		Serial.print(sonar.convert_cm(uS)); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
		Serial.println("cm");
  
		Serial.print("Sonar 2: ");
		Serial.print(sonar2.convert_cm(uS2));
		Serial.println("cm");*/
 
 
	//	dprintf("%d",(int)sonar.convert_cm(uS));
	//	vTaskDelay(1000);
		// dprintf("%d",(int)sonar.convert_cm(uS2));

		/* if(sonar.convert_cm(uS)<50){
		digitalWrite(MOTOR, HIGH);   // sets the LED on
		delay(100);                  // waits for a second
		//digitalWrite(MOTOR, LOW);    // sets the LED off
		//delay(1000);                  // waits for a second
		}else{
		digitalWrite(MOTOR, LOW);
		delay(100);
		}

		*/
		
		/*	 digitalWrite(TRIGGER_PIN, LOW);
			 delayMicroseconds(2);

			 digitalWrite(TRIGGER_PIN, HIGH);
			 delayMicroseconds(10);
			 
			 digitalWrite(TRIGGER_PIN, LOW);
			 pinMode(ECHO_PIN,INPUT);
			 duration = pulseIn(ECHO_PIN, HIGH,100000);
			 
			 //Calculate the distance (in cm) based on the speed of sound.
			 distance = duration/58.2;
		//	dprintf("%d 1", (int)distance);
			
			 digitalWrite(TRIGGER_PIN2, LOW);
			 delayMicroseconds(2);

			 digitalWrite(TRIGGER_PIN2, HIGH);
			 delayMicroseconds(10);
			 
			 digitalWrite(TRIGGER_PIN2, LOW);
			 pinMode(ECHO_PIN2,INPUT);
			 duration = pulseIn(ECHO_PIN2, HIGH,100000);
			 
			 //Calculate the distance (in cm) based on the speed of sound.
			 distance = duration/58.2;
		//	 dprintf("%d 2", (int)distance);
			 
			 
			 
			  digitalWrite(TRIGGER_PIN3, LOW);
			  delayMicroseconds(2);

			  digitalWrite(TRIGGER_PIN3, HIGH);
			  delayMicroseconds(10);
			  
			  digitalWrite(TRIGGER_PIN3, LOW);
			  pinMode(ECHO_PIN3,INPUT);
			  duration = pulseIn(ECHO_PIN3, HIGH,100000);
			  
			  //Calculate the distance (in cm) based on the speed of sound.
			  distance = duration/58.2;
			//  dprintf("%d 3", (int)distance);
			  
			  
			  
			   digitalWrite(TRIGGER_PIN4, LOW);
			   delayMicroseconds(2);

			   digitalWrite(TRIGGER_PIN4, HIGH);
			   delayMicroseconds(10);
			   
			   digitalWrite(TRIGGER_PIN4, LOW);
			   pinMode(ECHO_PIN4,INPUT);
			   duration = pulseIn(ECHO_PIN4, HIGH,100000);
			   
			   //Calculate the distance (in cm) based on the speed of sound.
			   distance = duration/58.2;
			//   dprintf("%d 4", (int)distance);
			   
			   
			    digitalWrite(TRIGGER_PIN5, LOW);
			    delayMicroseconds(2);

			    digitalWrite(TRIGGER_PIN5, HIGH);
			    delayMicroseconds(10);
			    
			    digitalWrite(TRIGGER_PIN5, LOW);
			    pinMode(ECHO_PIN5,INPUT);
			    duration = pulseIn(ECHO_PIN5, HIGH,100000);
			    
			    //Calculate the distance (in cm) based on the speed of sound.
			    distance = duration/58.2;
		//	    dprintf("%d 5", (int)distance);
			
			

			
		//Calculate the distance (in cm) based on the speed of sound.
		/*distance = duration/58.2;*/
		float distance1,distance2,distance3,distance4,distance5;
		distance1 = sonar_read(TRIGGER_PIN,ECHO_PIN);
		distance2= sonar_read(TRIGGER_PIN2,ECHO_PIN2);
		distance3 = sonar_read(TRIGGER_PIN3,ECHO_PIN3);
		distance4 = sonar_read(TRIGGER_PIN4,ECHO_PIN4);	
		distance5 = sonar_read(TRIGGER_PIN5,ECHO_PIN5);
		dprintf("%d %d %d %d %d",(int)distance1,(int)distance2,(int)distance3,(int)distance4,(int)distance5);
		
		/*dprintf("%d", (int) sonar_read(TRIGGER_PIN,ECHO_PIN));
		dprintf("%d", (int) sonar_read(TRIGGER_PIN2,ECHO_PIN2));
		dprintf("%d", (int) sonar_read(TRIGGER_PIN3,ECHO_PIN3));
		dprintf("%d", (int) sonar_read(TRIGGER_PIN4,ECHO_PIN4));
		dprintf("%d", (int) sonar_read(TRIGGER_PIN5,ECHO_PIN5));*/
		
		
 /*sonar final code
 digitalWrite(TRIGGER_PIN, LOW);
		  delayMicroseconds(2);

		  digitalWrite(TRIGGER_PIN, HIGH);
		  delayMicroseconds(10);
		  
		  digitalWrite(TRIGGER_PIN, LOW);
		  pinMode(ECHO_PIN,INPUT);
		  duration = pulseIn(ECHO_PIN, HIGH,100000);
		  
		  //Calculate the distance (in cm) based on the speed of sound.
		  distance = duration/58.2;
		  
		  */
		  
		  /*
		 pinMode(ECHO_PIN,INPUT);
		 digitalWrite(TRIGGER_PIN,HIGH);
		 delayMicroseconds(1000);
		 digitalWrite(TRIGGER_PIN,LOW);
		 duration = pulseIn(ECHO_PIN,HIGH);
		 distance = (duration/2)/29.1;*/
		/*  if(distance>10 && distance < 60){
			  digitalWrite(MOTOR, HIGH);   // sets the LED on
			  //  delay(100);                  // waits for a second
			  //digitalWrite(MOTOR, LOW);    // sets the LED off
			  //delay(1000);                  // waits for a second
			  }else{
			  digitalWrite(MOTOR, LOW);
			  // delay(100);
		  }*/
		  
		 // dprintf("%d",(int)distance);
		/***********************************
		**        reading sensors
		************************************/
		compass.read();
		dprintf("%d", int(compass.heading()));
		//dprintf("%d z",(int)(compass.a.z/16.0));
		
		/*if(compass.a.z/16.0<-1000){
		distFromStart += 33;
		step++;
		dprintf("%d step",step);	
		}*/
		/*  float heading = compass.heading();
		float XaVal, YaVal, ZaVal, fXa, fYa,fZa, pitch, roll,pitch_print, roll_print;
		const float alpha = 0.15;
		XaVal = compass.a.x/16.0; //Acceleration data registers contain a left-aligned 12-bit number, so values should be shifted right by 4 bits (divided by 16)
		YaVal = compass.a.y/16.0; //unit is in cm/s2
		ZaVal = compass.a.z/16.0;
		/***********************************
		**       keypad
		************************************/
		char key = keypad.getKey();

		//print out the key that is pressed 
		if (key != NO_KEY){
		// Serial.print("You have pressed ");
		Serial.println(key);
		}
		/***********************************
		**       altitude
		************************************/
		float pressure = ps.readPressureMillibars() + 248.5;
		float altitude = ps.pressureToAltitudeMeters(pressure);
		
		//dprintf("alt %d , pres %d",(int)altitude,(int)pressure);
		// Serial.print("Pressure is ");
		// Serial.print(pressure);
		//  Serial.println(" mbar");
		// Serial.print("Altitude is ");
		// Serial.print(altitude);// causes error
		// Serial.println(" m.");
		//dprintf("%d",(int)pressure);
		//dprintf("%d",(int)altitude);
		/******************************************************
		**  gyro meter reading
		******************************************************/
		gyro.read();
		/*Serial.println("Gyro meter ");
		Serial.print("X: ");
		Serial.print((int)gyro.g.x * 8.75 /1000);
		Serial.println(" degree/second");
		Serial.print("Y: ");
		Serial.print((int)gyro.g.y * 8.75 /1000);
		Serial.println(" degree/second");
		Serial.print("Z: ");
		Serial.print((int)gyro.g.z * 8.75 /1000);
		Serial.println(" degree/second");
		Serial.println("");*/
  
		//dprintf("x: %d",(int)(gyro.g.x * 8.75 /1000));
		//dprintf("y: %d",(int)(gyro.g.y * 8.75 /1000));
		//dprintf("z: %d",(int)(gyro.g.z * 8.75 /1000));
  
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
		// String direction = "";
		/*if(heading>=340 || heading <= 20)
  
		dprintf("North"); // direction = "North";
		else if (heading>=70 && heading <= 110)
 
		dprintf("East"); //  direction = "East";
		else if (heading>=160 && heading <= 200)
 
		dprintf("South");   //direction = "South";
		else if (heading>=250 && heading <= 290)

		dprintf("West");  //  direction = "West";
    
    
		else if (heading>20 && heading < 70)
  
		dprintf("North East"); // direction = "North East";
		else if (heading>110 && heading < 160)
 
		dprintf("South East"); //  direction = "South East";
		else if (heading>200 && heading < 250)
   
		dprintf("South West");// direction = "South West";
		else if (heading>290 && heading < 340)
 
		dprintf("North West");  // direction = "North West";
	
		// Serial.print("Heading is ");
		//Serial.println(direction);
		//Serial.println("degree.");
		/******************************************************
		**  Method 1 to calculate distance: using steps
		******************************************************/
 
		// a step and  distance using Z-ACCELERATION
		/*  if(ZaVal<-950){
		distFromStart+=33;  //1 step is 33 cm
		step++; 
		} 

  
		/*  Serial.print("X accel is ");Serial.print(XaVal); Serial.print(" cm/s2"); Serial.println(" "); 
		Serial.print("Y accel is ");Serial.print(YaVal); Serial.print(" cm/s2"); Serial.println(" "); 
		Serial.print("Z accel is ");Serial.print(ZaVal);Serial.print(" cm/s2"); Serial.println(" "); 
   
 
		Serial.print("1. You have walked ");
		Serial.print(step);
		Serial.print(" steps and distance is ");
		Serial.print(distFromStart);
		Serial.println(" cm from start");*/


		/*dprintf("x accel %d", (int)XaVal); 
		dprintf("y accel %d",(int) YaVal); 
		dprintf("z accel %d", (int)ZaVal); */
	
	
		/******************************************************
		**  pitch and roll
		******************************************************/
		// Low-Pass filter accelerometer
		/*  fXa = XaVal * alpha + (fXa * (1.0 - alpha));
		fYa = YaVal * alpha + (fYa * (1.0 - alpha));
		fZa = ZaVal * alpha + (fZa * (1.0 - alpha));

		/* Serial.print("Low pass X accel is ");Serial.print(fXa); Serifal.print(" cm/s2"); Serial.println(" "); 
		Serial.print("Low pass Y accel is ");Serial.print(fYa); Serial.print(" cm/s2"); Serial.println(" "); 
		Serial.print("Low pass Z accel is ");Serial.print(fZa);Serial.print(" cm/s2"); Serial.println(" ");    */
    
		/* roll  = atan2(fYa, sqrt(fXa*fXa + fZa*fZa));
		pitch = atan2(fXa, sqrt(fYa*fYa + fZa*fZa));
  
		roll_print = roll*180.0/M_PI;
		pitch_print = pitch*180.0/M_PI;
		/* Serial.print("pitch(Y) is ");
		Serial.print(pitch_print);
		Serial.println("degree ");

		Serial.print("roll(X) is ");
		Serial.print(roll_print);
		Serial.println("degree ");*/
		/******************************************************
		**  Method 2 to calculate distance: using accelerations
		******************************************************/
		/*  newTime = millis();
		deltaTime = newTime - oldTime;
  
		XaVal = XaVal - (1000 * (sin(pitch)));//offsetting pitch 
  
		// estimate the average acceleration since the previous sample, by averaging the two samples
		long avgAccel = (oldXaVal + XaVal) / 2;
  
		//if ((XaVal < 50 && XaVal > -50) && (oldXaVal < 50 && oldXaVal > -50)) 
		//  avgAccel = 0;
  
 
		/* working
		Serial.print("the avgAccel is ");
		Serial.print(avgAccel);
		Serial.println(" cm/s2");*/
		// integrate the average accel and add it to the previous speed to calculate the new speed
		// long newVelocity = oldVelocity + (avgAccel  * deltaTime/1000);
 
   
		//estimate the average speed since the previous sample, by averaging the two speeds
		//long avgVelocity = (oldVelocity + newVelocity) / 2;
  
		//  if ((XaVal < 50 && XaVal > -50) && (oldXaVal < 50 && oldXaVal > -50)) 
		//  avgVelocity = 0;
  
  
		// integrate the average speed and add it to the previous displacement to get the new displacement
		/*  long newDisplacement = oldDis + (avgVelocity * deltaTime/1000);
  
		oldTime = newTime;
		oldVelocity = newVelocity ;
		oldDis = newDisplacement;
		oldXaVal = XaVal;*/
		/*working
		Serial.print("2. You have walked ");
		Serial.print(newDisplacement);
		Serial.println("cm from start");  */
  
		/******************************************************
		**  IR sensor meter reading
		******************************************************/
		sensorValue = analogRead(sensorIR);
		cm = 10650.08 * pow(sensorValue,-0.935) - 10;
		/* Serial.print("IR sensor reads ");
		Serial.print(cm);
		Serial.println(" Cm");*/
  
		//delay(100);
		vTaskDelay(100);
	}
}
float prevTime = 0;
void task_headingNdist(void* p){
	while(1){
	//	dprintf("%d headinShake",handshaken);
	//	if(handshaken){
		//Serial.print("z");
		//Serial.println("heading");
		compass.read();
		//dprintf("%d mem",(int)freeRAM());
		//Serial.print("a");
		float heading = compass.heading();
		//Serial.print("b");
		//dprintf("%d mem2",(int)freeRAM());
		
		//dprintf("%d",(int)compass.a.x);
		float ZaVal,XaVal,YaVal,RZaVal;
		//ZaVal = compass.a.z/16.0;
		XaVal = compass.a.x/16.0;
		YaVal = compass.a.y/16.0;
		ZaVal = compass.a.z/16.0;
		RZaVal = sqrt( ((XaVal*XaVal)+(YaVal*YaVal))/4.0 + (ZaVal*ZaVal));
		
		//ZaVal = sqrt( ((compass.a.x*compass.a.x)+(compass.a.y*compass.a.y))/4.0 + (compass.a.z*compass.a.z));
		//ZaVal = ZaVal/16.0;
		// dprintf("%d", (int)compass.a.x);
		//dprintf("%d", (int)((compass.a.x*compass.a.x)/*+(compass.a.y*compass.a.y)/4.0*/));
		// dprintf("%d x %d y %d z", (int)compass.a.x, (int)compass.a.y,(int) compass.a.z);
		// dprintf("%d z val",(int) ZaVal);
	//	dprintf("%d",(int) ZaVal);
	//Serial.print("a");
	
	//dprintf("%d",(int)heading);
	//dprintf("%d",(int)compass.heading());
	//compass.heading();
	//Serial.print("b");
		//data[ID_DATA_HEADING] = (int) compass.heading();
	/*	if(ZaVal<-965){
			distFromStart+=33;  //1 step is 33 cm
			step++;
		}*/
	float currentTime = millis();
	if(RZaVal>1000 && (currentTime - prevTime) >= 600){
		distFromStart+=33;  //1 step is 33 cm
		step++;
	//	dprintf("%d_RZaval",(int)RZaVal);
		//	dprintf("%d _step %d _heading ",(int)step, (int) heading);
			prevTime = currentTime;
		}
		dprintf("%d",(int)heading);
		//sendData("%d %d",ID_DATA_HEADING,(int)heading);
		sendData(ID_DATA_HEADING,"%d",(int)heading);
		sendData(ID_DATA_DIST,"%d",(int)step);
		//delay(1000);
		//sendData("%d %d %d %d", ID_DATA_HEADING,(int) heading, ID_DATA_DIST, (int)step);
		//data[ID_DATA_DIST] = (int) distFromStart;
		//dprintf("dist is %d",(int)data[ID_DATA_DIST]);
		//dprintf("a");
		//delay(100);*/
	//delay(100);
		vTaskDelay(taskDelay);
		//}
	}
	
}
void task_poll_sonar(void* p){
	 UBaseType_t uxHighWaterMark;
	uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );
	//dprintf("start %d",(int)uxHighWaterMark);
	while(1){
		//if(handshaken){
			Serial.println("sonar");
		unsigned int s1 = sonar.ping();
		unsigned int s2 = sonar2.ping();
		unsigned int s3 = sonar3.ping();
		unsigned int s4 = sonar4.ping();
		unsigned int s5 = sonar5.ping();
		dprintf("%d %d %d %d %d %d %d %d %d %d", ID_DATA_SONAR1,(int)
		sonar.convert_cm(s1),ID_DATA_SONAR2,(int)sonar2.convert_cm(s2),ID_DATA_SONAR3,(int)sonar3.convert_cm(s3),ID_DATA_SONAR4
		,(int)sonar4.convert_cm(s4),ID_DATA_SONAR5,(int)sonar5.convert_cm(s5));
		
		sendData( ID_DATA_SONAR1,"%d",(int)sonar.convert_cm(s1));
		sendData(ID_DATA_SONAR2,"%d",(int)sonar2.convert_cm(s2));
		sendData(ID_DATA_SONAR3,"%d",(int)sonar3.convert_cm(s3));
		sendData(ID_DATA_SONAR4,"%d",(int)sonar4.convert_cm(s4));
		sendData(ID_DATA_SONAR5,"%d",(int)sonar5.convert_cm(s5));
	/*float distance1,distance2,distance3,distance4,distance5;
	distance1 = sonar_read(TRIGGER_PIN,ECHO_PIN);
	distance2= sonar_read(TRIGGER_PIN2,ECHO_PIN2);
	distance3 = sonar_read(TRIGGER_PIN3,ECHO_PIN3);
	distance4 = sonar_read(TRIGGER_PIN4,ECHO_PIN4);
	distance5 = sonar_read(TRIGGER_PIN5,ECHO_PIN5);
	dprintf("%d %d %d %d %d",(int)distance1,(int)distance2,(int)distance3,(int)distance4,(int)distance5);*/
	
	/*data[ID_DATA_SONAR1] = (int) sonar_read(TRIGGER_PIN,ECHO_PIN);
//	dprintf("%d 1 ",(int) sonar_read(TRIGGER_PIN,ECHO_PIN));
	data[ID_DATA_SONAR2]=	(int) sonar_read(TRIGGER_PIN2,ECHO_PIN2);
	data[ID_DATA_SONAR3] = (int) sonar_read(TRIGGER_PIN3,ECHO_PIN3);
	data[ID_DATA_SONAR4] = (int) sonar_read(TRIGGER_PIN4,ECHO_PIN4);
	data[ID_DATA_SONAR5] = (int) sonar_read(TRIGGER_PIN5,ECHO_PIN5);
	//dprintf("%d %d %d %d %d",data[ID_DATA_SONAR1],data[ID_DATA_SONAR2],data[ID_DATA_SONAR3],data[ID_DATA_SONAR4],data[ID_DATA_SONAR5]);
	*/
	vTaskDelay(taskDelay);
	//vTaskDelay(taskDelay);
	// uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL ); 
	
	//dprintf("now %d",(int)uxHighWaterMark);
	
	//delay(1000);
	//	}
	}
}


int readSerialByte() {	
	return Serial1.read();
}

void handshakenUntilFinish() {
	int inByte;
		while (1) {
			if (Serial1.available()){
				inByte = Serial1.read();
				dprintf("%c",inByte);
				if (inByte == 2) { // receive 2HELO
					dprintf("!");
					break;
				}
			}
		}
		dprintf("^");
		while (1) {
			dprintf("w");
			inByte = Serial1.read();
			Serial1.write(3); // answer 3HELLOACK
			if (inByte == 0) { //receive 0ACK
				dprintf("#");
				handshaken = 1;
				break;
			}
		}
}

int sendSimpleData() {
	int inByte;
	while(1) {
		Serial1.write(4);
		Serial1.write(0);
		Serial1.write("data");
		inByte = Serial1.read();
		if (inByte == '0') { //receive 0ACK
			debugPrint("$");
			break;
		}
	}
}


void task_comm(void* p){
	/* UBaseTwype_t uxHighWaterMark;
	  uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );*/
	while(1) {
		if(!handshaken){
			dprintf("enter handuntil");
		handshakenUntilFinish();
		}
		Serial.println("com");
		//vTaskDelete(NULL);
		vTaskDelay(portMAX_DELAY);
		//else {
			//sendSimpleData();
		/*	sendData("0 %d 1 %d 2 %d 3 %d 4 %d
		data[ID_DATA_SONAR4], 5 %d 6 %d 7 %d", data[ID_DATA_KEYPAD],
			data[ID_DATA_HEADING],
			data[ID_DATA_DIST],
			data[ID_DATA_SONAR1],
			data[ID_DATA_SONAR2],
			data[ID_DATA_SONAR3],
			data[ID_DATA_SONAR5]);*/
	//	}
	/*	dprintf("0 %d 1 %d 2 %d 3 %d 4 %d 5 %d 6 %d 7 %d", data[ID_DATA_KEYPAD],
		data[ID_DATA_HEADING],
		data[ID_DATA_DIST],
		data[ID_DATA_SONAR1],
		data[ID_DATA_SONAR2],
		data[ID_DATA_SONAR3],
		data[ID_DATA_SONAR4],
		data[ID_DATA_SONAR5]);*/
		//vTaskDelay(taskDelay);
	}
}
#define STACK_DEPTH 128//128// 128//128//128//64

void vApplicationIdleHook()
{
	//Do nothing
}

int main(void)
{
	init();
	setup();
	

	/*while(1){
	compass.read();
	float heading = compass.heading();
	dprintf("%d",(int) heading);
	delay(1000);
	}*/
	
	
	//pinMode(12,OUTPUT);
	//pinMode(13,OUTPUT);
	TaskHandle_t t1,t2,t3,t4;

	/*while(1){
		//gyro
		gyro.read();
		//acc
		compass.read();
		//sonar
		unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
		int sonar_reading = (int)sonar.convert_cm(uS);
		//baro
		float pressure = ps.readPressureMillibars();
		//dprintf("raw pressure is %d",(int) ((float)ps.readPressureRaw()/ 4096));
		float altitude = ps.pressureToAltitudeMeters(pressure);
		float temperature = ps.readTemperatureC();
		
		
		//ir
		sensorValue = analogRead(sensorIR);
		//inches = 4192.936 * pow(sensorValue,-0.935) - 3.937;
		cm = 10650.08 * pow(sensorValue,-0.935) - 10;
		
		char key = keypad.getKey();

		//print out the key that is pressed
		if (key != NO_KEY){
			dprintf("%c",key);
		}
	}*/
		
	
	//Create tasks
	//xTaskCreate(task1, "Task 1", STACK_DEPTH, NULL, 6, &t1);
	//xTaskCreate(task2, "Task 2", STACK_DEPTH, NULL, 5, &t2);
	//xTaskCreate(printArray, "Task Gyro", STACK_DEPTH,NULL,0,&t1);
	//xTaskCreate(task_sonar1,"task sornar",STACK_DEPTH,NULL,5,&t2);
	
	//xTaskCreate(task_ir,"Task Accelerometer", STACK_DEPTH, NULL,6,&t2);
	
	//xTaskCreate(task_poll_sensor,"Task_sensor",STACK_DEPTH,NULL,5,&t1);
	

	//xTaskCreate(task_accelerometer, "Task acc", STACK_DEPTH,NULL,5,&t1);
	//xTaskCreate(task_poll_sonar,"task_poll_sensor",STACK_DEPTH,NULL,6,&t2);
	//xTaskCreate(task_gyro, "Task gyro", STACK_DEPTH,NULL,7,&t3);
	//xTaskCreate(task_baro, "Task Gyro", STACK_DEPTH,NULL,8,&t4);
	//xTaskCreate(task_keypad, "Task acc", STACK_DEPTH,NULL,9,&t5);
	//xTaskCreate(task_comm,"task comm",STACK_DEPTH,NULL,6,&t6);
	//xTaskCreate(printArray,"task comm",STACK_DEPTH,NULL,7,&t6);
	
	
	
	
	
	
	xTaskCreate(task_comm,"task comm",256,NULL,3,&t1);
	xTaskCreate(task_poll_sonar,"task poll sensor", 256,NULL,4,&t2);
	xTaskCreate(task_keypad,"task keypad",STACK_DEPTH,NULL,5,&t3);
	xTaskCreate(task_headingNdist, "Task_heading",256,NULL,6,&t4);
	//dprintf("%d size",uxTaskGetStackHighWaterMark(t1));
	//dprintf("%d",(int)&task_gyro);
	//dprintf("%d",(int)&task_keypad);
	//dprintf("%d_ar",(int)&printArray);
	
	//xTaskCreate(task_sensor_poll,"Task_sensor",STACK_DEPTH,NULL,5,&t1);
	
	vTaskStartScheduler();
}