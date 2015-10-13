//AccelerometerCompassModule
//ACSerial


/*
The sensor outputs provided by the library are the raw 16-bit values
obtained by concatenating the 8-bit high and low accelerometer and
magnetometer data registers. They can be converted to units of g and
gauss using the conversion factors specified in the datasheet for your
particular device and full scale setting (gain).

Example: An LSM303D gives a magnetometer X axis reading of 1982 with
its default full scale setting of +/- 4 gauss. The M_GN specification
in the LSM303D datasheet (page 10) states a conversion factor of 0.160
mgauss/LSB (least significant bit) at this FS setting, so the raw
reading of -1982 corresponds to 1982 * 0.160 = 317.1 mgauss =
0.3171 gauss.

In the LSM303DLHC, LSM303DLM, and LSM303DLH, the acceleration data
registers actually contain a left-aligned 12-bit number, so the lowest
4 bits are always 0, and the values should be shifted right by 4 bits
(divided by 16) to be consistent with the conversion factors specified
in the datasheets.

Example: An LSM303DLH gives an accelerometer Z axis reading of -16144
with its default full scale setting of +/- 2 g. Dropping the lowest 4
bits gives a 12-bit raw value of -1009. The LA_So specification in the
LSM303DLH datasheet (page 11) states a conversion factor of 1 mg/digit
at this FS setting, so the value of -1009 corresponds to -1009 * 1 =
1009 mg = 1.009 g.
*/



#include <Wire.h>
#include <LSM303.h>

LSM303 compass;

char report[80];

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
}

void loop()
{
  compass.read();
float Xa_print, Ya_print, Za_print;
Xa_print = compass.a.x/16.0; //Acceleration data registers contain a left-aligned 12-bit number, so values should be shifted right by 4 bits (divided by 16)
Ya_print = compass.a.y/16.0; //unit is in cm/s2
Za_print = compass.a.z/16.0;

//to determine a step, the +zAccel should be -800  and -zAccel should be -1300 

Serial.print(Xa_print); Serial.print(" "); Serial.print(Ya_print); Serial.print(" "); Serial.println(Za_print);
delay(125);
  delay(100);
}