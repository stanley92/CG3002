from . import communication
from communication import communication

def main():
  c = communication.Communication()
  c.initialise()
  return c
  
if __name__ == '__main__':
  main()
