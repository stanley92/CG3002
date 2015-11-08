import heapq

def dijkstra(graph, start, target):
  inf = float('inf')
  D={i:inf for i in graph.get_vertices()}    # distance from start
  P={i:i for i in graph.get_vertices()}      # previous
  V={i:False for i in graph.get_vertices()}  # visited?

  D[start] = 0

  unvisited_queue = [(D[i], i) for i in graph.get_vertices()]
  heapq.heapify(unvisited_queue)

  while len(unvisited_queue):
    uv = heapq.heappop(unvisited_queue)
    current_id = uv[1]
    V[current_id] = True
    current_vertex = graph.get_vertex(current_id)

    for next in current_vertex.adjacent:
      if V[next]: continue
      new_distance = D[current_id] + current_vertex.adjacent[next]

      if new_distance < D[next]:
        D[next] = new_distance
        P[next] = current_id
      
    while len(unvisited_queue):
      heapq.heappop(unvisited_queue)

    unvisited_queue = [(D[i], i) for i in graph.get_vertices() if not V[i]]
    heapq.heapify(unvisited_queue)

  return (D,P)

def shortest(graph, start, target):
  print('start find shortest path')
  D,P = dijkstra(graph, start, target)
  print(D,P)
  path = []
  print('before loop')
  while 1:
    path.append(target)
    if (target == start): break
    target = P[target]
  print('after loop')
  path.reverse()
  return path


if __name__ == '__main__':
  import get_map_info
  building = '1'
  level = 2
  start = 1
  end = 28
  print('Test for map of ' + building + ' level ' + str(level) +'.')
  print('Finding path from node ID ' + str(start) + ' to ' + str(end))
  mapInfo = get_map_info.getMapInfo(building, level)
  graph = get_map_info.generateGraph(mapInfo)
  path = shortest(graph, start, end)
  print([graph.get_vertex(i).name for i in path])
