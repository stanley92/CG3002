//need to install keypad library 
//from http://playground.arduino.cc/Code/Keypad
#include <Keypad.h>



/*
pin 30 - 36
*/


const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'#','0','*'}
};

//row and col are adjustable
byte rowPins[ROWS] = {33, 32, 31, 30}; //connect to the row pinouts of the keypad;
byte colPins[COLS] = {36, 35, 34}; //connect to the column pinouts of the keypad;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
  Serial.begin(9600);
}

void loop(){
  char key = keypad.getKey();

  //print out the key that is pressed 
  if (key != NO_KEY){
    Serial.println(key);
  }
}
