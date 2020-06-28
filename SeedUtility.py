from CSRandom import CSRandomLite,CSRandom
from ObjectInfo import ObjectInfo
def dailyLuck(seed,daysPlayed,steps):
    #DailyLuck random is initialised before daysPlayed is incremented
    localDaysPlayed = daysPlayed - 1;
    rand = CSRandomLite(int(seed/100) + localDaysPlayed * 10 + 1 + steps)
    dayOfMonth = ((localDaysPlayed-1) % 28) + 1
  #  for index in range(100):
  #      print( str( min(.10, rand.Next(-100, 101) / 1000) ) )
    for index in range(dayOfMonth):
        rand.Sample()
    dish = rand.Next(194,240)
    while dish in { 346, 196, 216, 224, 206, 395, 217 }:
        dish = rand.Next(194,240)
    rand.Sample(); #Dish additional number
    rand.Next(1,4); #Dish number
    #rand.Sample(); #Friendship
    #rand.Sample(); #Friendship mail
    rand.Sample(); #Rarecrow society
    rand.Sample(); #Random call not yet found in code
    return min(.10, rand.Next(-100, 101) / 1000)

def dishOfTheDay(seed,daysPlayed,steps):
    #DailyLuck random is initialised before daysPlayed is incremented
    localDaysPlayed = daysPlayed - 1;
    rand = CSRandomLite(int(seed/100) + localDaysPlayed * 10 + 1 + steps)
    dayOfMonth = ((localDaysPlayed-1) % 28) + 1
  #  for index in range(100):
  #      print( str( min(.10, rand.Next(-100, 101) / 1000) ) )
    for index in range(dayOfMonth):
        rand.Sample()
    dish = rand.Next(194,240)
    while dish in { 346, 196, 216, 224, 206, 395, 217 }:
        dish = rand.Next(194,240)

    return dish

def giantCrop(seed,daysPlayed,x,y, version="1.3"):
    if version == "1.3":
        result = CSRandomLite(seed + daysPlayed + x*2000 + y).Sample()
    elif version == "1.4":
        result = oneTimeRandomGetDouble(seed, daysPlayed, x, y)
    return result < 0.01

def oneTimeRandomGetDouble(a,b,c,d):
    result = oneTimeRandomGetLong(a,b,c,d)
    result = result >> 11
    result = result * 1.11022302462516e-16
    return result

def constrainToLong(number):
    result = number & 0xffffffffffffffff
    return result

def oneTimeRandomGetLong(a,b,c,d):
  
    num1 = constrainToLong(((constrainToLong(a ^ (constrainToLong(b >> 14) | constrainToLong(b << 50)))) + ((constrainToLong(c >> 31) | constrainToLong(c << 33)) ^ (constrainToLong((d >> 18)) | constrainToLong(d << 46)))) * 1911413418482053185);
    num2 = constrainToLong((((constrainToLong(a >> 30) | constrainToLong(a << 34)) ^ constrainToLong(c)) + ((constrainToLong(b >> 32) | constrainToLong(b << 32)) ^ (constrainToLong(d >> 50) | constrainToLong(d << 14)))) * 1139072524405308145);
    num3 = constrainToLong((((constrainToLong(a >> 49) | constrainToLong(a << 15)) ^ (constrainToLong(d >> 33) | constrainToLong(d << 31))) + (constrainToLong(b) ^ (constrainToLong(c >> 48) | constrainToLong(c << 16)))) * 8792993707439626365);
    num4 = constrainToLong((((constrainToLong(a >> 17) | constrainToLong(a << 47)) ^ (constrainToLong(b >> 47) | constrainToLong(b << 17))) + ((constrainToLong(c >> 15) | constrainToLong(c << 49)) ^ constrainToLong(d))) * 1089642907432013597);
    return constrainToLong((constrainToLong(num1) ^ constrainToLong(num2) ^ (constrainToLong(num3 >> 21) | constrainToLong(num3 << 43)) ^ (constrainToLong(num4 >> 44) | constrainToLong(num4 << 20))) * 2550117894111961111 + ((constrainToLong(num1 >> 20) | constrainToLong(num1 << 44)) ^ (constrainToLong(num2 >> 41) | constrainToLong(num2 << 23)) ^ (constrainToLong(num3 >> 42) | constrainToLong(num3 << 22)) ^ constrainToLong(num4)) * 8786584852613159497 + ((constrainToLong(num1 >> 43) | constrainToLong(num1 << 21)) ^ (constrainToLong(num2 >> 22) | constrainToLong(num2 << 42)) ^ constrainToLong(num3) ^ (constrainToLong(num4 >> 23) | constrainToLong(num4 << 41))) * 3971056679291618767);

