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
  def __init__ (self, building, level, start=None, x=None, y=None, end=None, heading=0):
    self.building = building
    self.level = level
    self.start = start
    self.x = x
    self.y = y
    self.end = end
    self.graph = get_map_info.generateGraph(get_map_info.getMapInfo(building, level))
    if start!= None:
      self.path = self._generatePath()
    self.orient = user_orientation.Compass()
    self.orient.setNorthAt(heading)
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


  def _checkValidPath (self,graph):

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

  def start_nav(self):
    if self.x!=None and self.y!= None:
      closestVertex = get_map_info.getNearestVertex(self.x, self.y, self.graph)
      self.path = find_shortest_path.shortest(self.graph, closestVertex, self.end)     
    self.navigate()

  def navigate(self):
    if self.x!=None and self.y!= None:
      self.orient.setAngleOfNodeXY(graph,self.x,self.y,self.path[0])
      
    length = (len(self.path)) - 1
    self.displace.setDistTra(0)

    for i in range(length):

      self.orient.setAngleOfNodes(self.graph,self.path[i],self.path[i+1])
      old_dist = self.displace.getDistCal()
      
      new_dist = (get_map_info._calcDistance(self.graph.getVertex(self.path[i]).x, self.graph.getVertex(self.path[i]).y, self.graph.getVertex(self.path[i+1]).x, self.graph.getVertex(self.path[i+1]).y))
      print('new distance: ' + str(new_dist))
      total_dist = old_dist + new_dist
      self.displace.setDistCal(total_dist)

      while(self.displace.getDistTra() < self.displace.getDistCal()):
        # turning into correct direction
        self.turn()
        print('Distance total: ' + str(self.displace.getDistCal()))
        print('Distance travelled: ' + str(self.displace.getDistTra()))
        newDistTra = int(input('Enter extra distance travelled: '))
        self.displace.setDistTra(self.displace.getDistTra()+newDistTra)
        


  def turn(self):
    while not(self.orient.getAngleOfNodes() - ANGLE_MARGIN <= self.orient.getCompassValue() <= self.orient.getAngleOfNodes() + ANGLE_MARGIN):
      #### TODO: handledata compassValue (keep reading)
      #### DUMMY: compass Value
      newCompassData = int(input('compassData is (should turn to '+ str(self.orient.getAngleOfNodes()) +') :'))
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
     
    
while(1):
  print("Welcome")
  building = str(input('Building Name: '))
  level = input('Building Level: ')
  point = input('Are you on a starting point? ')
  if point == 'y':
    start = int(input('Start: '))
    end = int(input('End: '))
    run = Simulation(building, level, start=start, end=end)
    run.start_nav()
  elif point == 'n':
    x_coord = int (input ('Input x-coordinate: '))
    y_coord = int (input ('Input y-coordinate: '))
    heading = int (input ('Input heading: '))
    end = int(input('End: '))
    run = Simulation(building, level, x=x_coord, y=y_coord, end=end, heading = heading)
    print(type(run))
    run.start_nav()
  
  print("")
  
# Simulation(building, level, start=3, end=6)
# Simulation(building, level, x=200, y=600, end=6)
# DON'T DO THIS:
# Simulation(building, level, start=3, x=200, y=600, end=6)








