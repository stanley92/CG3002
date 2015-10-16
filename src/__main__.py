import threading

# from . import communication
from . import control
# from . import data

# from .communication import communication
# from .data import sensors
# from .data import keypad
from .data import compass
from .data import displacement
from .control import obstacle_detector
from .control import run_simulation


def data_poll(comm_data_buffer, keypad_data, compass_data, displacement_data, sensors_data):
  while (1):
    latest_keypad_data = comm_data_buffer.buffer.last(0)
    if (latest_keypad_data!= None):
      keypad_data.key_in(latest_keypad_data)
    compass_data.setCompassValue(comm_data_buffer.buffer.last(1))
    displacement_data.set_current_step(comm_data_buffer.buffer.last(2))

    sensors_data.set_sensor_left(comm_data_buffer.buffer.last(3))
    sensors_data.set_sensor_down(comm_data_buffer.buffer.last(4))
    sensors_data.set_sensor_front(comm_data_buffer.buffer.last(5))
    sensors_data.set_sensor_right(comm_data_buffer.buffer.last(6))
    sensors_data.set_sensor_leg(comm_data_buffer.buffer.last(7))


if __name__ == '__main__':

  orient = compass.Compass()
  displace = displacement.Displacement()
  # sensors_data = sensors.Sensors()
  # keypad_data = keypad.KeypadData()
  print("Welcome")
  building = str(input('Building Name: '))
  level = input('Building Level: ')
  point = input('Are you on a starting point? ')
  if point == 'y':
    start = int(input('Start: '))
    end = int(input('End: '))
    run = run_simulation.Simulation(orient, displace, building, level, start=start, end=end)
    run.start_nav()
  elif point == 'n':
    x_coord = int (input ('Input x-coordinate: '))
    y_coord = int (input ('Input y-coordinate: '))
    heading = float (input ('Input heading: '))
    end = int(input('End: '))
    run = run_simulation.Simulation(orient, displace, building, level, x=x_coord, y=y_coord, end=end, heading = heading)
    run.start_nav()
  
  print("")
  # c = communication.Communication()
  # while not c.handshaken:
  #   c.initialise()

  #handshaken
  # data_poll_thread = threading.Thread(target = data_poll, args = [c, keypad_data, orient, displace, sensors_data])

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