import SeedUtility
import TravelingCart
import Location;
def findBoilerRoomSeed():
    backwoods = Location.createBackwoods()
    mountain = Location.createMountain()
    forest = Location.createForest()
    busstop = Location.createBusstop()
    for seed in range(16269986,999999999):
        if seed % 10000 == 0:
            print("searching: " + str(seed))
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

        if cart[0][0] == cart[1][0] and ( cart[2][0] == cart[1][0] or quartz[0] > 0 ) and (cart[3][0] == cart[1][0] or quartz[1] > 0):

            print(str(seed) + " " + str(cart) + " " + str(quartz))# + " Leeks: " + str(leekCount))

def findFireQuartz(seed):
    #Will also return if enough gold is before the quartz
    goldOre = 0
    ironOre = 0
    fireQuartz = 0
    frozenTear = 0
    for number in range(1,10):
        item = SeedUtility.nextGeodeItemName(seed,number,"Omni",20)
        if item[0] == "Gold Ore" and goldOre == 0:
            if item[1] >= 5:
                goldOre = number
        if item[0] == "Iron Ore" and ironOre == 0:
            if item[1] >= 5:
                ironOre = number
        if item[0] == "Fire Quartz" and fireQuartz == 0:
            fireQuartz = number
        if item[0] == "Frozen Tear" and frozenTear == 0:
            frozenTear = number

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
        stock = TravelingCart.getTravelingMerchantStock(seed,day,"1.4")
        for item in stock.values():
            if item[0] == "Gold Bar":
                if item[1] < goldBar[1]:
                    goldBar = (day,item[1])
            if item[0] == "Iron Bar":
                if item[1] < ironBar[1]:
                    ironBar = (day,item[1])
            if item[0] == "Solar Essence":
                if item[1] < solar[1]:
                    solar = (day,item[1])
            if item[0] == "Void Essence":
                if item[1] < void[1]:
                    void = (day,item[1])

    if solar[1] + void[1] < 10000:
        return (solar,void,ironBar,goldBar)
    return None

def analyseSeeds():
    seeds = [
(10373125 ,13,26)]
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
    #for lday in range(5,19):
    #    print(str(lday) + " " + str(SeedUtility.dailyLuck(10373125 , lday, lday-1)))
  