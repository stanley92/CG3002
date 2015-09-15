import requests
import json


class Map():
  def __init__(self, info, locationMap, wifiMap):
    self.info = info
    self.nodeMap = locationMap
    self.wifi = wifiMap

class Info():
  def __init__(self, northAt):
    self.northAt = northAt

class LocationNode():
  def __init__(self, nodeId, x, y, nodeName, linkTo):
    self.nodeId = nodeId
    self.x = x
    self.y = y
    self.nodeName = nodeName
    self.linkTo = linkTo

class WifiNode():
  def __init__(self, nodeId, x, y, nodeName, macAddr):
    self.nodeId = nodeId
    self.x = x
    self.y = y
    self.nodeName = nodeName
    self.macAddr = macAddr

def downloadMap(params):
  url = "http://showmyway.comp.nus.edu.sg/getMapInfo.php"
  resp = requests.get(url=url, params=params)
  return resp.json()

def parseMapData(data):
  info = Info(data['info']['northAt'])
  locationNodes = []
  wifiNodes = []
  for location in data['map']:
    locationNodes.append(
      LocationNode(int(location['nodeId']),
        int(location['x']),
        int(location['y']),
        str(location['nodeName']),
        [int(link) for link in str(location['linkTo']).split(',')]
      )
    )
  for wifi in data['wifi']:
    wifiNodes.append(
      WifiNode(int(location['nodeId']),
        int(wifi['x']),
        int(wifi['y']),
        str(wifi['nodeName']),
        str(wifi['macAddr'])
      )
    )

  return Map(info, locationNodes, wifiNodes)




