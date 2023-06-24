from itertools import chain
import sys

from ObjectInfo import ObjectInfo as oi
from Utility import dayToYSD

import json
from itertools import chain
from CSRandom import CSRandom as CSRandomSlow, CSRandomLite as CSRandomFast
import time
from collections import OrderedDict

import SeedUtility

with open('ObjectInformation.json','r') as f:
    ObjectInfo = json.load(f)['content']
ObjectInfo = dict(zip(map(lambda x:int(x),ObjectInfo.keys()),map(lambda x: x.split('/'),ObjectInfo.values())))
for key in ObjectInfo.keys():
    ObjectInfo[key][1] = int(ObjectInfo[key][1])
ObjectInfo[174][0] = 'Large EggW'
ObjectInfo[182][0] = 'Large EggB'

objectsOffLimits = [69, 73, 79, 91, 158, 159, 160, 161, 162, 163,
                    261, 277, 279, 289, 292, 305, 308, 326, 341, 413,
                    417, 437, 439, 447, 454, 460, 645, 680, 681, 682,
                    688, 689, 690, 774, 775, 797, 798, 799, 800, 801,
                    802, 803, 807, 812]
validObjects = set()
for key,array in ObjectInfo.items():
    if '-' in array[3] and array[1] > 0 and '-13' not in array[3] and 'Quest' != array[3] \
        and 'Weeds' != array[0] and 'Minerals' not in array[3] and 'Arch' not in array[3]:
        if key < 790 and key not in objectsOffLimits:
            validObjects.add(key)

ObjectIDFromName = dict(zip([obj[0] for obj in ObjectInfo.values()], ObjectInfo.keys()))

validFurnature = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 31, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 95, 128, 192, 197, 202, 207, 212, 288, 294, 300, 306, 312, 416, 424, 432, 440, 512, 520, 528, 536, 704, 709, 714, 719, 724, 727, 800, 807, 814, 821, 1120, 1122, 1124, 1126, 1128, 1130, 1132, 1134, 1136, 1138, 1140, 1142, 1144, 1146, 1148, 1150, 1216, 1218, 1220, 1222, 1224, 1280, 1283, 1285, 1287, 1289, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1393, 1395, 1397, 1399, 1400, 1401, 1440, 1443, 1445, 1447, 1449, 1451, 1456, 1461, 1539, 1543, 1547, 1550, 1552, 1557, 1559, 1561, 1563, 1565, 1567, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1609, 1612, 1614, 1616, 1618, 1623, 1628, 1630, 1664, 1673, 1675, 1676, 1678, 1682, 1737, 1742, 1744, 1745, 1747, 1748, 1749, 1751, 1753, 1755, 1758, 1777, 1811, 1812, 1814, 1792, 1794, 1866, 1964, 1978, 2048, 2052, 2058, 2064, 2070, 2076, 2176, 2180, 2192, 2304, 2312, 2322, 1228, 2414, 2427, 2397, 2398, 1973, 1974, 1975, 1684, 2627, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2635, 2636, 1817, 1818, 1819, 1820, 1821, 2637, 2638, 2639, 2640, 2641, 2642, 2643, 2644, 2645, 2646, 2647, 2648, 2649, 2650, 2651, 2652, 2488, 2584, 2720, 2784, 2790, 2794, 2798, 2730, 2654, 2655, 2802, 2734, 2736, 2738, 2740, 2748, 2812, 2750, 2742, 2870, 2875]

def getTravelingMerchantStock_1_4(seed, version="1.4", CSRandom=CSRandomFast, rareSeeds=False, wantedItems=[], acceptableCount=-1):
	# check speed trial block below 
	# CSRandomSlow is 60% slower but it will always work
	# CSRandomFast can only call Next 100 times due to implementation
	# It's way faster to try the fast random until it crashes and restart
	# than it is to run the slow one by default across many seeds
	try:
		random = CSRandom(seed)
		currentStock = dict()
		foundItems = 0
		missedItems = 0
		for i in range(10):
			num = random.Next(2, 790)
			while True:
				num = (num+1) % 790;
				if num in validObjects:
					if wantedItems != []:
						if num in wantedItems:
							foundItems += 1
						else:
							missedItems += 1
							if acceptableCount == -1 or 10 - missedItems == acceptableCount - 1:
								return dict()
					cost = max(random.Next(1,11)* 100, ObjectInfo[num][1]*random.Next(3,6))
					qty = 1 if not (random.Sample() < 0.1) else 5
					if num not in currentStock:
						currentStock[num] = [cost,qty]
						break
        
		if rareSeeds:
			#Furniture
			lowerBound = 0
			upperBound = 1613

			index = random.Next(lowerBound, upperBound)
			while index not in validFurnature:
				index = random.Next(lowerBound, upperBound)
            
			#Furniture price
			random.Sample()

			qty = 1 if not (random.Sample() < 0.1) else 5
			if 347 not in currentStock:
				currentStock[347] = [1000,qty]




		return currentStock
	except:
		# we must've hit over 100 random calls, need to revert to the slow version
		return getTravelingMerchantStock_1_4(seed, version, CSRandomSlow,rareSeeds)

