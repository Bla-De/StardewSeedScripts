from CSRandom import MAX_INT, CSRandomLite,CSRandom
from ObjectInfo import ObjectInfo
import TrashCans
import Utility

omniItems = [538, 542, 548, 549, 552, 555, 556, 557, 558, 566, 568, 569, 571, 574, 576, 541, 544, 545, 546, 550, 551, 559, 560, 561, 564, 567, 572, 573, 577, 539, 540, 543, 547, 553, 554, 562, 563, 565, 570, 575, 578, 121, 122, 123]
geodeItems = [538, 542, 548, 549, 552, 555, 556, 557, 558, 566, 568, 569, 571, 574, 576, 121]
frozenItems = [541, 544, 545, 546, 550, 551, 559, 560, 561, 564, 567, 572, 573, 577, 123]
magmaItems = [539, 540, 543, 547, 553, 554, 562, 563, 565, 570, 575, 578, 122]
troveItems = [100, 101, 103, 104, 105, 106, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 166, 373, 797]


def dishOfTheDay(seed,daysPlayed,steps,rand=None):
    #random is initialised before daysPlayed is incremented
    localDaysPlayed = daysPlayed - 1;
    if rand == None:
        rand = CSRandomLite(int(seed/100) + localDaysPlayed * 10 + 1 + steps)
    dayOfMonth = 0
    if localDaysPlayed > 0:
        dayOfMonth = ((localDaysPlayed-1) % 28) + 1
  #  for index in range(100):
  #      print( str( min(.10, rand.Next(-100, 101) / 1000) ) )
    for index in range(dayOfMonth):
        rand.Sample()
    dish = rand.Next(194,240)
    while dish in { 346, 196, 216, 224, 206, 395, 217 }:
        dish = rand.Next(194,240)
     #Dish additional number
    number = rand.Next(1,4 + 10 if rand.Sample() < 0.08 else 0); #Dish number
    rand.Sample(); #Object constructor
    return dish,number

def dailyLuck(seed,daysPlayed,steps,hasFriends=False,rand=None):
    if rand == None:
        #random is initialised before daysPlayed is incremented
        rand = CSRandomLite(int(seed/100) + (daysPlayed - 1) * 10 + 1 + steps)
        dishOfTheDay(seed,daysPlayed,steps,rand)

    if hasFriends:
        rand.Sample(); #Friendship
        rand.Sample(); #Friendship mail
    rand.Sample(); #Rarecrow society
    return min(.10, rand.Next(-100, 101) / 1000)

def weatherTomorrow(seed,daysPlayed,steps,weatherToday=0,hasFriends=False,rand=None,version="1.5"):
    if rand == None:
        #random is initialised before daysPlayed is incremented
        rand = CSRandom(int(seed/100) + (daysPlayed - 1) * 10 + 1 + steps)
        dishOfTheDay(seed,daysPlayed,steps,rand)
        dailyLuck(seed,daysPlayed,steps,hasFriends,rand)

    #Ginger isle
    if version == "1.5":
        rand.Sample();

    if weatherToday == 2:
        num = rand.Next(16,64)
        for index in range(num):
            rand.Sample()
            rand.Sample()
            rand.Sample()
            rand.Sample()
            rand.Sample()
            rand.Sample()

    season = (daysPlayed-1) // 28 % 4
    spring = season == 0
    summer = season == 1
    fall = season == 2
    winter = season == 3

    dayOfMonth = (((daysPlayed-1) % 28) + 1)
    if not summer:
        if not winter:
            chanceToRainTomorrow = 0.183
        else:
            chanceToRainTomorrow = 0.63
    else:
        chanceToRainTomorrow = dayOfMonth * (3.0 / 1000.0) + .12

    if rand.Sample() < chanceToRainTomorrow:
        weather = 1
        if summer and rand.Sample() < 0.85 or not winter and rand.Sample() < 0.25 and dayOfMonth > 2 and dayOfMonth > 27:
            weather = 3
        if winter:
            weather = 5
    elif daysPlayed <= 2 or ( not spring or rand.Sample() >= 0.2 ) and ( not fall or rand.Sample() >= 0.6 ):
        weather = 0
    else:
        weather = 2

    return weather


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


