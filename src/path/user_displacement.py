import math
import get_map_info
#import scipy.integrate
#from scipy.integrate import quad

class Displacement():
  def __init__(self):
    # Actual distance calculated
    self.dist_cal = 0
    # Distance travelled from current Node
    self.dist_tra = 0

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


