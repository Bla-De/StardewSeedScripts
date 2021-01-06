import SeedUtility
import TravelingCart
import Location;
import os
def findBoilerRoomSeed():
    backwoods = Location.createBackwoods()
    mountain = Location.createMountain()
    forest = Location.createForest()
    busstop = Location.createBusstop()
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    print(absolute_path)
    filename = absolute_path + '/boilerRoomResults.txt'
    #f = open(filename,"at")
    for seed in range(44200000,999999999):
        if seed % 100000 == 0:
            print("searching: " + str(seed))
            f = open(filename,"at")
            f.write("searching: " + str(seed) + '\n')
            f.close()
        #if SeedUtility.dailyLuck(seed,18,17) > 0.099 and not SeedUtility.doesSeedHaveMonsterFloorMines(seed,18,50):
            #backwoods.processDay(seed,15)
            #mountain.processDay(seed,15)

            #leekCount = 0
            #for item in backwoods.items.items():
            #    if item[1] != "Leek":
            #        leekCount = leekCount + 1

            #for item in mountain.items.items():
            #    if item[1] != "Leek":
            #        leekCount = leekCount + 1

            #if leekCount < 4:
            #    continue

        quartz = findFireQuartz(seed)
        if quartz == None:
            continue

        cart = findEarlyCart(seed)
        if cart == None:
            continue

        if cart[0][0] == cart[1][0] and ( cart[3][0] == cart[1][0] or quartz[0] > 0 ) and (cart[2][0] == cart[1][0] or quartz[1] > 0):

            print(str(seed) + " " + str(cart) + " " + str(quartz))# + " Leeks: " + str(leekCount))
            f = open(filename,"at")
            f.write(str(seed) + " " + str(cart) + " " + str(quartz) + '\n')
            f.close()

def findFireQuartz(seed):
    #Will also return if enough gold is before the quartz
    goldOre = 0
    goldOreAmount = 0
    ironOre = 0
    ironOreAmount = 0
    fireQuartz = 0
    frozenTear = 0
    for number in range(1,10):
        item = SeedUtility.nextGeodeItem(seed,number,"Omni",20,"1.5")
        if item[0] == 384 and goldOre == 0:
            goldOreAmount = goldOreAmount + item[1]
            if goldOreAmount >= 5:
                goldOre = number
        if item[0] == 380 and ironOre == 0:
            ironOreAmount = ironOreAmount + item[1]
            if ironOreAmount >= 5:
                ironOre = number
        if item[0] == 82 and fireQuartz == 0:
            fireQuartz = number
        if item[0] == 84 and frozenTear == 0:
            frozenTear = number

        if fireQuartz > 0 and frozenTear > 0 and goldOre > 0 and ironOre > 0:
            return (goldOre,ironOre,fireQuartz,frozenTear)
    if fireQuartz > 0 and frozenTear > 0:
        return (goldOre,ironOre,fireQuartz,frozenTear)

    return None

def findEarlyCart(seed):
    days = [19,21,26]
    goldBar = (0,99999)
    ironBar = (0,99999)
    solar = (0,99999)
    void = (0,99999)

    idxGold = 336
    idxSolar = 768
    idxVoid = 769

    for day in days:
        stock = TravelingCart.getTravelingMerchantStock(seed,day,"1.5")
        hasVoid = False
        hasSolar = False
        for item in stock:
            if item == 336: #"Gold Bar":
                if stock[item][0] < goldBar[1]:
                    goldBar = (day,stock[item][0])
            if item == 335: #"Iron Bar":
                if stock[item][0] < ironBar[1]:
                    ironBar = (day,stock[item][0])
            if item == 768: #"Solar Essence":
                hasSolar = True
                if stock[item][0] < solar[1]:
                    solar = (day,stock[item][0])
            if item == 769: #"Void Essence":
                hasVoid = True
                if stock[item][0] < void[1]:
                    void = (day,stock[item][0])

        if hasVoid and hasSolar:
            return (solar,void,ironBar,goldBar)
    return None

def analyseSeeds():
    seeds = [
(14542796 ,31,32),
(14542796 ,33,34)]
    for seed in seeds:
        analyseSeed(seed[0],seed[1])
        analyseSeed(seed[0],seed[2])

def analyseSeed(seed,day):
    summer = day
    print(seed)
    busstop = Location.createBusstop()
    mountain = Location.createMountain()
    forest = Location.createForest()
    town = Location.createTown()
    busstop.processDay(seed,summer)
    mountain.processDay(seed,summer)
    forest.processDay(seed,summer)
    town.processDay(seed,summer)
    print(busstop.items)
    print(mountain.items)
    print(forest.items)
    print(town.items)
    #for lday in range(5,19):
     #   print(str(lday) + " " + str(SeedUtility.dailyLuck(seed, lday, lday-1)))

if __name__ == '__main__':
    findBoilerRoomSeed();
    #analyseSeeds();
    #print(TravelingCart.getTravelingMerchantStock(53234174,21,"1.4"))
    seed = 14542796
    for lday in range(5,25):
        print(str(lday) + " " + str(SeedUtility.dailyLuck(seed , lday, lday-1)) + " " + str(SeedUtility.doesSeedHaveMonsterFloorMines(seed,lday,21)))
  