def nextGeodeItem(seed,geodesCracked,geodeType,deepestMineLevel=0,version="1.4",hasCoconutHat=False):
    
    rand = CSRandomLite(geodesCracked + int(seed / 2))

    if version == "1.4" or version == "1.5":
        num1 = rand.Next(1,10)
        rand.Advance(num1)
        num2 = rand.Next(1, 10)
        rand.Advance(num2)
    
    if version == "1.5":
        rand.Advance(1) #QI beans

    if geodeType == "Coconut":
         if (rand.Sample() < 0.05 and not hasCoconutHat):
                return ("Hat",1);
         case = rand.Next(7)
         
         if case == 0:
             return (69, 1)
         if case == 1:
             return (835, 1)
         if case == 2:
             return (833, 5)
         if case == 3:
             return (831, 5)
         if case == 4:
             return (820, 1)
         if case == 5:
             return (292, 1)
         if case == 6:
             return (386, 5)
            

    if geodeType != "Trove" and rand.Sample() < 0.5:
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
        geodeSet = [];
        if geodeType == "Omni":
            geodeSet = omniItems
        if geodeType == "Geode":
            geodeSet = geodeItems
        if geodeType == "Frozen":
            geodeSet = frozenItems
        if geodeType == "Magma":
            geodeSet = magmaItems
        if geodeType == "Trove":
            geodeSet = troveItems

        item = (geodeSet[rand.Next(len(geodeSet))],1)

        if geodeType == "Omni":
            if rand.Sample() < 0.008 and geodesCracked > 15:
                item = (74, 1)

        return item

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


def randomItemFromSeason(gameID, day, seedAdd, furnace=False, forQuest=False,recipesKnown=1,mineFloor=0,desert=False):
    season = (day-1) // 28 % 4
    rand = CSRandom(gameID + day + seedAdd)
    source = [68, 66, 78, 80, 86, 152, 167, 153, 420]
    if mineFloor > 40:
        source.extend([62,70,72,84,422])
    if mineFloor > 80:
        source.extend([64,60,82])
    if desert:
        source.extend([88,90,164,165])
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
    if index == "Hat":
        return index
    return ObjectInfo[index].split('/')[0]

def fairyCropIndex(seed,days,numberOfHoeDirts=0):
    #Assumes all other terrainFeatures have been cleared (trees/grass/flooring)
    rand = CSRandom(seed+days)
    if numberOfHoeDirts == 0:
        return rand.Sample()
    return rand.Next(numberOfHoeDirts)

def totalHarvest(seed,chanceForExtra,level=0,fert=0,dailyLuck=0.0,LuckLevel=0):
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
    if rand.Sample() < 9.99999974737875E-05 + dailyLuck/1200 + LuckLevel/1500:
        num1 = num1 * 2

    return num1

def test14GiantCrops(seed,days,xRange,yRange):
    for day in days:
        for x in xRange:
            for y in yRange:
                if giantCrop(seed,day,x,y,"1.4"):
                    print(str(x)+","+str(y)+" day: "+str(day))

def findBestHarvest():
    #8820192
    for seed in range(2000000000):
        num = totalHarvest(seed,0.2,level=0,fert=0,dailyLuck=-0.1,LuckLevel=0)
        if num > 10:
            print(str(seed) + " " + str(num))
def summer2potatodrops():
    for seed in range(611235816,611235816+79*7+64*11+28):
        num = totalHarvest(seed,0.2)
        if num > 3:
            print(str(seed) + " " + str(num))

def printGiantCropHarvest(seed,spots,lastDay):
    for spot in spots:
        print(spot)
        for day in range(spot[2],lastDay+1):
            print(str(day) + " " + str(giantCropAmount(seed,day,spot[0]-1,spot[1]-1)))

def printPotatoSpots(seed,day):
     for y in range(18,25):
        for x in range(57,69):
            print(str(x)+","+str(y)+" harvest: "+ str(totalHarvest(seed+day+x*7+y*11,0.2)))

