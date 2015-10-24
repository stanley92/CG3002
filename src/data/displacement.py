import math

#import scipy.integrate
#from scipy.integrate import quad

class Displacement():
  def __init__(self, step_size=32):
    # Actual distance calculated
    self.step_size = step_size
    self.dist_cal = 0
    # Distance travelled from current Node
    self.dist_tra = 0
    self.step_travelled = 0
    self.cumulated_step = 0

  def setDistCal(self, v):
    self.dist_cal = v

  def getDistCal(self):
    return self.dist_cal

  def setDistTra(self, v):
    self.dist_tra = v

  def getDistTra(self):
    return self.dist_tra

  def distRemain(self):
    return (self.dist_cal - self.dist_tra)

  def set_current_step(self, cumulated_step):
    self.cumulated_step = cumulated_step

  def get_new_dist_tra_from_step(self):
    step_walked = self.cumulated_step - self.step_travelled
    self.step_travelled = self.cumulated_step
    return step_walked * self.step_size