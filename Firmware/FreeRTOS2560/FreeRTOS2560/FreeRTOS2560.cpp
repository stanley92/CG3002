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

//Tasks flash LEDs at Pins 12 and 13 at 1Hz and 2 Hz respectively
void task1(void *p)
{
	while(1)
	{
		digitalWrite(13,HIGH);
		vTaskDelay(500); //Delay for 500ticks. Since each tick is 1ms,
							//this delays for 500ms
		digitalWrite(13,LOW);
		vTaskDelay(500);
	}
	
}
void task2(void* p)
{
	
	while(1)
	{
		digitalWrite(12,HIGH);
		vTaskDelay(250);
		digitalWrite(12,LOW);
		vTaskDelay(250);
	}
}
#define STACK_DEPTH 64

void vApplicationIdleHook()
{
	//Do nothing
}

int main(void)
{
	init();
	pinMode(12,OUTPUT);
	pinMode(13,OUTPUT);
	TaskHandle_t t1,t2;
	
	//Create tasks
	xTaskCreate(task1, "Task 1", STACK_DEPTH, NULL, 6, &t1);
	xTaskCreate(task2, "Task 2", STACK_DEPTH, NULL, 5, &t2);
	
	vTaskStartScheduler();
}