def checkMinesSpotCondensed(seed, ladder=False,geologist=False,excavator=False,floor=0):
    objects = []
    r = CSRandomLite(seed)
    r.Sample()
    if not ladder:
        r.Sample()
    if geologist: 
        r.Sample()
    if r.Sample() < 0.022 * (1+int(excavator)):
        if geologist and r.Sample() < 0.5:
            objects.extend([535])
        objects.extend([535])
    if r.Sample() < 0.005 * (1+int(excavator)):
        if geologist and r.Sample() < 0.5:
            objects.extend([749])
        objects.extend([749])
    if r.Sample() < 0.05:
        r.Sample()
        r.Sample()
        if r.Sample() < 0.25:
            objects.extend([382])
        if floor < 40:
            if floor >= 20 and r.Sample() < 0.1:
                objects.extend([380])
            else:
                objects.extend([378])
        elif floor < 80:
            if floor >= 60 and r.Sample() < 0.1:
                objects.extend([384])
            elif r.Sample() >= 0.75:
                objects.extend([378])
            else:
                objects.extend([380])
        elif floor < 120:
            if r.Sample() >= 0.75:
                if r.Sample() >= 0.75:
                    objects.extend([378])
                else:
                    objects.extend([380])
            else:
                objects.extend([384])
        else:
            if r.Sample() < 0.01 + (floor - 120)/2000:
                objects.extend([386])
            else:
                if r.Sample() >= 0.75:
                    if r.Sample() >= 0.75:
                        objects.extend([378])
                    else:
                        objects.extend([380])
                else:
                    objects.extend([384])

    return objects

def checkMinesSpot(seed,floor,x,y, ladder=False,geologist=False):
    return checkMinesSpotCondensed(x*1000 + y + floor + int(seed/2),ladder,geologist)

def checkAllMinesSpots():
    seeds = range(0,500000000,2)
    #seeds = [2896322,6285359,13038485,18403015,18492950,25824924,27221569,28708149,34668426,38850312,39519095,40915740,46272221,46876017,48174678,49661258,51057903,53033396,55604636,58389877,58479812,61868849,63175559,65240987,69135836,70597468,73986505,75383150,78044325,85688284,90251916,92227409,92947222,94433802,96409295,102369572,106551458,106641393,107220241,108616886,112511735,113908380,113973367,114577163,115370012,118759049,124719326,126180958,141181839,143084296,147142116,151992785,153389430,162134948,163531593,170070718,174252604,174342539,186460195,192420472,195303697,196765329,200154366,202129859,202635671,202725606,206907492,212272022,214843262,218232299,219025148,224985425,229836094,230439890,231232739,231901522,242043685,250797252,251466035,258219161,261608198,262401047,263004843,263069830,267855512,268361324,273815789,274608638,277997675,280568915,285933445,290205266,299627616,300420465,304894162,306380742,311231411,312628056,317191688,318498398,318588333,324458675,330705989,336062470,336666266]
    for seed in seeds:
        objects = checkMinesSpotCondensed(seed,False,False)
        if len(objects) == 4:
            print(seed)

def geodeTest():
    seed = 1
    for i in range(1,10):
        print(nextGeodeItemName(seed,i,"Omni",version="1.5"))

def rainCheck():
    seed = 758980005

    steps = range(13,48)

    days = range(2,20)

    for step in steps:
        print("Step: " + str(step))
        for day in days:
            print("day: " + str(day) + " " + str(weatherTomorrow( seed,day,step )))

def remixedMinesChest(seed, floor):
    items = []
    if floor == 10:
        items = [("Boots",506),("Boots",507),("MeleeWeapon",12),("MeleeWeapon",17),("MeleeWeapon",22),("MeleeWeapon",31)]
    elif floor == 20:
        items = [("MeleeWeapon",11),
                ("MeleeWeapon",24),
                ("MeleeWeapon",20),
                ("Ring",517),
                ("Ring",519)]
    elif floor == 50:
        items = [("Boots",509),
                ("Boots",510),
                ("Boots",508),
                ("MeleeWeapon",1),
                ("MeleeWeapon",43)]
    elif floor == 60:
        items = [("MeleeWeapon",21),
                ("MeleeWeapon",44),
                ("MeleeWeapon",6),
                ("MeleeWeapon",18),
                ("MeleeWeapon",27)]
    elif floor == 80:
        items = [("Boots",512),
                ("Boots",511),
                ("MeleeWeapon",10),
                ("MeleeWeapon",7),
                ("MeleeWeapon",46),
                ("MeleeWeapon",19)]
    elif floor == 90:
        items = [("MeleeWeapon",8),
                ("MeleeWeapon",52),
                ("MeleeWeapon",45),
                ("MeleeWeapon",5),
                ("MeleeWeapon",60)]
    elif floor == 110:
        items = [("Boots",514),
                ("Boots",878),
                ("MeleeWeapon",50),
                ("MeleeWeapon",28)]

    rand = CSRandomLite((seed*512) + floor)

    return items[(rand.Next(len(items)))]