def giantCropAmount(seed,daysPlayed,x,y):
    rand = CSRandomLite(seed + daysPlayed + x*7 + y*11)
    return rand.Next(15,22)

def monsterFloor(seed,daysPlayed,level):
    if level % 5 == 0:
        return False
    if level % 40 < 5:
        return False
    if level % 40 > 30:
        return False
    if level % 40 == 19:
        return False

    rand = CSRandomLite(int(seed/2)+daysPlayed+level*100)
    return rand.Sample() < 0.044

def doesSeedHaveMonsterFloorMines(seed,daysPlayed,deepestFloor):
    for floor in range(1,deepestFloor):
        if monsterFloor(seed,daysPlayed,floor):
            return True
    return False

def unusualDarkFloor(seed,daysPlayed,level):
    if level % 10 == 0:
        return False
    if level % 40 > 30:
        return False
    rand = CSRandomLite(daysPlayed * level + 4 * level + int(seed/2))
    if rand.Sample() < 0.3 and level > 2:
        return True
    if rand.Sample() < 0.15 and level > 5 and not level == 120:
        return True
    return False

def doesSeedHaveUnusualDarkFloor(seed,daysPlayed,deepestFloor):
    for floor in range(1,deepestFloor):
        if unusualDarkFloor(seed,daysPlayed,floor):
            return True
    return False