def getTravelingMerchantStock(gameID, dayNumber, version="1.4"):
    if version == "1.4" or version == "1.5":
        return getTravelingMerchantStock_1_4(gameID + dayNumber, version)

    def _invalid_idx(index):
        invalid = True if index in [158, 159, 160, 161, 162, 163, 326, 341, 413, 437, 439, 454, 460, 645, 681, 682,
                                    688, 689, 690, 774, 775] else False
        return invalid

    def _invalid_str(strArray):
        conditions = strArray[3].find('-') == -1 or int(strArray[1]) <= 0 or strArray[3].find('-13') != -1 or strArray[3] == 'Quest' or strArray[0] == 'Weeds' or strArray[3].find('Minerals') != -1 or strArray[3].find('Arch') != -1
        return conditions

    rand = CSRandomSlow(gameID+dayNumber)
    currentStock = dict()
    for i in range(10):
        index = rand.Next(2, 790)
        while True:
            index = (index+1) % 790
            if index not in ObjectInfo or _invalid_idx(index):
                continue
            strArray = oi[index].split('/')
            if _invalid_str(strArray):
                continue
            price = max(rand.Next(1, 11)*100, int(strArray[1])*rand.Next(3, 6))
            amount = 1 if (rand.Sample() > 0.1) else 5
            break
        currentStock[index] = [price,amount]
    return currentStock


def checkDay(gameID,day,itemList):
    a = getTravelingMerchantStock(gameID, day)
    vals = [s[0] for s in list(a.values())]
    return list(set(vals) & set(itemList))


def findItem(gameID, item):
    day = 0
    counter = 1
    itemList = [item]
    while day == 0:
        cur_day = 7*counter - 2
        a = checkDay(gameID, cur_day, itemList)
        if a:
            day = cur_day
            break
        cur_day = 7*counter
        a = checkDay(gameID, cur_day, itemList)
        if a:
            day = cur_day
            break
        counter = counter+1
    cost = [a[1] for a in getTravelingMerchantStock(gameID, day).values() if a[0] in itemList]
    return [dayToYSD(day),item,cost]

def findBundleSeed():
    if len(sys.argv) >= 2:
        gameID = int(sys.argv[1])
    else:
        gameID = 143594438
    print('GameID:', gameID)

    bundleAnimal    = ['L. Goat Milk', 'Large Milk', 'Large EggW', 'Large EggB', 'Duck Egg', 'Wool']
    bundleArtisan   = ['Truffle Oil', 'Cloth', 'Goat Cheese', 'Cheese', 'Honey', 'Jelly', 'Apple', 'Apricot', 'Orange', 'Peach', 'Pomegranate', 'Cherry', 'Milk', 'Goat Milk']
    bundleChef      = ['Maple Syrup', 'Fiddlehead Fern', 'Truffle', 'Poppy', 'Maki Roll', 'Fried Egg']
    bundleDye       = ['Red Mushroom', 'Sea Urchin', 'Sunflower', 'Duck Feather', 'Aquamarine', 'Red Cabbage']
    bundleEnchanter = ['Oak Resin', 'Wine', 'Rabbit\'s Foot', 'Pomegranate Sapling']
    bundleFodder    = ['Wheat', 'Hay', 'Apple Sapling']
    bundleList = [bundleAnimal, bundleChef, bundleDye, bundleEnchanter, bundleArtisan, bundleFodder]

    print('Finding TRUFFLE:')
    print(findItem(gameID, 'Truffle'))
    print('Finding Rabbit Foot:')
    print(findItem(gameID, 'Rabbit\'s Foot'))

    print('Scanning Days:')
    for i in range(1, 16*3+1):
        itemList = []
        for bundle in bundleList:
            day = 7*i-2
            items = checkDay(gameID, day, bundle)
            if items:
                itemList.append([[dayToYSD(day), a[0], a[1]] for a in
                                 getTravelingMerchantStock(gameID, day).values() if a[0] in items])
        for bundle in bundleList:
            day = 7*i
            items = checkDay(gameID, day, bundle)
            if items:
                itemList.append([[dayToYSD(day), a[0], a[1]] for a in getTravelingMerchantStock(gameID, day).values() if
                                 a[0] in items])
        if itemList:
            print(list(chain.from_iterable(itemList)))
            
def writeAllSeedsToFile():

    file = open("F:\SDV\Cart.txt","ab")

    startSeed = -2147483648
    endSeed = 2147483647

    for seed in range(startSeed,endSeed + 1):
        file.write(format(seed,'b')+format(":",'b')+ format(getTravelingMerchantStock_1_4(seed)+format(",\n",'b'),'b'))



if __name__ == '__main__':
    #findBundleSeed()
    #writeAllSeedsToFile();
    seed = 329267225
    days = [166,168,173,175,180,182,187,189]
    found = False

    for day in days:
        stock = getTravelingMerchantStock(seed,day,"1.5")
        for item in stock.items():
            print( SeedUtility.getItemFromIndex(item[0]))
