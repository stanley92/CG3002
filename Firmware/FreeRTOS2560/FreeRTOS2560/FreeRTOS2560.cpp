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
/*gyro code*/

/*sonar code*/
#define TRIGGER_PIN  22  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     24  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
/*sonar code*/

/*Keypad code*/
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
/*keypad code*/

char data[12];
/*keypad code*/

/*IR code*/
#define sensorIR 15               //Must be an analog pin
float sensorValue, inches, cm;    //Must be of type float for pow()
/*IR code*/

/*gyro code*/
L3G gyro;
/*gyro code*/

/*baro code*/
LPS ps;
/*baro code*/

/*accelerometer code*/
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
int freeRAM () {
	extern int __heap_start;
	extern int *__brkval;
	int v;
	if(__brkval == 0){
		return (int)&v - (int)&__heap_start;
	}
	return (int)&v - (int)__brkval;
	//return ((int) &v) – ((__brkval == 0 ? (int) &__heap_start : (int) __brkval));
}

void printArray(void* p){
	int i;
	data [1] = 123;
	char canRead = '0';
	while(1){
		if(Serial.available()){
			canRead = Serial.read();
		}
		if(canRead -'0'){
			//for(i = 1;i<10;i++){
				Serial.println(/*data[1]*/213);
				Serial.print('\r');
		//	}
			Serial.println(freeRAM());
			canRead = '0';
		}
		vTaskDelay(500);
	}
}

void setup(){
	
	Serial.begin(115200);
	Wire.begin(); //gyro code
	gyro.init();//gyro code
	gyro.enableDefault(); //gyro code
	ps.enableDefault(); //baro code
		
		/*accelerometer code*/
		compass.init();
		compass.enableDefault();
		/*accelerometer code*/
		/*sonar code*/
		pinMode(TRIGGER_PIN, OUTPUT);
		pinMode(ECHO_PIN, INPUT);
		/*sonar code*/
		 
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
		dprintf("%d is pressure, %d is altitude, %d is temperature",(int) pressure,(int)  altitude,(int) temperature);
		//dprintf("%d alt",(int)altitude);
		/*
		Serial.print("p: ");
		Serial.print(pressure);
		Serial.print(" mbar\ta: ");
		Serial.print(altitude);
		Serial.print(" m\tt: ");
		Serial.print(temperature);
		Serial.println(" deg C");
*/		delay(1000);
		vTaskDelay(1000);
		//delay(100);
	}
	/*baro code*/
}
void task_keypad(void* p){
	
	/*KeyPad code*/
	while(1)
	{
		char key = keypad.getKey();

		//print out the key that is pressed
		if (key != NO_KEY){
			dprintf("%c",key);
		}
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
		Serial.print("1");
		//delay(1000);
		vTaskDelay(3000);
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
	while(1){
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
		//dprintf("hello");
		// dprintf("G ");
		//dprintf("X: ");
		//dprintf("%d",(int)gyro.g.x);
		//	dprintf(" Y: ");
		//dprintf("%d",(int)gyro.g.y);
		// dprintf(" Z: ");
		//dprintf("%d",(int)gyro.g.z);
		//dprintf("%d",(int)gyro.g.x);
		//dprintf("%d",gyro.g.x);
		//delay(1000);
		dprintf("X is %d, Y is %d, Z is %d", (int)gyro.g.x,(int)gyro.g.y,(int)gyro.g.z);
		//delay(1000);
		vTaskDelay(2000);
		
	}

	/* gyro code*/
}
void task2(void* p)
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
}
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
void task_poll_sensor(void* p){
	
	
}
#define STACK_DEPTH 128//64

void vApplicationIdleHook()
{
	//Do nothing
}

int main(void)
{
	init();
	setup();
	pinMode(12,OUTPUT);
	pinMode(13,OUTPUT);
	TaskHandle_t t1,t2;
	
	
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
//	xTaskCreate(printArray, "Task Gyro", STACK_DEPTH,NULL,0,&t1);
	//xTaskCreate(task_sonar1,"task sornar",STACK_DEPTH,NULL,5,&t2);
	//xTaskCreate(task_baro, "Task Gyro", STACK_DEPTH,NULL,5,&t1);
	//xTaskCreate(task_ir,"Task Accelerometer", STACK_DEPTH, NULL,6,&t2);
	xTaskCreate(task_poll_sensor,"Task_sensor",STACK_DEPTH,NULL,5,&t1);
	
	vTaskStartScheduler();
}