from . import get_map_info
import heapq

def dijkstra(graph, start, target):
  inf = float('inf')
  D={i:inf for i in graph.getVertices()}    # distance from start
  P={i:i for i in graph.getVertices()}      # previous
  V={i:False for i in graph.getVertices()}  # visited?

  D[start] = 0

  unvisited_queue = [(D[i], i) for i in graph.getVertices()]
  heapq.heapify(unvisited_queue)

  while len(unvisited_queue):
    uv = heapq.heappop(unvisited_queue)
    current_id = uv[1]
    V[current_id] = True
    current_vertex = graph.getVertex(current_id)

    for next in current_vertex.adjacent:
      if V[next]: continue
      new_distance = D[current_id] + current_vertex.adjacent[next]

      if new_distance < D[next]:
        D[next] = new_distance
        P[next] = current_id
      
    while len(unvisited_queue):
      heapq.heappop(unvisited_queue)

    unvisited_queue = [(D[i], i) for i in graph.getVertices() if not V[i]]
    heapq.heapify(unvisited_queue)

  return (D,P)

def shortest(graph, start, target):
  D,P = dijkstra(graph, start, target)
  path = []
  while 1:
    path.append(target)
    if (target == start): break
    target = P[target]
  path.reverse()
  return path

g = get_map_info.g
p = shortest(g,1,28)
print([g.getVertex(i).name for i in p])