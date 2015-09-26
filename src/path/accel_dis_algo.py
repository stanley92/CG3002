##  unsigned long time_New = millis();
##  unsigned long time_Delta = time_New - time;
##
##  ...
##
##  // estimate the average acceleration since the previous sample, by averaging the two samples
##  long accel_Avg = (accel + accel_New) / 2;
##
##  // integrate the average accel and add it to the previous speed to calculate the new speed
##  long speed_New = speed + (accel_Avg  * time_Delta);
##
##  estimate the average speed since the previous sample, by averaging the two speeds
##  long speed_Avg = (speed + speed_New) / 2;
##
##  // integrate the average speed and add it to the previous displacement to get the new displacement
##  long displacement_New = displacement + (speed_Avg * time_Delta);
##
##  time = time_New;
##  speed = speed_New ;
##  displacement = displacement_New;


class accelDisplaceAlgo():
  def __init__(self):
    time_New = 0
    time_Delta = 0
    accel = 0
    accel_New = 0
    accel_Avg = 0
    speed = 0
    speed_New = 0
    speed_Avg = 0
    displacement = 0
    displacement_New = 0
    displacement_Avg = 0

  def settime_New(self, v):
    self.time_New = v

  def gettime_New(self):
    return self.time_New

  def settime_Delta(self, time_New, time):
    self.time_Delta = time_New - time

  def gettime_Delta(self):
    return self.time_Delta

  def setAccel(self, accel_New):
    self.accel = accel_New

  def getAccel(self):
    return self.accel

  def setaccel_New(self, v):
    self.accel_New = v

  def getaccel_New(self):
    return self.accel_New

  def setaccel_Avg(self, accel, accel_New):
    self.accel_Avg = (accel + accel_New) / 2

  def getaccel_Avg(self):
    return self.accel_Avg

  def setSpeed(self, speed_New):
    self.speed = speed_New

  def getSpeed(self):
    return self.speed

  def setspeed_New(self, speed, time_Delta, accel_Avg):
    self.speed_New = speed + (time_Delta * accel_Avg)

  def getspeed_New(self):
    return self.speed_New

  def setspeed_Avg(self, speed, speed_New):
    self.speed_Avg = (speed + speed_New) / 2

  def getspeed_Avg(self):
    return self.speed_Avg
  
  def setDisplacement(self, displacement_New):
    self.displacement = displacement_New

  def getDisplacemnet(self):
    return self.displacement

  def setdisplacement_New(self, displacement, speed_Avg, time_Delta):
    self.displacement_New = displacement + (speed_Avg * time_Delta)

  def getdisplacement_New(self):
    return self.displacement_New

  def setdisplacement_Avg(self, displacement, displacement_New):
    self = (displancement + displacement_New) / 2

  def getdisplacement_Avg(self):
    return self.displacement_Avg

  
