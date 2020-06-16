
import TravelingCart
import SeedUtility
import TrashCans

def findSeed():
    cartDays = [5,7,12,14,19,21,26,28]
    krobusDays = [10,17,24]
    #krobusDays= [24]
    bestSeed = 0
    bestSeedAmount = 99999
    seeds = range(-1000000000,2147483648)
    #seeds = [-522420324,-1592059384,-1465407692,-1028626208,-448726017,-292239603,-122162209,611235816]
    #seeds=[611235816,690079572,1008139240,-2131847362,-1984324702,-1881191744,-1878196469,-1807801067,-1804000585,-1776233795,-1770833157,-1736458165,-1732797703,-1697547940,-1646855095,-1592059384,-1465407692,-1463762811,-1453051255,-1268229407,-1230761571,-1160997286,-1157820029,-1153587803,-1128195071,-1098339703,-1074465120,-1030968205,-1028626208,-1023756801,-1014545826,-1004721616,-925020035,-922687671,-811091642,-809908649,-709968377,-638161535,-625569381,-608034108,-595706433,-573015200,-522810374,-522420324,-448726017,-439807257,-413811947,-403148417,-324791433,-292239603,-267600127,-189564877,-186796577,-170441087,-122162209,-83611757]
    for seed in seeds:
        if seed % 1000000 == 0:
            print("Searching: " + str(seed))

        #Requires a fairy morning of Summer 2
        if not SeedUtility.nightEvent(seed,30) == "Fairy":
            continue

        #Look at travelling cart for Spring
        neededItems = {140:1,266:1,272:1,276:1,408:1,416:1,418:1,699:1}

        #idealItems= [254,256,258,260,270,376,421]

        #cabbageSeed = True

        #summerCrops = 0

        for day in cartDays:
            stock = TravelingCart.getTravelingMerchantStock_1_4(seed+day)
            for item in stock.items():
                #if item[0] in idealItems:
                #    summerCrops = summerCrops + 1
                #    idealItems.remove(item[0])
                #if item[0] == 262:
                #    summerCrops = summerCrops + item[1][1]
                #if item[0] == 266 and cabbageSeed:
                #    cabbageSeed = False
                if item[0] == 485 and 266 in neededItems:
                    item = (266,(item[1][0],item[1][1]))
                #    cabbageSeed = True
                if item[0] not in neededItems:
                    continue
                quantity = neededItems[item[0]] - item[1][1]
                if quantity <= 0:
                    del neededItems[item[0]]
                else:
                    neededItems[item[0]] = quantity
               
        for day in krobusDays:
            kroItem = SeedUtility.uniqueKrobusStock(seed,day)
            if kroItem not in neededItems:
                continue
            del neededItems[kroItem]

        #if cabbageSeed:
        #    summerCrops =  summerCrops - 1


        if neededItems == {}: # and summerCrops >1:
            print(seed)

        if len(neededItems) < bestSeedAmount:
            bestSeed = seed
            bestSeedAmount = len(neededItems)
    print(bestSeed)
    print(bestSeedAmount)

if __name__ == '__main__':
    findSeed()