def enchantment(seed,type,times=0,previousEnchantments=[]):
    enchantments = []
    if type == "Weapon":
        enchantments = ['Artful', 'Bug Killer', 'Vampiric', 'Crusader', 'Haymaker']
    elif type == "Hoe":
        enchantments = ['Reaching','Generous','Archaeologist','Efficient','Swift']

    for previous in previousEnchantments:
        if previous in enchantments:
            enchantments.remove(previous)

    rand = CSRandomLite(seed + times)
    
    rand = CSRandomLite(seed + times)

    return enchantments[(rand.Next(len(enchantments)))]

def monsterFloor(seed,daysPlayed,level,version="1.5"):
    result = "";
    if level < 120 and level % 5 == 0:
        return False
    if level < 120 and level % 40 < 5:
        return False
    if level < 120 and level % 40 > 30:
        return False
    if level < 120 and level % 40 == 19:
        return False

    if version=="1.3":
        rand = CSRandomLite(int(seed/2)+daysPlayed+level)
    else:
        rand = CSRandomLite(int(seed/2)+daysPlayed+level*100)
    if rand.Sample() < 0.044:

        if rand.Sample() < 0.5:
            result = "Monster"
        else:
            result = "Slime"

        if level > 126:
            if rand.Sample() < 0.5:
                result = "Dino"

    return result


def doesSeedHaveMonsterFloorMines(seed,daysPlayed,deepestFloor):
    for floor in range(1,deepestFloor):
        if monsterFloor(seed,daysPlayed,floor):
            return True
    return False

