import math
import get_map_info

class Compass():
  def __init__(self):
    # User's Offset in Degrees
    self.compass_value = 0
    # Fixed angle btw North to curr n next node
    self.angleOfNodes = 0

  def setCompassValue(self, v):
    self.compass_value = v #arduino_compass_value()

  def getCompassValue(self):
    return self.compass_value

  def setAngleOfNodes(self,graph,currNodeId,nextNodeId,northAt):
    x_curr = graph.getVertex(currNodeId).x
    y_curr = graph.getVertex(currNodeId).y
    x_next = graph.getVertex(nextNodeId).x
    y_next = graph.getVertex(nextNodeId).y
    x_hori = math.fabs(x_curr - x_next)
    y_vert = math.fabs(y_curr - y_next)
    
    # 1st Quadrant
    if x_next > x_curr and y_next > y_curr:
      self.angleOfNodes = 90 - math.degrees(math.atan(y_vert/x_hori))
    # 2nd Quadrant
    elif x_next > x_curr and y_next < y_curr:
      self.angleOfNodes = math.degrees(math.atan(y_vert/x_hori)) + 90
    # 3rd Quadrant
    elif x_next < x_curr and y_next < y_curr:
      self.angleOfNodes = 270 - math.degrees(math.atan(y_vert/x_hori))
    # 4th Quadrant
    elif x_next < x_curr and y_next > y_curr:
      self.angleOfNodes = math.degrees(math.atan(y_vert/x_hori)) + 270
    elif x_next == x_curr and y_next > y_curr:
      self.angleOfNodes = 0
    elif x_next == x_curr and y_next < y_curr:
      self.angleOfNodes = 180
    elif x_next > x_curr and y_next == y_curr:
      self.angleOfNodes = 90
    elif x_next < x_curr and y_next == y_curr:
      self.angleOfNodes = 270

    self.angleOfNodes -= northAt
    if self.angleOfNodes >= 360:
      self.angleOfNodes -= 360
      
  def getAngleOfNodes(self):
    return self.angleOfNodes

  def userOffset(self): # - angle , get -ve gives , +ve give
    offset = self.angleOfNodes - self.compass_value
    offset_abs = math.fabs(offset)
    if offset < 0:
      if offset_abs < 180:
        return 'turn left'
      else:
        return 'turn right'
    elif offset > 0:
      if offset_abs < 180:
        return 'turn right'
      else:
        return 'turn left'
    else:
      return 'no turn'
    
##x = Compass()
##g = get_map_info.generateGraph(get_map_info.getMapInfo('COM1',2))
##
##x.setCompassValue(0)
##print('User angle = ' + str(x.getCompassValue()))
##x.setAngleOfNodes(g,5,4)
##print('Node angle = ' + str(x.getAngleOfNodes()))
##print(x.userOffset())
