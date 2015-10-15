import math
import get_map_info
import os

########################################
# Compass Class
# + compass_value : int
# + angleOfNodes : int
# + northAt : int
########################################
class Compass():
  def __init__(self):
    # User's Offset in Degrees
    self.compass_value = 0
    # Fixed angle btw North to curr n next node
    self.angleOfNodes = 0
    # North angle of map
    self.northAt = 0

  def setNorthAt(self,v):
    self.northAt = v

  def getNorthAt(self):
    return self.northAt

  # Retrieves the value from compass sensor
  def setCompassValue(self, v):
    self.compass_value = v 

  def getCompassValue(self):
    return self.compass_value

  # Sets the angle between two nodes
  def setAngleOfNodes(self,graph,currNodeId,nextNodeId):
    x_curr = graph.getVertex(currNodeId).x
    y_curr = graph.getVertex(currNodeId).y
    x_next = graph.getVertex(nextNodeId).x
    y_next = graph.getVertex(nextNodeId).y
    x_hori = math.fabs(x_curr - x_next)
    y_vert = math.fabs(y_curr - y_next)

    self.angleOfNodes = cal_angle(x_next,x_curr,y_next,y_curr,x_hori,y_vert,self.northAt)

  # Sets the angle between a node and the current coordinates
  def setAngleOfNodeXY(self,graph,x_new,y_new,nextNodeId):
    x_next = graph.getVertex(nextNodeId).x
    y_next = graph.getVertex(nextNodeId).y
    x_hori = math.fabs(x_new - x_next)
    y_vert = math.fabs(y_new - y_next)

    self.angleOfNodes = cal_angle(x_next,x_new,y_next,y_new,x_hori,y_vert,self.northAt)
    
  def getAngleOfNodes(self):
    return self.angleOfNodes

  # Tells the user the shortest rotation to the next node
  def userOffset(self):
    offset = self.angleOfNodes - self.compass_value
    offset_abs = math.fabs(offset)
    #Angle Margin
    if offset < -5: 
      if offset_abs < 180:
        os.system ("say turn left")
        return 'turn left'
      else:
        os.system ("say turn right")
        return 'turn right'
    #Angle Margin
    elif offset > 5:
      if offset_abs < 180:
        os.system ("say turn right")
        return 'turn right'
      else:
        os.system ("say turn left")
        return 'turn left'
    else:
      os.system ("say walk straight")
      return 'walk straight'

def cal_angle(x_next,x_curr,y_next,y_curr,x_hori,y_vert,northAt):
  # 1st Quadrant
  if x_next > x_curr and y_next > y_curr:
    angle = (90 - math.degrees(math.atan(y_vert/x_hori)))
  # 2nd Quadrant
  elif x_next > x_curr and y_next < y_curr:
    angle = math.degrees(math.atan(y_vert/x_hori)) + 90
  # 3rd Quadrant
  elif x_next < x_curr and y_next < y_curr:
    angle = 270 - math.degrees(math.atan(y_vert/x_hori))
  # 4th Quadrant
  elif x_next < x_curr and y_next > y_curr:
    angle = math.degrees(math.atan(y_vert/x_hori)) + 270
  elif x_next == x_curr and y_next > y_curr:
    angle = 0
  elif x_next == x_curr and y_next < y_curr:
    angle = 180
  elif x_next > x_curr and y_next == y_curr:
    angle = 90
  elif x_next < x_curr and y_next == y_curr:
    angle = 270    

  angle -= northAt
  
  if angle >= 360:
      angle -= 360
  elif angle < 0:
    angle += 360

  return angle    


##x = Compass()
##g = get_map_info.generateGraph(get_map_info.getMapInfo('COM1',2))
##
##x.setCompassValue(0)
##print('User angle = ' + str(x.getCompassValue()))
##x.setAngleOfNodes(g,5,4)
##print('Node angle = ' + str(x.getAngleOfNodes()))
##print(x.userOffset())
