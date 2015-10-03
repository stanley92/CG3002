#########################################
# simulation class
# + building : str
# + level : int
# + start : int
# + end : int
#########################################
import find_shortest_path
import get_map_info
import obstacle_detector
import user_displacement
import user_orientation
import math

ANGLE_MARGIN = 5

class Simulation():
  def __init__ (self, building, level, start=None, x=None, y=None, end=None):
    self.building = building
    self.level = level
    self.start = start
    self.x = x
    self.y = y
    self.end = end
    self.self.graph = get_map_info.generateGraph(building, level)
    self.path = self._generatePath()
    self.orient = user_orientation.Compass()
    self.displace = user_displacement.Displacement()

  def setBuilding (self, building): 
    self.building = building

  def getBuilding (self): 
    return self.building

  def setLevel (self, level): 
    self.level = level

  def getLevel (self): 
    return self.level

  def setStart (self, start): 
    self.start = start

  def getStart (self): 
    return self.start

  def setEnd (self, end): 
    self.end = end

  def getEnd (self): 
    return self.end


  def _checkValidPath (self):

    if not 0<self.start<=len(self.graph.getVertices()):
      print('No such start point')
      return False
    elif not 0<self.end<=len(self.graph.getVertices()):
      print('No such end point')
      return False
    return True

  def _generatePath (self):
    if self._checkValidPath(self.graph):
      self.path = find_shortest_path.shortest(self.graph, self.start, self.end)
      return self.path
    else:
      return None

  def start(self):
    if x!=None and y!= None:
      closestVertex = get_map_info.getNearestVertex(coordinate_x, coordinate_y, self.graph)
      path = find_shortest_path.shortest(self.graph, closestVertex, self.end)
    elif start != None:
      path = self.path
    else:
      return None
    return path

  def navigate(self):
    if x!=None and y!= None:
      self.orient.setAngleOfNodeXY(graph,x_coord,y_coord,path[0])
      length = (len(path)) - 1
      self.displace.setDistTra(0)

    for i in range (1,length):

      self.orient.setAngleOfNodes(graph,path[i],path[i+1])
      old_value = self.displace.getDistCal()
      new_value = (get_map_info._calcDistance(graph.getVertex(i).x, graph.getVertex(i+1).x, graph.getVertex(i).y, graph.getVertex(i+1).y))
      total_value = old_value + new_value
      self.displace.setDistCal(total_value)

      while(self.displace.getDistTra() < self.displace.getDistCal()):
              # turning into correct direction
              self.turn()

              # walk
              newDistTra = int(input('distance total' + str(distance) + ', enter distance travelled: '))
              self.displace.setDistTra(newDistTra)


  def turn(self):
    while (self.orient.getAngleOfNodes() - ANGLE_MARGIN \
    <= self.orient.getCompassValue() \
    <= self.orient.getAngleOfNodes() + ANGLE_MARGIN):
      #### TODO: handledata compassValue (keep reading)
      #### DUMMY: compass Value
      newCompassData = int(input('compassData is (should turn to '+ self.orient.getAngleOfNodes() +') :'))
      self.orient.setCompassValue(newCompassData)
      ####
      #### TODO: motor buzz
      #### DUMMY:
      direction = self.orient.userOffset()
      print(direction);
      ####


    #print('Node angle = ' + str(self.orient.getAngleOfNodes()))
    #print(self.orient.userOffset())

    #### TODO: motor



# Simulation(building, level, start=3, end=6)
# Simulation(building, level, x=200, y=600, end=6)
# DON'T DO THIS:
# Simulation(building, level, start=3, x=200, y=600, end=6)








