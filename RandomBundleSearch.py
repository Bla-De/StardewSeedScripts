

import TravelingCart
import SeedUtility
import TrashCans
import RandomBundlesSeeding
import os
import json
from CSRandom import CSRandomLite as Random

fairyItems = [254,256,258,260,376,421,268,262,266,270]
absolute_path = os.path.dirname(os.path.abspath(__file__))
filename = absolute_path + '/CCRoomResults.txt'
travelingCartCache = {}

def cleanupCache(seed):
    keys = []
    for key in travelingCartCache:
        if key < seed:
            keys.append(key)
    for key in keys:
        del travelingCartCache[key]

def findSeed():
    cartDays = [5,7,12,14,19,21,26,28]
    krobusDays = [10,17,24]
    bestSeed = 0
    bestSeedAmount = 99999
    seeds = range(179831485,999999999)
    for seed in seeds:
        if seed % 10000 == 0:
            cleanupCache(seed)

        if seed % 1000000 == 0:
            print("Searching: " + str(seed))
            f = open(filename,"at")
            f.write("searching: " + str(seed) + '\n')
            f.close()

        #Find bundles for this seed
        requiredItems,hasFairyItems = RandomBundlesSeeding.getAllSeasonalRequiredItems(seed, "Quality Crops","Quality Fish")

        #Check if seed is valid
        if -1 in requiredItems:
            continue

        #Requires a fairy morning of Summer 2
        hasFairy = SeedUtility.nightEvent(seed,30) == "Fairy"
        if hasFairyItems and not hasFairy:
            continue

        if hasFairy:
            for fairyItem in fairyItems:
                while fairyItem in requiredItems:
                    del requiredItems[requiredItems.index(fairyItem)]

        #Look at travelling cart for Spring
        #neededItems = {140:1,266:1,272:1,276:1,408:1,416:1,418:1,699:1}
        #neededItems = {140:1,272:1,276:1,408:1,416:1,418:1,699:1}

        #idealItems= [254,256,258,260,270,376,421,266]


        summerCrops = 0

        for day in cartDays:
            if seed+day in travelingCartCache:
                stock = travelingCartCache[seed+day]
            else:
                stock = TravelingCart.getTravelingMerchantStock_1_4(seed+day,"1.5")
                travelingCartCache[seed+day] = stock
            for item in stock.items():
                if item[0] == 262:
                    summerCrops = summerCrops + item[1][1]
                if item[0] not in requiredItems:
                    continue
                del requiredItems[requiredItems.index(item[0])]
               
        for day in krobusDays:
            kroItem = SeedUtility.uniqueKrobusStock(seed,day)
            if kroItem not in requiredItems:
                continue
            del requiredItems[requiredItems.index(kroItem)]

        if 266 in requiredItems:
            random = Random(seed*12)
            if random.Next(2,31) <= 8:
                del requiredItems[requiredItems.index(266)]

        #Hack for Garden bundle
        if len(requiredItems) == 1:
            if 593 in requiredItems or 595 in requiredItems or 421 in requiredItems:
                requiredItems = []

        if requiredItems == []:
            print(str(seed) + " " + str(summerCrops))
            f = open(filename,"at")
            f.write(str(seed) + " " + str(summerCrops) + '\n')
            f.close()

        if len(requiredItems) < bestSeedAmount:
            bestSeed = seed
            bestSeedAmount = len(requiredItems)
    #print(bestSeed)
    #print(bestSeedAmount)
def displayDetails(seeds,cartDays,krobusDays):
        for seed in seeds:
            print(seed)
            print(json.dumps(RandomBundlesSeeding.generate_random_bundles(seed), indent=4))
            for day in cartDays:
                print(day)
                stock = TravelingCart.getTravelingMerchantStock_1_4(seed+day,"1.5")
                for item in stock.items():
                    print(SeedUtility.getItemFromIndex(item[0]))
            print("Krobus")
            for day in krobusDays:
                print(day)
                print(SeedUtility.getItemFromIndex( SeedUtility.uniqueKrobusStock(seed,day)))

                

if __name__ == '__main__':
    findSeed()
    
    seeds=[52411360]
    displayDetails(seeds,[5,7,12,14,19,21,26,28],[10,17,24])