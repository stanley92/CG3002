import find_shortest_path
import get_map_info
import obstacle_detector
import user_displacement
import user_orientation

print('Welcome To FindMyWay15\n')

while(1):
  
  building = input('Building Name: ')
  level = input('Building Level: ')
  start = int(input('Start: '))
  end = int(input('End: '))

  try:
    mapInfo = get_map_info.getMapInfo(building, level)
    graph = get_map_info.generateGraph(mapInfo)
    # print(graph.getVertices())

    if 0<start<=len(graph.getVertices()) and 0<end<=len(graph.getVertices()): 
      path = find_shortest_path.shortest(graph, start, end)
      print([graph.getVertex(i).name for i in path])

      orient = user_orientation.Compass()
      orient.setCompassValue(0)
      length = (len(path)) - 1

      for i in range (length):
        print('[Step ' + str(i) + ']')
        print(graph.getVertex(path[i]).name + ' -> ' + graph.getVertex(path[i+1]).name)
        print('User angle = ' + str(orient.getCompassValue()))
        orient.setNorthToNodes(graph,path[i],path[i+1])
        print('Node angle = ' + str(orient.getNorthToNodes()))
        print(orient.userOffset())
        orient.setCompassValue(orient.getNorthToNodes())

    else:
      if not 0<start<=len(graph.getVertices()):
        print('No such start point')
      if not 0<end<=len(graph.getVertices()):
        print('No such end point')
      
  except TypeError:
    print('No such location')
     
  

  print('')
