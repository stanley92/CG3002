from . import find_shortest_path
from . import get_map_info
import math
import os
import time
import subprocess

#########################################
# simulation class
# + building : str
# + level : int
# + start : int
# + end : int
#########################################

ANGLE_MARGIN = 5

class Simulation():
  def __init__ (self, orient, displace, building, level, start=None, x=None, y=None, end=None, heading=0):
    self.building = building
    self.level = level
    self.start = start
    self.x = x
    self.y = y
    self.end = end
    self.graph = get_map_info.generateGraph(get_map_info.getMapInfo(building, level))
    self.path = self._generatePath()
    self.orient = orient
    self.orient.setNorthAt(heading)
    self.displace = displace

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

  ################################################
  # Determines if the path is VALID
  ################################################
  def _checkValidPath (self,graph):
    if not 0<self.start<=len(self.graph.getVertices()):
      print('No such start point')
      return False
    elif not 0<self.end<=len(self.graph.getVertices()):
      print('No such end point')
      return False
    return True

  ################################################
  # Assigns the path dependent on start or x,y
  ################################################
  def _generatePath (self):
    if self.start!=None:
      if self._checkValidPath(self.graph):
        self.path = find_shortest_path.shortest(self.graph, self.start, self.end)
        return self.path
    elif self.x!=None and self.y!= None:
      closestVertex = get_map_info.getNearestVertex(self.x, self.y, self.graph)
      self.path = find_shortest_path.shortest(self.graph, closestVertex.id, self.end)
      return self.path
    else:
      return None

  ################################################
  # Begin the navigation process
  ################################################
  def start_nav(self):
          
    self.navigate()

    self.say('You have reached your destination!')
    print('You have reached your destination!')

  ################################################
  # Tells the User to turn L/R before walking
  ################################################
  def navigate(self):
    if self.x!=None and self.y!= None:
      self.walk(-1)
      
    length = (len(self.path)) - 1
    
    for i in range(length):
      self.walk(i)
      
  ################################################
  # Walking algoritim
  # When i = -1, specially for random x,y location
  # When i = 0 to path length, runs normally
  # Calls the User to turn 1st before walking
  ################################################
  def walk(self, i):
    if (i == -1):
      self.orient.setAngleOfNodeXY(self.graph,self.x,self.y,self.path[0])
      new_dist = (get_map_info._calcDistance(self.x, self.y, self.graph.getVertex(self.path[0]).x, self.graph.getVertex(self.path[0]).y))
      self.displace.setDistCal(new_dist)
    else:      
      self.orient.setAngleOfNodes(self.graph,self.path[i],self.path[i+1])
      old_dist = self.displace.getDistCal()
      new_dist = (get_map_info._calcDistance(self.graph.getVertex(self.path[i]).x, self.graph.getVertex(self.path[i]).y, self.graph.getVertex(self.path[i+1]).x, self.graph.getVertex(self.path[i+1]).y))
      total_dist = old_dist + new_dist
      self.displace.setDistCal(total_dist)

    while(self.displace.getDistTra() < self.displace.getDistCal()): #havent travel enuf distance
      # turning into correct direction
      self.turn()
      # distance to next node
      print('Distance total: ' + str(self.displace.getDistCal()))
      print('Distance travelled: ' + str(self.displace.getDistTra()))
      print('Distance to next node: ' + str(self.displace.getDistCal()-self.displace.getDistTra()))
      #newDistTra = int (input ('Distance Travelled:'))
      newDistTra = self.displace.get_new_dist_tra_from_step()
      newDistTra = math.cos( math.radians( math.fabs (self.orient.getAngleOfNodes()-self.orient.getCompassValue() ) ) ) * newDistTra
      print('Angle: ' + str((self.orient.getCompassValue())))
      print('Actual Dist: ' + str(newDistTra))

      #self.say("You have walked" + str(int(newDistTra)) + 'cm')
      #os.system ("say You have walked" + str(int(newDistTra)) + 'cm')
      self.displace.setDistTra(self.displace.getDistTra() + newDistTra)
      print('Remaining Dist: ' + str (self.displace.getDistCal()-self.displace.getDistTra()))
      
      #self.say("You have a remaining of" + str(int(self.displace.getDistCal()-self.displace.getDistTra())) + 'cm')
      #os.system ("say You have a remaining of" + str(int(self.displace.getDistCal()-self.displace.getDistTra())) + 'cm')
      time.sleep(1)
    # print(len(self.path))
    # print(self.graph.getVertex(self.path[len(self.path)-1]).id)
    if i!=-1 and i<len(self.path)-2 :
      print('You have reached node ' + self.graph.getVertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
      self.say('You have reached node ' + self.graph.getVertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
    else:
      print('You have reached node ' + self.graph.getVertex(self.path[i+1]).name)
      self.say('You have reached node ' + self.graph.getVertex(self.path[i+1]).name)

  ################################################
  # Turning algorithim
  ################################################
  def turn(self):
    #### TODO: handledata compassValue (keep reading)
    #### DUMMY: compass Value
    print('')
    print('Next node angle: ' + str(self.orient.getAngleOfNodes()))
    print('Current direction: ' + str(self.orient.getCompassValue()))
     
    # direction = self.orient.userOffset()
    #print(direction)

    if not (-5 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < 5):
      print ('You are currently off margin. ' + self.orient.userOffset())
      self.say('You are currently off margin. ' + self.orient.userOffset())

  #os.system ("say " + direction)
  #self.say(direction)
  ####
  #print('Node angle = ' + str(self.orient.getAngleOfNodes()))
  #print(self.orient.userOffset())

  #### TODO: motor
  #print('')

  def say(self, message):
    subprocess.call('espeak -v%s+%s -s70 -k5 %s 2>/dev/null' % ('en', 'f3', message), shell=True) 

  
# Simulation(building, level, start=3, end=6)
# Simulation(building, level, x=200, y=600, end=6)
# DON'T DO THIS:
# Simulation(building, level, start=3, x=200, y=600, end=6)








