from . import find_shortest_path
from . import get_map_info

if __name__ == '__main__':
  building = 'COM1'
  level = 2
  start = 1
  end = 28
  print('Test for map of ' + building + ' level ' + str(level) +'.')
  print('Finding path from node ID ' + str(start) + ' to ' + str(end))
  map_info = get_map_info.getMapInfo(building, level)
  graph = get_map_info.generateGraph(map_info)
  path = find_shortest_path.shortest(graph, start, end)
  print([graph.getVertex(i).name for i in path])