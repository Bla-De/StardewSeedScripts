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

def giantCrop(seed,daysPlayed,x,y):
    rand = CSRandomLite(seed + daysPlayed + x*2000 + y)
    return rand.Sample() < 0.01

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





            

#if __name__ == '__main__':
    #findVaultGiantCropSeed();
    #findMine50Seed();