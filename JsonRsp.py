import requests
import json

url = requests.get("http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=DemoBuilding&Level=2")
resp = url.json()
print(resp)
print("")

obj = json.dumps(resp, indent=4, separators=(',', ':'))
print (obj)

mapInfo = json.dumps(resp["info"], indent=4, separators=(',', ':'))
print (mapInfo)

mapDetails = json.dumps(resp["map"], indent=4, separators=(',', ':'))
print (mapDetails)

wifiDetails = json.dumps(resp["wifi"], indent=4, separators=(',', ':'))
print (wifiDetails)

print ("")
print ("")
print ("")
print ("")
print ("response 2")

url2 = "http://showmyway.comp.nus.edu.sg/getMapInfo.php"
params = dict(
	Building='DemoBuilding',
	Level='2'
)

resp2 = requests.get(url=url2, params=params)
data = resp2.json()
obj2 = json.dumps(data, dict, indent=4, sort_keys= True, separators=(',', ':'))

print (obj2)

print (type(obj2))
	