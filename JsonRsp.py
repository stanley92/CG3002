import requests
import json

'''
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
'''

url2 = "http://showmyway.comp.nus.edu.sg/getMapInfo.php"
params = dict(
	Building='DemoBuilding',
	Level='2'
)

resp2 = requests.get(url=url2, params=params)
data = resp2.json()
#obj2 = json.dumps(data, dict, indent=4, sort_keys= True, separators=(',', ':'))
info = data['info']
details = data['map']
wifi = data['wifi']

print(info)
print("")
print(details)
print("")
print(wifi)
print("")
print (type(data))

for x in info:
	print info['northAt']

for w in details:
	print int(w['y'])
	print int(w['x'])
	print int (w['nodeId'])
	print str (w['nodeName'])
	print [int(link) for link in (str(w['linkTo']).split(','))]

for x in wifi:
	print int(x['y'])
	print int(x['x'])
	print int (x['nodeId'])
	print str (x['nodeName'])
	print str (x[])