import math
import get_map_info

class Compass():
  def __init__(self):
    # User's Offset in Degrees
    self.compass_value = 0
    # Fixed angle btw North to curr n next node
    self.angle_NorthToNodes = 0

  def setCompassValue(self, v):
    self.compass_value = v #arduino_compass_value()

  def getCompassValue(self):
    return self.compass_value

  def setNorthToNodes(self,graph,currNodeId,nextNodeId):
    x_curr = graph.getVertex(currNodeId).x
    y_curr = graph.getVertex(currNodeId).y
    x_next = graph.getVertex(nextNodeId).x
    y_next = graph.getVertex(nextNodeId).y
    x_hori = math.fabs(x_curr - x_next)
    y_vert = math.fabs(y_curr - y_next)
    
    # 1st Quadrant
    if x_next > x_curr and y_next > y_curr:
      self.angle_NorthToNodes = 90 - math.degrees(math.atan(y_vert/x_hori))
    # 2nd Quadrant
    elif x_next > x_curr and y_next < y_curr:
      self.angle_NorthToNodes = math.degrees(math.atan(y_vert/x_hori)) + 90
    # 3rd Quadrant
    elif x_next < x_curr and y_next < y_curr:
      self.angle_NorthToNodes = 270 - math.degrees(math.atan(y_vert/x_hori))
    # 4th Quadrant
    elif x_next < x_curr and y_next > y_curr:
      self.angle_NorthToNodes = math.degrees(math.atan(y_vert/x_hori)) + 270
    elif x_next == x_curr and y_next > y_curr:
      self.angle_NorthToNodes = 0
    elif x_next == x_curr and y_next < y_curr:
      self.angle_NorthToNodes = 180
    elif x_next > x_curr and y_next == y_curr:
      self.angle_NorthToNodes = 90
    elif x_next < x_curr and y_next == y_curr:
      self.angle_NorthToNodes = 270
      
  def getNorthToNodes(self):
    return self.angle_NorthToNodes

  def userOffset(self): # - angle , get -ve gives , +ve give
    offset = self.angle_NorthToNodes - self.compass_value
    if offset < 0:
      return 'turn left'#1 # Turn Left
    elif offset > 0:
      return 'turn right'#2 # Turn Right
    else:
      return 'no turn'#0 # No turn
    
##x = Compass()
##g = get_map_info.generateGraph(get_map_info.getMapInfo('COM1',2))

##x.setCompassValue(0)
##print('User angle = ' + str(x.getCompassValue()))
##x.setNorthToNodes(g,5,4)
##print('Node angle = ' + str(x.getNorthToNodes()))
##print(x.userOffset())
