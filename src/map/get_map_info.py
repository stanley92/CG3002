import requests
import json
import math

########################################
# Map class
# + info : Info
# + location_nodes : Dict(LocationNode)
# + wifi_node : Dict(WifiNode)
#########################################
class Map():
  def __init__(self, info, location_nodes, wifi_nodes):
    self.info = info
    self.location_nodes = location_nodes
    self.wifi_nodes = wifi_nodes

#########################################
# Info class
# + north_at : int
#########################################
class Info():
  def __init__(self, north_at):
    self.north_at = north_at

#########################################
# LocationNode class
# + id : int
# + x : int
# + y : int
# + node_name : str
# + link_to : List(int)
#########################################
class LocationNode():
  def __init__(self, node_id, x, y, node_name, link_to):
    self.id = node_id
    self.x = x
    self.y = y
    self.node_name = node_name
    self.link_to = link_to

#########################################
# WifiNode class
# + id : int
# + x : int
# + y : int
# + node_name : str
# + mac_addr : str
#########################################

class WifiNode():
  def __init__(self, node_id, x, y, node_name, mac_addr):
    self.id = node_id
    self.x = x
    self.y = y
    self.node_name = node_name
    self.mac_addr = mac_addr

#########################################
# Vertex class
# + id : int
# + x : int
# + y : int
# + name : str
# + adjacent : Dict(int)
#########################################
class Vertex():
  def __init__(self, node): # (LocationNode)
    self.id = node.id
    self.x = node.x
    self.y = node.y
    self.name = node.node_name
    self.adjacent = {}

  def addNeighbor(self, node, code):
    self.adjacent[node.id] = _calcDistance(self.x, self.y, node.x, node.y)

  def getConnections(self):
    return self.adjacent.keys()  

#########################################
# Graph class
# + vertices : Dict(Vertex)
# + num_vertices : int
#########################################
class Graph():
  def __init__(self):
    self.vertices = {}
    self.num_vertices = 0

  def addVertex(self, node): # (LocationNode) -> (Vertex)
    self.num_vertices = self.num_vertices + 1
    new_vertex = Vertex(node)
    self.vertices[new_vertex.id] = new_vertex
    return new_vertex

  def getVertex(self, n): # (int) -> (Vertex or None)
    if n in self.vertices:
      return self.vertices[n]
    else: 
      return None

  def getVertices(self):
    return self.vertices.keys()

  def addEdge(self, frm, to): # (int, int)
    if frm not in self.vertices:
      raise KeyError('Vertex not found')
    if to not in self.vertices:
      raise KeyError('Vertex not found')
    fromNode = self.vertices[frm]
    toNode = self.vertices[to]
    cost = _calcDistance(fromNode.x, fromNode.y, toNode.x, toNode.y)
    self.vertices[frm].addNeighbor(self.vertices[to], cost)
    self.vertices[to].addNeighbor(self.vertices[frm], cost)


def _calcDistance(x1, y1, x2, y2):
  return math.sqrt((x1-x2)**2+ (y1-y2)**2)

def downloadMap(params):
  url = "http://showmyway.comp.nus.edu.sg/getMapInfo.php"
  resp = requests.get(url=url, params=params)
  return resp.json()

def parseMapData(data):
  info = Info(data['info']['northAt'])
  location_nodes = {}
  wifi_nodes = {}
  for location in data['map']:
    location_nodes[int(location['nodeId'])] = (
      LocationNode(int(location['nodeId']),
        int(location['x']),
        int(location['y']),
        str(location['nodeName']),
        [int(link) for link in str(location['linkTo']).split(',')]
      )
    )
  for wifi in data['wifi']:
    wifi_nodes[int(wifi['nodeId'])] = (
      WifiNode(int(wifi['nodeId']),
        int(wifi['x']),
        int(wifi['y']),
        str(wifi['nodeName']),
        str(wifi['macAddr'])
      )
    )

  return Map(info, location_nodes, wifi_nodes)

def generateGraph(mapData):
  location_nodes = mapData.location_nodes
  graph = Graph()
  for i in location_nodes:
    graph.addVertex(location_nodes[i])
  for i in location_nodes:
    for link in location_nodes[i].link_to:
      graph.addEdge(location_nodes[i].id, link)
  return graph


def getMapInfo(building, level):
  jsonObject = downloadMap(dict(Building=building, Level=level))
  mapData = parseMapData(jsonObject)
  graph = generateGraph(mapData)
  return graph

g = getMapInfo('COM1',2)
print(g)



