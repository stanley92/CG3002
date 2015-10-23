import threading
import time
import subprocess
import RPi.GPIO as GPIO

from . import communication
from . import control
from . import data

from .communication import communication
from .data import sensors
from .data import keypad
from .data import compass
from .data import displacement
from .control import obstacle_detector
from .control import run_simulation
from .control import controller

def data_poll(comm_data_buffer, keypad_data, compass_data, displacement_data, sensors_data, prog_controller):
  while (1):
    try:
      latest_key = comm_data_buffer.buffer.last(0)
      if latest_key!= None:
        print("key in")
        keypad_data.key_in(latest_key)
      if comm_data_buffer.buffer.have_data(1):
        compass_data.setCompassValue(int(comm_data_buffer.buffer.last(1)))
      if comm_data_buffer.buffer.have_data(2):
        displacement_data.set_current_step(int(comm_data_buffer.buffer.last(2)))
      if comm_data_buffer.buffer.have_data(3):
        sensors_data.set_sensor_hand(int(comm_data_buffer.buffer.last(3)))
      if comm_data_buffer.buffer.have_data(4):
        sensors_data.set_sensor_left(int(comm_data_buffer.buffer.last(4)))
      if comm_data_buffer.buffer.have_data(5):
        sensors_data.set_sensor_right(int(comm_data_buffer.buffer.last(5)))
      if comm_data_buffer.buffer.have_data(6):
        sensors_data.set_sensor_left_ankle(int(comm_data_buffer.buffer.last(6)))
      if comm_data_buffer.buffer.have_data(7):
        sensors_data.set_sensor_right_ankle(int(comm_data_buffer.buffer.last(7)))
      if not prog_controller.is_program_running():
        print("data polling stopped")
        break
    except Exception as e:
      print(str(e))
      pass

