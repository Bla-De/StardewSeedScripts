from CSRandom import CSRandomLite,CSRandom
from ObjectInfo import ObjectInfo
from Utility import dayToYSD
import SeedUtility
GarbageLocations = { 
							0 : [[13,86],'Jodi'],	# Jodi
							1 : [[19,89],'Emily'],	# Emily
							2 : [[56,85],'Lewis'],	# Lewis	
							3 : [[108,91],'Museum'],# Museum
							4 : [[97,80],'Clint'],	# Clint
							5 : [[47,70],'Gus'],		# Gus
							6 : [[52,63],'George'],	# George
							7 : [[110,56],'Joja'] #Joja
							}
seasonDict = {0:'Spring', 1:'Summer', 2:'Fall', 3:'Winter'}


def randomItemFromSeason(gameID, day, seedAdd, furnace=False,mineFloor=0,desert=False):
	return SeedUtility.randomItemFromSeason(gameID, day, seedAdd, furnace,mineFloor=mineFloor,desert=desert)

def checkTrash(gameID,day,index,x,y,furnace=False, luck=0.0, version = "1.4", returnMinLuck=False,minesFloor=0,desert=False,cansChecked=0,trashSeed=0):
	if version == "1.4" or version == "1.5":
		if trashSeed == 0:
			rand = CSRandomLite(int(gameID / 2) + day + 777 + index * 77)
		else:
			rand = CSRandomLite(trashSeed)
		num2 = rand.Next(0,100)
		for index2 in range(num2):
			rand.Sample()
		num2 = rand.Next(0,100)
		for index2 in range(num2):
			rand.Sample()
	else:
		if trashSeed == 0:
			rand = CSRandomLite(int(gameID/2) + day + 777 + index)
		else:
			rand = CSRandomLite(trashSeed)
		
	mega = False
	doubleMega = False
	if cansChecked > 20:
		mega = rand.Sample() < 0.01
		doubleMega = rand.Sample() < 0.002

	if doubleMega:
		if returnMinLuck:
			return "Hat",-0.1
		return "Hat"
	if not mega:
		result = rand.Sample()
	if mega or result < luck + 0.2:
		if mega:
			minLuck = -0.1
		else:
			minLuck = result - 0.2
		r = rand.Next(10)
		if r == 6:
			ps = randomItemFromSeason(gameID, day, x*653+y*777, furnace,minesFloor,desert)
		elif r == 8:
			ps = 309 + rand.Next(3)
		else:	
			ps = { 0 : 168,
					 1 : 167,
					 2 : 170,
					 3 : 171,
					 4 : 172,
					 5 : 216,
					 7 : 403,
					 9 : 153
					}[r]
		if index == 3:
			result = rand.Sample()
			if result < luck + 0.2:
				minLuck = max(minLuck,result - 0.2)
				ps = 535
				if rand.Sample() < 0.05:
					ps = 749
		if index == 4:
			result = rand.Sample()
			if result < luck + 0.2:
				minLuck = max(minLuck,result - 0.2)
				ps = 378 + rand.Next(3)*2
				if version == "1.4":
					rand.Next(1,5)
		if index == 5:
			result = rand.Sample()
			if result < luck + 0.2:
				minLuck = max(minLuck,result - 0.2)
				ps = 196 # meals are complicated
				if returnMinLuck:
					return 'DishOfTheDay',minLuck
				return 'DishOfTheDay'
		if index == 6:
			result = rand.Sample()
			if result < luck + 0.2:
				minLuck = max(minLuck,result - 0.2)
				ps = 223
		if index == 7 and rand.Sample() < 0.2:
			ps = 167
		if returnMinLuck:
			return ps,minLuck
		return ps
	if returnMinLuck:
		return None,None
	return None

def checkAllTrash(gameID, day, furnace=False, luck=0.0, version = "1.4",returnMinLuck=False,minesFloor=0,desert=False,cansChecked=0):
	results = []
	for i in range(8):
		item = checkSpecificTrash(gameID, day, i, furnace, luck, version,returnMinLuck,minesFloor,desert,cansChecked)
		if not item == None:
			results.extend([item])
	return results

def checkSpecificTrash(gameID, day, i, furnace=False, luck=0.0, version = "1.4",returnMinLuck=False,minesFloor=0,desert=False,cansChecked=0,trashSeed=0):
	can = GarbageLocations[i]
	return checkTrash(gameID,day,i,can[0][0],can[0][1],furnace,luck,version,returnMinLuck,minesFloor,desert,cansChecked,trashSeed)

def checkCans(gameID, day, cans, furnace=False, luck=0.0, version = "1.4",desert=False,cansChecked=0):
	results = []
	for i in cans:
		item = checkSpecificTrash(gameID, day, i, furnace, luck, version,desert=desert,cansChecked=cansChecked)
		if not item == None:
			results.extend([item])
	return results

if __name__ == '__main__':

	print(checkSpecificTrash(4667992,2,5,True,0.092,"1.4",True,0,False,0))
	if False:
		import sys
		if len(sys.argv) >= 2:
			gameID = int(sys.argv[1])
		else:
			gameID = 170579501
		print(gameID)
		days = [188]
		for day in days:
			flag = False
			Cans = dayToYSD(day) + "\n"
			for i in range(8):
				can = GarbageLocations[i]
				item,luck = checkTrash(gameID,day,i,can[0][0],can[0][1],True,0.10,"1.4",True)
				if item is not None:
					flag = True
					Cans = Cans + ("\t %s : %s\n" % (can[1],SeedUtility.getItemFromIndex(item)+ ", Minimum luck: "+str(luck) ))
			if flag:
				print(Cans)

		items = checkAllTrash(gameID,33,True,0.1,"1.4")
		print(items)
		input()