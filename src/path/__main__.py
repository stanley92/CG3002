import run_simulation

if __name__ == '__main__':
################################################
# Simulated Event
################################################
  while(1):
    print("Welcome")
    building = 'com1' #str(input('Building Name: '))
    level = 2 #input('Building Level: ')
    point = 'y' #input('Are you on a starting point? ')
    if point == 'y':
      start = 10 #int(input('Start: '))
      end = 16 #int(input('End: '))
      run = run_simulation.Simulation(building, level, start=start, end=end)
      run.start_nav()
    elif point == 'n':
      x_coord = int (input ('Input x-coordinate: '))
      y_coord = int (input ('Input y-coordinate: '))
      heading = float (input ('Input heading: '))
      end = int(input('End: '))
      run = run_simulation.Simulation(building, level, x=x_coord, y=y_coord, end=end, heading = heading)
      run.start_nav()
    
    print("")