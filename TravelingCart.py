from itertools import chain
import sys

from ObjectInfo import ObjectInfo as oi
from Utility import dayToYSD

import json
from itertools import chain
from CSRandom import CSRandom as CSRandomSlow, CSRandomLite as CSRandomFast
import time
from collections import OrderedDict

with open('ObjectInformation.json','r') as f:
    ObjectInfo = json.load(f)['content']
ObjectInfo = dict(zip(map(lambda x:int(x),ObjectInfo.keys()),map(lambda x: x.split('/'),ObjectInfo.values())))
for key in ObjectInfo.keys():
    ObjectInfo[key][1] = int(ObjectInfo[key][1])
ObjectInfo[174][0] = 'Large EggW'
ObjectInfo[182][0] = 'Large EggB'

objectsOffLimits = [79, 158, 159, 160, 161, 162, 163, 261, 277, 279,
                   305, 308, 326, 341, 413, 417, 437, 439, 447, 454, 
                   460, 645, 680, 681, 682, 688, 689, 690, 774, 775,
                   797, 798, 799, 800, 801, 802, 803, 807, 812]
validObjects = set()
for key,array in ObjectInfo.items():
    if '-' in array[3] and array[1] > 0 and '-13' not in array[3] and 'Quest' != array[3] \
        and 'Weeds' != array[0] and 'Minerals' not in array[3] and 'Arch' not in array[3]:
        if key < 790 and key not in objectsOffLimits:
            validObjects.add(key)

ObjectIDFromName = dict(zip([obj[0] for obj in ObjectInfo.values()], ObjectInfo.keys()))

def getTravelingMerchantStock_1_4(seed, CSRandom=CSRandomFast):
    # check speed trial block below 
    # CSRandomSlow is 60% slower but it will always work
    # CSRandomFast can only call Next 100 times due to implementation
    # It's way faster to try the fast random until it crashes and restart
    # than it is to run the slow one by default across many seeds
    try:
        random = CSRandom(seed)
        currentStock = dict()
        for i in range(10):
            num = random.Next(2, 790)
            while True:
                num = (num+1) % 790;
                if num in validObjects:
                    cost = max(random.Next(1,11)* 100, ObjectInfo[num][1]*random.Next(3,6))
                    qty = 1 if not (random.Sample() < 0.1) else 5
                    if num not in currentStock:
                        currentStock[num] = [cost,qty]
                        break
        return currentStock
    except:
        # we must've hit over 100 random calls, need to revert to the slow version
        return getTravelingMerchantStock_1_4(seed, CSRandomSlow)

def getTravelingMerchantStock(gameID, dayNumber, version="1.4"):
    if version == "1.4":
        return getTravelingMerchantStock_1_4(gameID + dayNumber)

    def _invalid_idx(index):
        invalid = True if index in [158, 159, 160, 161, 162, 163, 326, 341, 413, 437, 439, 454, 460, 645, 681, 682,
                                    688, 689, 690, 774, 775] else False
        return invalid

    def _invalid_str(strArray):
        conditions = strArray[3].find('-') == -1 or int(strArray[1]) <= 0 or strArray[3].find('-13') != -1 or strArray[3] == 'Quest' or strArray[0] == 'Weeds' or strArray[3].find('Minerals') != -1 or strArray[3].find('Arch') != -1
        return conditions

    rand = CSRandom(gameID+dayNumber)
    stock = {}
    stockItems = set()
    for i in range(10):
        index = rand.Next(2, 790)
        while True:
            index = (index+1) % 790
            if index not in ObjectInfo or _invalid_idx(index,version):
                continue
            strArray = oi[index].split('/')
            if _invalid_str(strArray):
                continue
            price = max(rand.Next(1, 11)*100, int(strArray[1])*rand.Next(3, 6))
            amount = 1 if (rand.Sample() > 0.1) else 5
            stockItems.add(index)
            break
        stock[i] = [strArray[0], price, amount]
    return stock


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
    writeAllSeedsToFile();
