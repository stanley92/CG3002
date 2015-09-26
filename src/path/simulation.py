

import find_shortest_path
import get_map_info
import obstacle_detector
import user_displacement
import user_orientation

building = 'com1'
level = 2
start = 1
end = 28
mapInfo = get_map_info.getMapInfo(building, level)
graph = get_map_info.generateGraph(mapInfo)
path = find_shortest_path.shortest(graph, start, end)
print([graph.getVertex(i).name for i in path])

orient = user_orientation.Compass()
orient.setCompassValue(0)
length = (len(path)) - 1
for i in range (length):
  print('LOOP ' + str(i))
  print(graph.getVertex(path[i]).name + ' -> ' + graph.getVertex(path[i+1]).name)
  print('User angle = ' + str(orient.getCompassValue()))
  orient.setNorthToNodes(graph,path[i],path[i+1])
  print('Node angle = ' + str(orient.getNorthToNodes()))
  print(orient.userOffset())
  orient.setCompassValue(orient.getNorthToNodes())
