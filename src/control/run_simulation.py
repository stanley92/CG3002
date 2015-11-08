from . import find_shortest_path
from . import get_map_info
from . import espeak

import math
import os
import time
import subprocess
import json

#########################################
# simulation class
# + building : str
# + level : int
# + start : int
# + end : int
#########################################

ANGLE_MARGIN = 10

class Simulation():
  def __init__ (self, prog_controller, orient, displace, speak, 
    building_start=None, level_start=None, id_start=None, 
    building_end=None, level_end=None, id_end=None,
    x=None, y=None ):
   
    # map information
    self.building_start = building_start
    self.level_start = level_start
    self.id_start = id_start
    self.building_end = building_end
    self.level_end = level_end
    self.id_end = id_end

    # interbuilding information
    self.link_count = 0
    self.links = {}
    
    # global variable for interbuilding navigating
    
    self.current_building = building_start
    self.current_level = level_start
    self.current_link_id = 0
    self.current_link = {}
    self.current_start_id = self.id_start
    self.current_end_id = None
    self.next_start_id = None
    self.is_final_path = False

    # initial path finding
    self._init_path()
    

    # modules to navigate
    self.prog_controller = prog_controller
    self.orient = orient
    
    self.displace = displace
    self.speak = speak 

    # global variables for immediate navigation
    self.side_steps=0
    self.walk_straight_added = False

    self.x = x
    self.y = y

  ################################################
  # Determines if the path is VALID
  ################################################
  def _check_valid_node_id (self, graph, node_start, node_end):
    if not 0<node_start<=len(self.graph.get_vertices()):
      print('No such start point')
      return False
    elif not 0<node_end<=len(self.graph.get_vertices()):
      print('No such end point')
      return False
    return True

  ################################################
  # Init the path dependent on start
  ################################################
  def _init_path (self):
    try:
      # importing the interbuilding links map
      data_file = open("/home/pi/Desktop/CG3002/src/control/links.json")
      global_links = json.load(data_file)
      for navigation in global_links:
        print(navigation)
        if str(navigation['building_start']) == str(self.building_start) \
        and str(navigation['level_start']) == str(self.level_start) \
        and str(navigation['building_end']) == str(self.building_end) \
        and str(navigation['level_end']) == str(self.level_end):
          print('YEPP!!')
          print(navigation)
          self.link_count = int(navigation['link_count'])
          self.links = navigation['links']

        return 
      assert False
    # elif self.x!=None and self.y!= None:
    #   closestVertex = get_map_info.getNearestVertex(self.x, self.y, self.current_graph)
    #   path = find_shortest_path.shortest(self.current_graph, closestVertex.id, self.end)
    #   return path
    except Exception as e:
      print(str(e))
      print('Failed to init Path')
    


  ################################################
  # Find the path within current building
  ################################################
  def _find_next_path(self):
    is_final_path = False

    self.current_link_id = self.current_link_id +1
    self.current_link = self.links[str(self.current_link_id)]
    self.current_building = str(self.current_link['building'])
    self.current_level = str(self.current_link['level'])
    current_map_info = get_map_info.get_map_info(self.current_building, self.current_level)
    self.current_graph = get_map_info.generate_graph(current_map_info)
    self.orient.setNorthAt(int(current_map_info.info.north_at))
    # find start and end in the current map
    if self.current_link_id == 0:
      self.current_start_id = self.id_start
    else:
      self.current_start_id = None
    if self.current_link_id == self.link_count:
      self.current_end_id = self.id_end
      is_final_path = True
    else:
      self.current_end_id = None

    if current_start_id == None: # continue from prev map
      self.current_start_id = self.next_start_id
      self.next_start_id = None

    if current_end_id == None: # have a next map to continue
      next_link = self.links[self.current_link_id+1]
      next_building = str(next_link['building'])
      next_level = str(next_link['level'])
      m_from, m_to = self.current_graph.get_link_to(building=next_building,level=next_level)
      self.current_end_id = m_from
      self.next_start_id = m_to
      
    
    path = find_shortest_path.shortest(self.current_graph, self.current_start_id, self.current_end_id)

    return path, is_final_path

  ################################################
  # Begin the navigation process
  ################################################
  def start_nav(self):
    while not self.is_final_path:
      self.path, self.is_final_path = self._find_next_path()

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
      self.orient.setAngleOfNodeXY(self.current_graph,self.x,self.y,self.path[0])
      new_dist = (get_map_info._calcDistance(self.x, self.y, self.current_graph.get_vertex(self.path[0]).x, self.current_graph.get_vertex(self.path[0]).y))
      self.displace.setDistCal(new_dist)
    else:      
      self.orient.setAngleOfNodes(self.current_graph,self.path[i],self.path[i+1])
      old_dist = self.displace.getDistCal()
      new_dist = (get_map_info._calcDistance(self.current_graph.get_vertex(self.path[i]).x, self.current_graph.get_vertex(self.path[i]).y, self.current_graph.get_vertex(self.path[i+1]).x, self.current_graph.get_vertex(self.path[i+1]).y))
      total_dist = old_dist + new_dist
      self.displace.setDistCal(total_dist)

    while(self.displace.getDistTra() < self.displace.getDistCal()): #havent travel enuf distance
      
      if not self.prog_controller.is_program_running_sim():
        print("Run Simulation stopped")
        break

      self.turn()

      newSteps = self.displace.get_new_dist_tra_from_step()
      if newSteps != 0:
        if math.fabs(self.orient.getAngleOfNodes()-self.orient.getCompassValue()) < ANGLE_MARGIN:
          newDistTra = newSteps
          self.side_steps = 0
        else:  
          newDistTra = math.cos( math.radians( math.fabs (self.orient.getAngleOfNodes()-self.orient.getCompassValue() ) ) ) * newSteps
          self.side_steps = math.sin ( math.radians ( self.orient.getAngleOfNodes() - self.orient.getCompassValue() ) ) * newSteps # distance to next node

        if newDistTra < 0:
          self.speak.add_speech(3, 'You are in the wrong direction.')

        print('Distance total: ' + str(self.displace.getDistCal()))
        print('Distance travelled: ' + str(self.displace.getDistTra()))
        print('Distance to next node: ' + str(self.displace.getDistCal()-self.displace.getDistTra()))
        

        print('Angle: ' + str((self.orient.getCompassValue())))
        print('Actual Dist: ' + str(newDistTra))

        totalDistTra = self.displace.getDistTra() + newDistTra
        if totalDistTra > self.displace.getDistCal(): # reached
          self.displace.setDistTra(self.displace.getDistCal())
        else:
          self.displace.setDistTra(totalDistTra)
        remainingDist = self.displace.getDistCal()-self.displace.getDistTra()

        print('Remaining Dist: ' + str (remainingDist))
        
        time.sleep(1)

    if self.side_steps > 0:
      self.speak.add_speech(2, 'Turn Right 90 degrees')
      # self.say('Turn Right 90 degrees')
    elif self.side_steps < 0:
      self.speak.add_speech(2, 'Turn Left 90 degrees')
      # self.say('Turn Left 90 degrees')

    while (math.fabs(self.side_steps) > 100):
      newSteps = self.displace.get_new_dist_tra_from_step()
      if -100 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < -80 :
        #To calculate how much to walk
        print('side_steps' - str(self.side_steps))
        self.side_steps = self.side_steps - newSteps
      elif 80 < self.orient.getAngleOfNodes() - self.orient.getCompassValue() < 100:
        #to calculate how much to walk
        print('side_steps' + str(self.side_steps))
        self.side_steps = self.side_steps + newSteps

    # print(len(self.path))
    # print(self.current_graph.get_vertex(self.path[len(self.path)-1]).id)
    if i!=-1 and i<len(self.path)-2 :
      arrivedText = 'You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name
      print (str(arrivedText))
      self.speak.add_speech(1, arrivedText)
      self.speak.add_speech(1, arrivedText)
      
      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      #print('You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
      #self.say('You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name + ' ' + self.orient.userOffset())
    else:
      arrivedText = 'You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name 
      print (str(arrivedText))
      self.speak.add_speech(1, arrivedText)
      self.speak.add_speech(1, arrivedText)

      # subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True)
      #print('You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name)
      #self.say('You have reached node ' + self.current_graph.get_vertex(self.path[i+1]).name)

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
      self.walk_straight_added = False
      time.sleep(1.5)
    else:
      if not self.walk_straight_added:
        self.walk_straight_added = True
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










