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
  print('')

  try:
    mapInfo = get_map_info.getMapInfo(building, level)
    graph = get_map_info.generateGraph(mapInfo)
    # print(graph.getVertices())

    if not 0<start<=len(graph.getVertices()):
      print('No such start point')

    elif not 0<end<=len(graph.getVertices()):
      print('No such end point')

    else:
      path = find_shortest_path.shortest(graph, start, end)

    print([graph.getVertex(i).name for i in path])
    print('')
    orient = user_orientation.Compass()
    length = (len(path)) - 1
    position = input('Are you at the start point: Y/N: ')
    print('')

    if position == 'Y' or position == 'y':
      orient.setCompassValue(0)

      for i in range (length):
        print('[Step ' + str(i) + ']')
        print(graph.getVertex(path[i]).name + ' -> ' + graph.getVertex(path[i+1]).name)
        print('User angle = ' + str(orient.getCompassValue()))
        orient.setAngleOfNodes(graph,path[i],path[i+1])
        print('Node angle = ' + str(orient.getAngleOfNodes()))
        print(orient.userOffset())
        orient.setCompassValue(orient.getAngleOfNodes())
        print('')

    elif position == 'N' or position == 'n':
      x_coord = int (input ('Input x-coordinate: '))
      y_coord = int (input ('Input y-coordinate: '))
      heading = int (input ('Input heading: '))
      nearestNode = 0
      orient.setCompassValue(heading)
      print('')
      
      for i in range (length):
        total_dist = graph.getVertex(path[i]).adjacent[path[i+1]]
        dist_1 = get_map_info._calcDistance(x_coord,y_coord,graph.getVertex(path[i]).x, graph.getVertex(path[i]).y)
        dist_2 = get_map_info._calcDistance(x_coord,y_coord,graph.getVertex(path[i+1]).x, graph.getVertex(path[i+1]).y)
        if total_dist == dist_1 + dist_2:
          print('Nearest Node: ' + graph.getVertex(path[i+1]).name)
          prevNode = i
          nearestNode = i+1
          break

      print('Current location -> ' + graph.getVertex(path[nearestNode]).name)
      print('User angle = ' + str(orient.getCompassValue()))
      orient.setAngleOfNodes(graph,path[prevNode],path[nearestNode])
      print('Node angle = ' + str(orient.getAngleOfNodes()))
      print(orient.userOffset())
      orient.setCompassValue(orient.getAngleOfNodes())
      print('')
      
      for i in range (nearestNode,length):
        print('[Step ' + str(i) + ']')
        print(graph.getVertex(path[i]).name + ' -> ' + graph.getVertex(path[i+1]).name)
        print('User angle = ' + str(orient.getCompassValue()))
        orient.setAngleOfNodes(graph,path[i],path[i+1])
        print('Node angle = ' + str(orient.getAngleOfNodes()))
        print(orient.userOffset())
        orient.setCompassValue(orient.getAngleOfNodes())
        print('')

  except TypeError:
    print('No such location')
  
  print('')
