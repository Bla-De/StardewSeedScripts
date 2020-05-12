from CSRandom import CSRandomLite
from ObjectInfo import ObjectInfo
def dailyLuck(seed,daysPlayed,steps):
    #DailyLuck random is initialised before daysPlayed is incremented
    localDaysPlayed = daysPlayed - 1;
    rand = CSRandomLite(seed//100 + localDaysPlayed * 10 + 1 + steps)
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
    rand = CSRandomLite(seed//100 + localDaysPlayed * 10 + 1 + steps)
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
    return (oneTimeRandomGetLong(a,b,c,d) >> 11) * 1.11022302462516E-16

def oneTimeRandomGetLong(a,b,c,d):
    num1 = ((( a ^ ( (b >> 14) |  b << 50)) + (( (c >> 31) |  c << 33) ^ ( (d >> 18) |  d << 46))) * 1911413418482053185);
    num2 = (((( (a >> 30) |  a << 34) ^  c) + (( (b >> 32) |  b << 32) ^ ( (d >> 50) |  d << 14))) * 1139072524405308145);
    num3 = (((( (a >> 49) |  a << 15) ^ ( (d >> 33) |  d << 31)) + ( b ^ ( (c >> 48) |  c << 16))) * 8792993707439626365);
    num4 = (((( (a >> 17) |  a << 47) ^ ( (b >> 47) |  b << 17)) + (( (c >> 15) |  c << 49) ^  d)) * 1089642907432013597);
    return (( num1 ^  num2 ^ ( (num3 >> 21) |  num3 << 43) ^ ( (num4 >> 44) |  num4 << 20)) * 2550117894111961111 + (( (num1 >> 20) |  num1 << 44) ^ ( (num2 >> 41) |  num2 << 23) ^ ( (num3 >> 42) |  num3 << 22) ^  num4) * 8786584852613159497 + (( (num1 >> 43) |  num1 << 21) ^ ( (num2 >> 22) |  num2 << 42) ^  num3 ^ ( (num4 >> 23) |  num4 << 41)) * 3971056679291618767);

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

    rand = CSRandomLite(seed//2+daysPlayed+level*100)
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
    rand = CSRandomLite(daysPlayed * level + 4 * level + seed//2)
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
    rand = CSRandomLite(geodesCracked + 1 + seed // 2)
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
    rand = CSRandomLite(seed//2 + daysPlayed)
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
    rand = CSRandomLite(seed//2 + daysPlayed)
    dayOfWeek = daysPlayed % 7
    if dayOfWeek == 3:
        return rand.Next(698,709)
    if dayOfWeek == 6:
        index = rand.Next(194,245)
        if index == 217:
            index = 216
        return index
    return None


def randomItemFromSeason(gameID, day, seedAdd, furnace=False, forQuest=False):
    season = (day-1) // 28 % 4
    rand = CSRandomLite(gameID + day + seedAdd)
    source = [68, 66, 78, 80, 86, 152, 167, 153, 420]
    if furnace:
        source.extend([334,335,336,338])
    source.extend({
		0 : [16,18,20,22,129,131,132,136,137,142,143,145,147,148,152,167,267],
		1 : [128,130,132,136,138,142,144,145,146,149,150,155,396,398,402,267], 
		2 : [404,406,408,410,129,131,132,136,137,139,140,142,143,148,150,154,155,269],
		3 : [412,414,416,418,130,131,132,136,140,141,144,146,147,150,151,154,269]
		}[season])
    if forQuest and rand.Sample() >= 0.4:
        source.extend([194])
    r = rand.Next(len(source))
    return source[r]

def getItemFromIndex(index):
    if index == "DishOfTheDay":
        return index
    return ObjectInfo[index].split('/')[0]


def test14GiantCrops(seed):
    for x in range(59,74):
        for y in range(19,24):
            for day in range(14,28):
                if giantCrop(seed,day,x,y,"1.4"):
                    print(str(x)+","+str(y)+" "+str(day))

if __name__ == '__main__':
    #findVaultGiantCropSeed();
    #findMine50Seed();
    print(uniqueKrobusStock(6,6))
    test14GiantCrops(0)