def isMushroomFloor(seed,day,floor,version="1.5"):
	if (floor % 5 == 0):
		return False

	if monsterFloor(seed,day,floor,version):
		return False
	
	if False: 
        #(rng.Sample() < 0.044 && save.quarryUnlocked && floor % 40 > 1 ):
		#if (rng.Sample() < 0.25):
		#	quarryLevel.push(mineLevel + '*');
		#else:
		#	quarryLevel.push(mineLevel);
		#skipMushroomCheck = true;
		return False
	
	if version=="1.3":
		rng = CSRandomLite(int(seed/2)+floor+day)
	else:
		rng = CSRandomLite(day * floor + (4 * floor) + seed // 2);
	num = rng.Sample()
	if (num < 0.3 and floor > 2):
		rng.Sample()
	rng.Sample()
    
	num = rng.Sample()
	if (num < 0.035 and floor > 80):
		return True
	
def forageQuality(seed,day,x,y,forageLevel):
    r = CSRandomLite(seed//2 + day + x + y*777)
    if r.Sample() < forageLevel / 30:
        return "Gold"

    if r.Sample() < forageLevel / 15:
        return "Silver"

def winterStarGift(seed,year,who):
    rand = CSRandomLite(seed//2 + year + 25 + 3 + 29)
    items = []
    if who == "Clint":
        items.extend([337,336])
        items.extend(rand.Next(535,538))
    elif who == "Marnie":
        items.extend(176)
    elif who == "Robin":
        items.extend(388,390,709)
    elif who == "Willy":
        items.extend(690,687,703)
    elif who == "Evelyn":
        items.extend(223)
    elif who == "Vincent" or who == "Jas" or who == "Leo":
        items.extend(330,103,394)
        items.extend(rand.Next(535,538))
    else:
        items.extend(608,651,611,517,466,422,392,348,346,341,221,64,60,70)

    return items[rand.Next(len(items))]

def winterStarRecipient(seed,year):
    rand = CSRandomLite((seed//2)^year)

def GetPossibleCrops(season,firstWeek):
    if season == 0:
        if firstWeek:
            return [24,192]
        return [190,188,24,192]
    elif season == 1:
        if firstWeek:
            return [254,256]
        return [254,256,264,262,260]
    elif season == 2:
        if firstWeek:
            return [272,278]
        return [270,276,280,272,278]

def GetQuestItem(seed,daysPlayed,recipesKnown=1,mineFloor=0, furnaceRecipe=False, desert=False):
    random = CSRandomLite(seed + daysPlayed)
    random.Sample() # Selecting person
    season = (daysPlayed-1) // 28 % 4
    if season != 3 and random.Sample() < 0.15:
        possibleCrops = GetPossibleCrops(season, ((daysPlayed-1 )% 28)+1 <= 7)
        return possibleCrops[random.Next(len(possibleCrops))]
    return randomItemFromSeason( seed, daysPlayed, 1000, furnaceRecipe, True,recipesKnown,mineFloor,desert)


def RainOutput():
    seed = 303533402
    for day in range(3,14):
        output = ""
        for steps in range(5,70):
            output += str(weatherTomorrow(seed,day,steps,hasFriends=True))
            output += '\t'
        print(output)

def SupplyCrates(seed,x,y,houseLevel=0):

    r = CSRandomLite(floatingTruncation(seed+x*777+y*7))
    if houseLevel == 0:
        result = r.Next(6)
        if result == 0:
            return (770,r.Next(3,6))
        elif result == 1:
             return(371, r.Next(5, 8));
                            
        elif result == 2:
             return(535, r.Next(2, 5));
                            
        elif result == 3:
             return(241, r.Next(1, 3));
                            
        elif result == 4:
             return(395, r.Next(1, 3));
                            
        elif result == 5:
             return(286, r.Next(3, 6));
                            
    elif houseLevel == 1:
        result = (r.Next(9))
                        
        if result == 0:
            return(770, r.Next(3, 6));
        elif result == 1:
            return(371, r.Next(5, 8));
        elif result == 2:
            return(749, r.Next(2, 5));
        elif result == 3:
            return(253, r.Next(1, 3));
        elif result == 4:
            return(237, r.Next(1, 3));
        elif result == 5:
            return(246, r.Next(4, 8));
        elif result == 6:
            return(247, r.Next(2, 5));
        elif result == 7:
            return(245, r.Next(4, 8));
        elif result == 8:
            return(287, r.Next(3, 6));
    elif houseLevel == 2:
        result = (r.Next(8))
        if result == 0:
            return(770,r.Next(3, 6));
        elif result == 1:
            return(920,r.Next(5, 8));
        elif result == 2:
            return(749,r.Next(2, 5));
        elif result == 3:
            return(253,r.Next(2, 4));
        elif result == 4:
            return(r.Next(904, 906), r.Next(1, 3));
        elif result == 5:
            return(246, r.Next(4, 8));
            return(247, r.Next(2, 5));
            return(245, r.Next(4, 8));
        elif result == 6:
            return(275, 2);
        elif result == 7:
            return(288, r.Next(3, 6));

def floatingTruncation(num):
    working = num
    length = len(str(working))
    if length > 9:
        factor = 10**(length-9)
        working = int(working/factor)
        working = working * factor

    working = working & 0xffffffff

    if working > MAX_INT:
        working = working - MAX_INT  * 2

    return working

def troveRun():
    treasures = 0
    maxTreasures = 0;

    for seed in range(0,1000000000,2):
        item = nextGeodeItemName(seed,0,"Trove",0,"1.5")[0]
        if item == "Treasure Chest":
            treasures += 1
        else:
            if treasures > maxTreasures:
                print(seed)
                print(treasures)
                maxTreasures = treasures
            treasures = 0
  
MAX_INT = 0x7FFFFFFF
MIN_INT = 0x80000000
def int_overflow(val):
	if not -MAX_INT-1 <= val <= MAX_INT:
		val = (val + (MAX_INT + 1)) % (2 * (MAX_INT + 1)) - MAX_INT - 1
	return val

if __name__ == '__main__':
	count = 0
	bestCount = 0
	bestSeed = 0
	for seed in range(1000000000):
		count = totalHarvest(seed,0.02,0,0,0.1,7)
		if count > bestCount:
			bestCount = count
			bestSeed = seed

	print(bestCount)
	print(bestSeed)
		