def nextGeodeItem(seed,geodesCracked,geodeType,deepestMineLevel=0,version="1.4"):
    #Assume geodesCracked passed in is 0 based
    rand = CSRandomLite(geodesCracked + 1 + int(seed / 2))
    if version == "1.4":
        num1 = rand.Next(1,10)
        for index in range(num1):
          rand.Sample()
        num2 = rand.Next(1, 10)
        for index in range(num2):
          rand.Sample()

    if rand.Sample() < 0.5:
        initialStack = rand.Next(3) * 2 + 1
        if rand.Sample() < 0.1:
            initialStack = 10
        if rand.Sample() < 0.01:
            initialStack = 20
        if rand.Sample() < 0.5:
            case = rand.Next(4)
            if case == 0 or case == 1:
                return (390,initialStack)
            elif case == 2:
                return (330,1)
            else:
                if geodeType == "Geode":
                    return (86,1)
                if geodeType == "Frozen":
                    return (84,1)
                if geodeType == "Magma":
                    return (82,1)
                if geodeType == "Omni":
                    return (82 + rand.Next(3) * 2,1)
        else:
            if geodeType == "Geode":
                case = rand.Next(3)
                if case == 0:
                    return (378,initialStack)
                if case == 1:
                    if deepestMineLevel > 25:
                        return (380,initialStack)
                    return (378,initialStack)
                if case == 2:
                    return (382,initialStack)
            if geodeType == "Frozen":
                case = rand.Next(4)
                if case == 0:
                    return (378,initialStack)
                if case == 1:
                    return (380,initialStack)
                if case == 2:
                    return (382, initialStack)
                if case == 3:
                    if deepestMineLevel > 75:
                        return (384,initialStack)
                    return (380,initialStack)
            if geodeType == "Magma" or geodeType == "Omni":
                case = rand.Next(5)
                if case == 0:
                    return (378,initialStack)
                if case == 1:
                    return (380,initialStack)
                if case == 2:
                    return (382,initialStack)
                if case == 3:
                    return (384,initialStack)
                if case == 4:
                    return (386,initialStack//2 +1)
    else:
        return ("Mineral",1)

def nextGeodeItemName(seed,geodesCracked,geodeType,deepestMineLevel=0,version="1.4"):
    result = nextGeodeItem(seed,geodesCracked,geodeType,deepestMineLevel,version)
    try:
        index = result[0]
        string = ObjectInfo[index].split('/')[0]
    except:
        string = result[0]
    return (string,result[1])

def nightEvent(seed,daysPlayed):
    #Night events are based on the new day
    if daysPlayed==32:
        return None
    rand = CSRandomLite(int(seed/2) + daysPlayed)
    if rand.Sample() < 0.01:        
        if (daysPlayed -1) // 28 % 4 != 3:
            return "Fairy"
    if rand.Sample() < 0.01:
        return "Witch"
    if rand.Sample() < 0.01:
        return "Meteor"
    if rand.Sample() < 0.01:
        if daysPlayed > 28*4:
            return "UFO"
    if rand.Sample() < 0.01:
        return "Owl"

def uniqueKrobusStock(seed,daysPlayed):
    rand = CSRandomLite(int(seed/2) + daysPlayed)
    dayOfWeek = daysPlayed % 7
    if dayOfWeek == 3:
        return rand.Next(698,709)
    if dayOfWeek == 6:
        index = rand.Next(194,245)
        if index == 217:
            index = 216
        return index
    return None


def randomItemFromSeason(gameID, day, seedAdd, furnace=False, forQuest=False,recipesKnown=1,mineFloor=0):
    season = (day-1) // 28 % 4
    rand = CSRandom(gameID + day + seedAdd)
    source = [68, 66, 78, 80, 86, 152, 167, 153, 420]
    if forQuest and mineFloor > 40:
        source.extend([62,70,72,84,422])
    if forQuest and mineFloor > 80:
        source.extend([64,60,82])
    if furnace:
        source.extend([334,335,336,338])
    source.extend({
		0 : [16,18,20,22,129,131,132,136,137,142,143,145,147,148,152,167,267],
		1 : [128,130,132,136,138,142,144,145,146,149,150,155,396,398,402,267], 
		2 : [404,406,408,410,129,131,132,136,137,139,140,142,143,148,150,154,155,269],
		3 : [412,414,416,418,130,131,132,136,140,141,144,146,147,150,151,154,269]
		}[season])
    if forQuest:
        for recipe in range(recipesKnown):
            #Random called for cooking recipes
            rand.Sample()

    r = rand.Next(len(source))
    return source[r]

def getItemFromIndex(index):
    #handle being called after trashcans
    if index == "DishOfTheDay":
        return index
    return ObjectInfo[index].split('/')[0]

def fairyCropIndex(seed,days,numberOfHoeDirts=0):
    #Assumes all other terrainFeatures have been cleared (trees/grass/flooring)
    rand = CSRandom(seed+days)
    if numberOfHoeDirts == 0:
        return rand.Sample()
    return rand.Next(numberOfHoeDirts)

def totalHarvest(seed,chanceForExtra,level=0,fert=0):
    num1 = 1
    rand = CSRandomLite(seed)
    num3 = 0.2 * (level / 10.0) + 0.2 * fert * ((level + 2.0) / 12.0) + 0.01;
    if rand.Sample() >= num3:
        rand.Sample() #crop quality
    if False:
        rand.Sample() #TODO: min/max harvest
    if chanceForExtra > 0:
        while rand.Sample() < chanceForExtra:
            num1 = num1 +1
    if rand.Sample() < 9.99999974737875E-05:
        num1 = num1 * 2

    return num1

def test14GiantCrops(seed):
    for day in range(16,27):
        for x in range(57,69):
            for y in range(19,35):
                if giantCrop(seed,day,x,y,"1.4"):
                    print(str(x)+","+str(y)+" day: "+str(day))

def findBestHarvest():
    for seed in range(3582582,2147483648):
        num = totalHarvest(seed,0.2)
        if num > 12:
            print(str(seed) + " " + str(num))
def summer2potatodrops():
    for seed in range(611235816,611235816+79*7+64*11+28):
        num = totalHarvest(seed,0.2)
        if num > 3:
            print(str(seed) + " " + str(num))

def printGiantCropHarvest(seed,spots,days):
    for spot in spots:
        print(spot)
        for day in days:
            print(str(day) + " " + str(giantCropAmount(seed,day,spot[0]-1,spot[1]-1)))

def printPotatoSpots(seed,day):
     for y in range(18,25):
        for x in range(57,69):
            print(str(x)+","+str(y)+" harvest: "+ str(totalHarvest(seed+day+x*7+y*11,0.2)))

if __name__ == '__main__':
    #test14GiantCrops(1946946589 );
    printGiantCropHarvest(1946946589,[[65,21]],range(24,25))
    #findMine50Seed();
    #print(fairyCropIndex(611235816,30))
    #printPotatoSpots(1946946589,18)

    #findBestHarvest()
            