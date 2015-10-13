import math
import get_map_info
#import scipy.integrate
#from scipy.integrate import quad

class walk():
  def __init__(self):
    # Actual distance calculated
    self.dist_cal = 0
    # Distance travelled from current Node
    self.dist_tra = 0

  def setDistCal(self,graph,currNode,nextNode):
    x_curr = graph.getVertex(currNodeId).x
    y_curr = graph.getVertex(currNodeId).y
    x_next = graph.getVertex(nextNodeId).x
    y_next = graph.getVertex(nextNodeId).y

    self.dist_cal = sqrt(pow(x_curr-x_next,2) + pow(y_curr-y_next,2))

  def calDistTra(v):
    # integrate accelerometer twice get displacement
    # add to dist_tra
    # if dis_tra >= dis_cal --> stop
    # if dis_tra < dis_cal --> walk
    accel = v


