from . import find_shortest_path
from . import get_map_info
from . import espeak

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

ANGLE_MARGIN = 10

class Simulation():
  def __init__ (self, prog_controller, orient, displace, speak, building, level, start=None, x=None, y=None, end=None):
   
    self.prog_controller = prog_controller
    self.building = building
    self.level = level
    self.start = start
    self.x = x
    self.y = y
    self.end = end
    map_info = get_map_info.getMapInfo(building, level)
    self.graph = get_map_info.generateGraph(map_info)
    self.path = self._generatePath()
    self.orient = orient
    self.orient.setNorthAt(int(map_info.info.north_at))
    self.displace = displace
    self.speak = speak 
    self.sideStep=0

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

    self.speak.add_speech(3, 'You have reached your destination.')
    # self.say('You have reached your destination!')
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
      if not self.prog_controller.is_program_running_sim():
        print("Run Simulation stopped")
        break
      
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
      if not self.prog_controller.is_program_running_sim():
        print("Run Simulation stopped")
        break
      self.turn()
      newSteps = self.displace.get_new_dist_tra_from_step()
      if newSteps != 0:
        if math.fabs(self.orient.getAngleOfNodes()-self.orient.getCompassValue()) < ANGLE_MARGIN:
          newDistTra = newSteps
          self.sideStep = 0
        else:  
          newDistTra = math.cos( math.radians( math.fabs (self.orient.getAngleOfNodes()-self.orient.getCompassValue() ) ) ) * newSteps
          self.sideStep = math.sin ( math.radians ( self.orient.getAngleOfNodes() - self.orient.getCompassValue() ) ) * newSteps
        # distance to next node
        if newDistTra < 0:
          self.speak.add_speech(3, 'You are in the wrong direction.')
          # self.say('You are in the wrong direction')

        print('Distance total: ' + str(self.displace.getDistCal()))
        print('Distance travelled: ' + str(self.displace.getDistTra()))
        print('Distance to next node: ' + str(self.displace.getDistCal()-self.displace.getDistTra()))
        #newDistTra = int (input ('Distance Travelled:'))

        print('Angle: ' + str((self.orient.getCompassValue())))
        print('Actual Dist: ' + str(newDistTra))

        #self.say("You have walked" + str(int(newDistTra)) + 'cm')
        #os.system ("say You have walked" + str(int(newDistTra)) + 'cm')
        totalDistTra = self.displace.getDistTra() + newDistTra
        if totalDistTra > self.displace.getDistCal(): # reached
          self.displace.setDistTra(self.displace.getDistCal())
        else:
          self.displace.setDistTra(totalDistTra)
        remainingDist = self.displace.getDistCal()-self.displace.getDistTra()

        print('Remaining Dist: ' + str (remainingDist))
        
        #self.say("You have a remaining of" + str(int(self.displace.getDistCal()-self.displace.getDistTra())) + 'cm')
        #os.system ("say You have a remaining of" + str(int(self.displace.getDistCal()-self.displace.getDistTra())) + 'cm')
        
        time.sleep(2)

    if self.sideStep > 0:
      self.speak.add_speech(2, 'Turn Right 90 degrees')
      # self.say('Turn Right 90 degrees')
    elif self.sideStep < 0:
      self.speak.add_speech(2, 'Turn Left 90 degrees')
      # self.say('Turn Left 90 degrees')

    while (math.fabs(self.sideStep) > 100):
      newSteps = self.displace.get_new_dist_tra_from_step()
      if -100 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < -80 :
        #To calculate how much to walk
        print('sideStep' - str(self.sideStep))
        self.sideStep = self.sideStep - newSteps
      elif 80 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < 100:
        #to calculate how much to walk
        print('sideStep' + str(self.sideStep))
        self.sideStep = self.sideStep + newSteps

    # print(len(self.path))
    # print(self.graph.getVertex(self.path[len(self.path)-1]).id)
    if i!=-1 and i<len(self.path)-2 :
      arrivedText = 'You have reached node ' + self.graph.getVertex(self.path[i+1]).name )
      print (str(arrivedText))
      self.speak.add_speech(1, arrivedText)
      self.speak.add_speech(1, arrivedText)
      
      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      #print('You have reached node ' + self.graph.getVertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
      #self.say('You have reached node ' + self.graph.getVertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
    else:
      arrivedText = 'You have reached node ' + self.graph.getVertex(self.path[i+1]).name
      print (str(arrivedText))
      self.speak.add_speech(1, arrivedText)
      self.speak.add_speech(1, arrivedText)

      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      #print('You have reached node ' + self.graph.getVertex(self.path[i+1]).name)
      #self.say('You have reached node ' + self.graph.getVertex(self.path[i+1]).name)

  ################################################
  # Turning algorithim
  ################################################
  def turn(self):
    #### TODO: handledata compassValue (keep reading)
    #### DUMMY: compass Value
    print('Next node angle: ' + str(self.orient.getAngleOfNodes()))
    print('Current direction: ' + str(self.orient.getCompassValue()))
     
    # direction = self.orient.userOffset()
    #print(direction)

    if not (-10 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < 10):
      print ('Wrong direction. ' + self.orient.userOffset())
      self.speak.add_speech(3, self.orient.userOffset())
      walk_straight_added = False
      time.sleep(1.5)
    else 
      if not walk_straight_added:
        walk_straight_added = True
        self.speak.add_speech(3, 'walk straight')
        time.sleep(1.5)

      # self.say(self.orient.userOffset())

  #os.system ("say " + direction)
  #self.say(direction)
  ####
  #print('Node angle = ' + str(self.orient.getAngleOfNodes()))
  #print(self.orient.userOffset())

  #### TODO: motor
  #print('')

  # def say(self, message):
  #   subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 










