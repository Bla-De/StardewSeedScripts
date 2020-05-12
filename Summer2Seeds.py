
import TravelingCart
import SeedUtility
import TrashCans

def findSeed():
    cartDays = [5,7,12,14,19,21,26,28]
    krobusDays = [10,17,24]
    bestSeed = 0
    bestSeedAmount = 99999
    for seed in range(541214634,2147483648):
        if seed % 1000000 == 0:
            print("Searching: " + str(seed))

        #Requires a fairy morning of Summer 2
        if not SeedUtility.nightEvent(seed,30) == "Fairy":
            continue

        #Look at travelling cart for Spring
        neededItems = {140:1,266:1,272:1,276:1,408:1,416:1,418:1,699:1}

        for day in cartDays:
            stock = TravelingCart.getTravelingMerchantStock_1_4(seed+day)
            for item in stock.items():
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

        if neededItems == {}:
            print(seed)

        if len(neededItems) < bestSeedAmount:
            bestSeed = seed
            bestSeedAmount = len(neededItems)
    print(bestSeed)
    print(bestSeedAmount)

if __name__ == '__main__':
    findSeed()

