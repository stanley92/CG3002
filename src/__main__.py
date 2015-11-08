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
from .control import espeak

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
        sensors_data.set_sensor_front(int(comm_data_buffer.buffer.last(6)))
      if comm_data_buffer.buffer.have_data(7):
        sensors_data.set_sensor_right_ankle(int(comm_data_buffer.buffer.last(7)))
      if comm_data_buffer.buffer.have_data(8):
        sensors_data.set_sensor_front(int(comm_data_buffer.buffer.last(8)))
      if not prog_controller.is_program_running_all():
        print("data polling stopped")
        break
    except Exception as e:
      print(str(e))
      pass



# def say(message):
#   subprocess.call('espeak -v%s+%s -s 170 "%s" 2>/dev/null' % ('en-us', 'f4', message), shell=True) 

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(23, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(25, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(22, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(27, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(24, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
  GPIO.output(23, False) #hand
  GPIO.output(25, False) #right ankle
  GPIO.output(22, False) #front
  GPIO.output(27, False) #left 
  GPIO.output(24, False) #right

if __name__ == '__main__':
  print("Welcome")
  setup()
  orient = compass.Compass()
  displace = displacement.Displacement()
  sensors_data = sensors.Sensors()
  prog_controller = controller.Controller()
  speak = espeak.Espeak(prog_controller)
  keypad_data = keypad.KeypadData(speak)
  prog_controller.start_all()
  c = communication.Communication(prog_controller)
  while not c.handshaken:
    c.initialise()
  speak_thread = threading.Thread(target = speak.speak, args = [])
  speak_thread.start()
  data_poll_thread = threading.Thread(target = data_poll, args = [c, keypad_data, orient, displace, sensors_data, prog_controller])
  data_poll_thread.start() 
  # data_poll_test_thread = threading.Thread(target = data_poll_test, args = [c, keypad_data, orient, displace, sensors_data, prog_controller])
  # data_poll_test_thread.start() 
  speak.add_speech(3, 'Welcome')
  # subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', 'Welcome'), shell=True)

  try :
    while True:
      if keypad_data.data_ready():
        speak.add_speech(3, 'Setting Data')
        # subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', 'Setting Data'), shell=True)
        print('ALL DATA READY START THE THING!')
        time.sleep(1)
        start_building = keypad_data.start_building 
        start_level = keypad_data.start_level
        end_building = keypad_data.end_building
        end_level = keypad_data.end_level
        start_node = keypad_data.start_node
        end_node = keypad_data.end_node
        try:
          displace.initialise()
          run = run_simulation.Simulation(prog_controller, orient, displace, speak, 
            building_start=start_building, level_start = start_level, start=start_node,
            building_end=end_building, level_end = end_level, end=end_node)
          run_simulation_thread = threading.Thread(target = run.start_nav, args = [])
          run_simulation_thread.start()
          obstacle_detect = obstacle_detector.ObstacleDetector(prog_controller, sensors_data, speak)
          obstacle_detect_thread1 = threading.Thread(target = obstacle_detect.inf_loop1, args = [])
          obstacle_detect_thread2 = threading.Thread(target = obstacle_detect.inf_loop2, args = [])
          obstacle_detect_thread3 = threading.Thread(target = obstacle_detect.inf_loop3, args = [])
          obstacle_detect_thread4 = threading.Thread(target = obstacle_detect.inf_loop4, args = [])
          obstacle_detect_thread5 = threading.Thread(target = obstacle_detect.inf_loop5, args = [])
          obstacle_detect_thread1.start()
          obstacle_detect_thread2.start()
          obstacle_detect_thread3.start()
          obstacle_detect_thread4.start()
          obstacle_detect_thread5.start()
          keypad_data.clear()
          speak.add_speech (3, 'All data ready. You can start walking.')
          # subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', 'All data ready. You can start walking.'), shell=True)
        except Exception as e:
          print(str(e))
          print('Some error. Key in again')
          speak.add_speech(3, 'Some error. Key in again')
          prog_controller.stop_sim()
          try:
            run_simulation_thread.join() #run simulation
          except NameError:
            print('Run simulation thread never started')
            pass
          try:
            obstacle_detect_thread1.join()
            obstacle_detect_thread2.join()
            obstacle_detect_thread3.join()
            obstacle_detect_thread4.join()
            obstacle_detect_thread5.join()
          except NameError:
            print('ObstacleDetector thread never started')
            pass
          try:
            speak_thread.join() #obs detect
          except NameError:
            print('Speak thread never started')
            pass
          prog_controller.start_sim()
    
      elif keypad_data.function_query_dist():
        remainingDist = displace.getDistCal()-displace.getDistTra()
        print('Remaining Dist: ' + str (remainingDist))
        speak.add_speech(3, 'Remaining distance ' + int(remainingDist))
        # say('Remaining distance.')
        # say(str(remainingDist))
      elif keypad_data.signal_prog_reset():
        prog_controller.stop_sim()
        try:
          run_simulation_thread.join() #run simulation
        except NameError:
          print('Run simulation thread never started')
          pass
        try:
          obstacle_detect_thread1.join() #obs detect
          obstacle_detect_thread2.join() #obs detect
          obstacle_detect_thread3.join() #obs detect
          obstacle_detect_thread4.join() #obs detect
          obstacle_detect_thread5.join() #obs detect
        except NameError:
          print('ObstacleDetector thread never started')
          pass
        prog_controller.start_sim()
  except KeyboardInterrupt:
    GPIO.cleanup()
    prog_controller.stop_all()
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
      obstacle_detect_thread1.join() #obs detect
      obstacle_detect_thread2.join() #obs detect
      obstacle_detect_thread3.join() #obs detect
      obstacle_detect_thread4.join() #obs detect
      obstacle_detect_thread5.join() #obs detect
    except NameError:
      print('ObstacleDetector thread never started')
      pass
    try:
      speak_thread.join() #run simulation
    except NameError:
      print('Speak thread never started')
      pass
    try:
      data_poll_thread.join() #polling
      # data_poll_test_thread.join() #polling
    except NameError:
      print('Data polling thread never started')
      pass
