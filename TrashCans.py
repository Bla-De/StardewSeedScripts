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


def randomItemFromSeason(gameID, day, seedAdd, furnace=False):
	return SeedUtility.randomItemFromSeason(gameID, day, seedAdd, furnace)

def checkTrash(gameID,day,index,x,y,furnace=False, luck=0.0, version = "1.4"):
	if version == "1.4":
		rand = CSRandom(gameID // 2 + day + 777 + index * 77)
		num2 = rand.Next(0,100)
		for index2 in range(num2):
			rand.Sample()
		num2 = rand.Next(0,100)
		for index2 in range(num2):
			rand.Sample()
		#rand.Sample()
		#rand.Sample()
	else:
		rand = CSRandomLite(gameID//2 + day + 777 + index)
	if rand.Sample() < luck + 0.2:
		r = rand.Next(10)
		if r == 6:
			ps = randomItemFromSeason(gameID, day, x*653+y*777, furnace)
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
		if index == 3 and rand.Sample() < luck + 0.2:
			ps = 535
			if rand.Sample() < 0.05:
				ps = 749
		if index == 4 and rand.Sample() < luck + 0.2:
			ps = 378 + rand.Next(3)*2
			if version == "1.4":
				rand.Next(1,5)
		if index == 5 and rand.Sample() < luck + 0.2:
			ps = 196 # meals are complicated
			return 'DishOfTheDay'
		if index == 6 and rand.Sample() < luck + 0.2:
			ps = 223
		if index == 7 and rand.Sample() < 0.2:
			ps = 167
		return ps
	return None

def checkAllTrash(gameID, day, furnace=False, luck=0.2, version = "1.4"):
	results = set()
	for i in range(8):
		can = GarbageLocations[i]
		results.add(checkTrash(gameID,day,i,can[0][0],can[0][1],furnace,luck,version))
	return results

if __name__ == '__main__':
	import sys
	if len(sys.argv) >= 2:
		gameID = int(sys.argv[1])
	else:
		gameID = 20992
	for day in range(1,28):
		flag = False
		Cans = dayToYSD(day) + "\n"
		for i in range(8):
			can = GarbageLocations[i]
			item = checkTrash(gameID,day,i,can[0][0],can[0][1],False,0.016)
			if item is not None:
				flag = True
				Cans = Cans + ("\t %s : %s\n" % (can[1],SeedUtility.getItemFromIndex(item)))
		if flag:
			print(Cans)
