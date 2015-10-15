import run_simulation

if __name__ == '__main__':
################################################
# Simulated Event
################################################
  while(1):
    print("Welcome")
    building = str(input('Building Name: '))
    level = input('Building Level: ')
    point = input('Are you on a starting point? ')
    if point == 'y':
      start = int(input('Start: '))
      end = int(input('End: '))
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