def say(message):
  subprocess.call('espeak -v%s+%s -s 170 "%s" 2>/dev/null' % ('en-us', 'f4', message), shell=True) 

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(23, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(25, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(22, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(27, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(24, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.output(23, False) #left ankle
  GPIO.output(25, False) #right ankle
  GPIO.output(22, False) #hand
  GPIO.output(27, False) #left 
  GPIO.output(24, False) #right

if __name__ == '__main__':
  setup()
  orient = compass.Compass()
  displace = displacement.Displacement()
  sensors_data = sensors.Sensors()
  keypad_data = keypad.KeypadData()
  prog_controller = controller.Controller()
  prog_controller.start()
  c = communication.Communication(prog_controller)
  while not c.handshaken:
    c.initialise()
  data_poll_thread = threading.Thread(target = data_poll, args = [c, keypad_data, orient, displace, sensors_data, prog_controller])
  data_poll_thread.start() 

  self.say('Welcome')
  
  try :
    while True:
      if keypad_data.data_ready():
        self.say('All data ready. You can start walking.')
        print('ALL DATA READY START THE THING!')
        time.sleep(1)
        building = keypad_data.building #str(input('Building Name: '))
        if building == 1:
          building = 'COM1'
        elif building == 2:
          building = 'COM2'
        level = keypad_data.level #input('Building Level: ')
        if level == 0:
          level = 'B1'
        point = 'y' #input('Are you on a starting point? ')
        if point == 'y':
          start = keypad_data.start_node #int(input('Start: '))
          end = keypad_data.end_node #int(input('End: '))
          run = run_simulation.Simulation(prog_controller, orient, displace, building, level, start=start, end=end)
          run_simulation_thread = threading.Thread(target = run.start_nav, args = [])
          run_simulation_thread.start()
          obstacle_detect = obstacle_detector.ObstacleDetector(prog_controller, sensors_data)
          obstacle_detect_thread_1 = threading.Thread(target = obstacle_detect.inf_loop_1, args = [])
          obstacle_detect_thread_2 = threading.Thread(target = obstacle_detect.inf_loop_2, args = [])
          obstacle_detect_thread_3 = threading.Thread(target = obstacle_detect.inf_loop_3, args = [])
          obstacle_detect_thread_4 = threading.Thread(target = obstacle_detect.inf_loop_4, args = [])
          obstacle_detect_thread_5 = threading.Thread(target = obstacle_detect.inf_loop_5, args = [])
          obstacle_detect_thread_1.start()
          obstacle_detect_thread_2.start()
          obstacle_detect_thread_3.start()
          obstacle_detect_thread_4.start()
          obstacle_detect_thread_5.start()
          keypad_data.clear()
          

          # run.start_nav()
        elif point == 'n':
          x_coord = int (input ('Input x-coordinate: '))
          y_coord = int (input ('Input y-coordinate: '))
          heading = float (input ('Input heading: '))
          end = int(input('End: '))
          run = run_simulation.Simulation(orient, displace, building, level, x=x_coord, y=y_coord, end=end, heading = heading)
          run.start_nav()
      elif keypad_data.function_query_dist():
        remainingDist = displace.getDistCal()-displace.getDistTra()
        print('Remaining Dist: ' + str (remainingDist))
        say('Remaining distance.')
        say(str(remainingDist))
  except KeyboardInterrupt:
    GPIO.cleanup()
    prog_controller.stop()
    try:
      c.thread.join() #polling
    except NameError:
      print('Communication data buffer thread never started')
      pass
    try:
      run_simulation_thread.join() #run simulation
    except NameError:
      print('Run simulation thread never started')
      pass
    try:
      obstacle_detect_thread_2.join() #obs detect
    except NameError:
      print('ObstacleDetector 2 thread never started')
      pass
    try:
      obstacle_detect_thread_3.join() #obs detect
    except NameError:
      print('ObstacleDetector 3 thread never started')
      pass
    try:
      obstacle_detect_thread_4.join() #obs detect
    except NameError:
      print('ObstacleDetector 4 thread never started')
      pass
    try:
      obstacle_detect_thread_5.join() #obs detect
    except NameError:
      print('ObstacleDetector 5 thread never started')
      pass
    try:
      obstacle_detect_thread_1.join() #obs detect
    except NameError:
      print('ObstacleDetector 1 thread never started')
      pass
    try:
      data_poll_thread.join() #polling
    except NameError:
      print('Data polling thread never started')
      pass

def say(self, message):
    subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 
  # print("Welcome")
  # building = 'COM1'
  # level = 2
  # point = 'y'
  # if point == 'y':
  #   start = 1
  #   end = 28
  #   run = run_simulation.Simulation(orient, displace, building, level, start=start, end=end)
  #   run.start_nav()
  # elif point == 'n':
  #   x_coord = int (input ('Input x-coordinate: '))
  #   y_coord = int (input ('Input y-coordinate: '))
  #   heading = float (input ('Input heading: '))
  #   end = int(input('End: '))
  #   run = run_simulation.Simulation(orient, displace, building, level, x=x_coord, y=y_coord, end=end, heading = heading)
  #   run.start_nav()
  
  # print("")
  
  #handshaken

  # building = keypad_data.building #str(input('Building Name: '))
  # if building == 1:
  #   building = 'COM1'
  # elif building == 2:
  #   building = 'COM2'
  # level = keypad_data.level #input('Building Level: ')
  # if level == 0:
  #   level = 'B1'
  # point = 'y' #input('Are you on a starting point? ')
  # if point == 'y':
  #   start = keypad_data.start_node #int(input('Start: '))
  #   end = keypad_data.end_node #int(input('End: '))

  # run = run_simulation.Simulation(orient, displace, building, level, start=start, end=end)
  # run.start_nav()
  # elif point == 'n':
  #   x_coord = int (input ('Input x-coordinate: '))
  #   y_coord = int (input ('Input y-coordinate: '))
  #   heading = float (input ('Input heading: '))
  #   end = int(input('End: '))
  #   run = run_simulation.Simulation(orient, displace, building, level, x=x_coord, y=y_coord, end=end, heading = heading)
  #   run.start_nav()
