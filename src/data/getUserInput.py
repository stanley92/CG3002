from path import get_map_info					# change your import also
from path import find_shortest_path

class getUserInput():
	
	def getBuildingName(btn):
		if (btn == "1#")
			building = "COM1"		
		elif (btn == "2#")
			building = "COM2"

		return building

	def getBuildingLevel(btn):
		if (btn == "1#")
			level = "b1"
		elif (btn == "2#")
			level = "1"
		elif (btn == "3#")
			level = "2"
		elif (btn == "4#")
			level = "3"
		elif (btn == "5#")
			level = "4"

		return level

	def getDestination(dest_str): 
		dest = dest_str.replace("#", "")
		return dest

mapInfo = get_map_info.getMapInfo(getBuildingName(btn),getBuildingLevel(btn)) # how can u call getBuildingName like this :v it's in a class
graph = get_map_info.generateGraph(mapInfo)
s_path = find_shortest_path.shortest(graph,0,getDestination(dest))	# u didn't include the module names

north_at = mapInfo.info.north_at
lastKnownNode = graph.getVertex(i).id


# walking algorithm is only btw 2 nodes

# Assuming user always walks starting at entrance
# initial last known node will be 0 (starting point)
# last known node = last node departed from

# when a cancel happens last known node selected
# from the 2 nodes based on the distance remaining
# user will be directed to tt node

# based on info : north at 180
# based on user direction, (180 - displacement angle)
# if +ve turn Left, if -ve turn Right
# assume walking on straight path

# if person walk out of straight path, person just needs to reach y-axis
# while automatically adjusting to L/R based on motor

# sonar sensor value < wall distance value
# activate motor


