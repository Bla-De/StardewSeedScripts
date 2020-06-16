
from CSRandom import CSRandomLite as Cs
import Location
import SeedUtility
import TrashCans

def IsQuestItem(seed,daysPlayed):
    return Cs(seed + daysPlayed).Sample() >= 0.6

def GetRandomPerson(seed,daysPlayed,list):
    return list[Cs(seed + daysPlayed).Next(len(list))]

def IsRightRandomPerson(seed,daysPlayed,list,person):
    return GetRandomPerson(seed,daysPlayed,list) == person

def GetQuestItem(seed,daysPlayed,recipesKnown=1,mineFloor=0):
    random = Cs(seed + daysPlayed)
    random.Sample() # Selecting person
    season = (daysPlayed-1) // 28 % 4
    if season != 3 and random.Sample() < 0.15:
        possibleCrops = GetPossibleCrops(season, ((daysPlayed-1 )% 28)+1 <= 7)
        return possibleCrops[random.Next(len(possibleCrops))]
    return SeedUtility.randomItemFromSeason( seed, daysPlayed, 1000, False, True,recipesKnown,mineFloor)

def GetPossibleCrops(season,firstWeek):
    if season == 0:
        if firstWeek:
            return [24,192]
        return [190,188,24,192]
    elif season == 1:
        if firstWeek:
            return [264,262,260]
        return [254,256,264,262,260]
    elif season == 2:
        if firstWeek:
            return [272,278]
        return [270,276,280,272,278]

def FindMarriageSeed():
    for seed in range(2127999038,2147483648): #TAS - 886567826
        #if seed % 1000000 == 0:
        #    print("searching: "+str(seed))
        AnalyseSeed(seed,False,0,False,0.08)

def AnalyseSeed(seed,report=False,horseradishDay=0,strict=False,inputluck=0.8):
    
    if report:
        print(seed)
    goodSpringItems = {16,18,20,22,24,190,192}
    goodSummerItems = {396,398,402}
    friendships = ["Robin","Lewis","Shane","Marnie"]

    if not report:
        if not IsQuestItem(seed,20) or not IsRightRandomPerson(seed,20,friendships,"Shane"):
            return

    
    found = False
    possibleSteps = []
    possibleSteps2 = []
    steps = 0
    if strict:
        for steps in range(240):
            if SeedUtility.dishOfTheDay(seed,3,steps) == 215:
                possibleSteps.extend([steps])
                found = True

        if not found:
            return
        lowestLuck = 999
        beststeps = 0
        for steps in possibleSteps:
            luck = SeedUtility.dailyLuck(seed,3,steps)
            if TrashCans.checkSpecificTrash(seed,3,5,False,luck) == 'DishOfTheDay':
                possibleSteps2.extend([steps])
                if luck < lowestLuck:
                    beststeps = steps
                    lowestLuck = luck

        if possibleSteps2 == []:
            return
        steps = beststeps
        if report:
            print(possibleSteps2)
    if strict:
        for day in range(1,22):
            event = SeedUtility.nightEvent(seed,day)
            if event == "Meteor" or event == "Fairy":
                return


    
    count = 0
    firstQuest = False
    horseradishQuest = False
    dailyTrash = list()
    availableTrash = list()
    validDay = list()
    #days = [6,8,10,16,20,22]
    friendships = []
    for day in range(2,29):
        if day in {13,24}:
            continue
        if firstQuest:
            friendships = ["Shane"]
        elif day < 20:
            friendships = ["Robin","Lewis","Shane"]
        else:
            friendships = ["Robin","Lewis","Shane","Marnie"]
        if not IsQuestItem(seed,day):
            continue
        if not firstQuest and not IsRightRandomPerson(seed,day,friendships,"Shane"):
            continue

        luck = inputluck
        if strict:
            if count == 0:
                luck = SeedUtility.dailyLuck(seed,3,beststeps)

        if count == 0 and not TrashCans.checkSpecificTrash(seed,day,5,False,luck) == 'DishOfTheDay':
            return


        if count < 4: # 3 for TAS, 4 for seeded
            recipes = 1
        else:
            recipes = 2

        if day > 20: #7 heart
            recipes = recipes + 1

        if day > 24: #foraging 2
            recipes = recipes + 1

        item = GetQuestItem(seed, day,recipes)

        checkedTrash = False
        cans = [0,1,2,5,6]
        if item not in goodSpringItems:
            dailyTrash.clear
            dailyTrash = TrashCans.checkCans(seed,day,cans,False,luck)
            if (dailyTrash == None or item not in dailyTrash) and (availableTrash == None or item not in availableTrash ):
                if day == 20:
                    return

                continue
            checkedTrash = True

        if day < 5 and item == 24:
            continue
        if day < 7 and item == 192:
            continue
        if day < 14 and item == 190:
            continue

        if not checkedTrash:
            dailyTrash.clear
            dailyTrash = TrashCans.checkCans(seed,day,cans,False,luck)

        availableTrash.extend(dailyTrash)
        if checkedTrash:
            availableTrash.remove(item)
        firstQuest = False
        count = count + 1

        if item == 16:
            horseradishQuest = True

        validDay.extend([day])
        if report:
            print(str(day)+": "+SeedUtility.getItemFromIndex(item))
    if count < 7:
        return

    if not report:
        print(str(seed)+" "+str(count) + " " + str(horseradishQuest))

    return validDay

def checkForGoodHorseradish(seed,day):
    forest = Location.createForest()
    forest.processDay(seed,day)
    for spawn in forest.items.items():
        if spawn[1] == "Wild Horseradish":
            x = spawn[0][0]
            y = spawn[0][1]

            if 47 <= x <= 97 and y <= 37:
                return spawn[0]

    return None

def checkQuests(seed,days):
    for day in days:
        if not IsQuestItem(seed, day):
            continue

        if day ==2:

            personList = ["Robin","Lewis","Demetrius",]
        elif day < 8:
            personList = ["Robin","Lewis","Demetrius","Willy"]
        else:
            personList = ["Robin","Lewis","Demetrius","Willy","Marnie"]
        print(str(day) + " " + SeedUtility.getItemFromIndex(GetQuestItem(seed,day)) + " " + GetRandomPerson(seed,day,personList))

if __name__ == '__main__':

    #print(SeedUtility.getItemFromIndex(GetQuestItem(436587570,22,4)))


    FindMarriageSeed()

    if True:

        
    
        
        #seeds=[1099580,1621067,13197449,13253836,14376653,23354966,24482084,29668500,33019044,36418818,39202837,41906902,45199074,47174141,58989516,68616293,76541221,79856740,107002132,120373944,124277074,124503849,137900763,140263851,148611917,150719914,153647209,164633610,172780564,176114497,179064913,179106986,185977685,195590144,208195965,230090530,240206824,252190399,270198820,275841751,277303269,280970553,282394948,302843647,305426554,317030988,319715027,325405092,331705851,332510500,334379504,335984966,336623419,339655885,345086154,348397479,359311284,371149357,374137453,379780696,403210223,405725193,416407920,420275357,424285825,425071767,434147292,436587570,439563448,445248653,462407387,467143218,477592681,479112571,484844133,494786331,501138416,508349441,511348886,512186355,519899201,536071639,537104583,546205120,548215865,721979759]
        seeds=[24482084,35164053,68616293,87255430,99701900,110202890,121734144,172057854,206288634,217556191,346337508,386746886,412917712,434907014,472483143,491968734,510678951,605865399,663290882,713701525,732755104,789998672,865086561,878135988,887258647,998846025,1028766074,1049072902,1058828863,1064189591,1069740572,1104058040,1125612476,1127390066,1139058999,1156806487,1167332828,1223526556,1245141504,1391110072,1450256021,1490158896,1571922210,1584131314,1591162386,1611639981,1647313840,1660937529,1753285577,1849678630,1868424789,1890571792,1924974476,1940010252,1940685248,1946946589,1957799055,1979893195,1986613568]
        seeds = []
        
        for seed in seeds:
            days = AnalyseSeed(seed,True,0,True,0.1)
            #days = []
            for day in days:
                flag = False
                Cans = TrashCans.dayToYSD(day) + "\n"
                for i in [0,1,2,5,6]:
                    can = TrashCans.GarbageLocations[i]
                    item,minLuck = TrashCans.checkTrash(seed,day,i,can[0][0],can[0][1],False,0.08,"1.4",True)
                    if item is not None:
                        flag = True
                        Cans = Cans + ("\t %s : %s\n" % (can[1],SeedUtility.getItemFromIndex(item)+ ", Minimum luck: "+str(minLuck) ))
                if flag:
                    print(Cans)
                
                print(checkForGoodHorseradish(seed,day))
            for day in range(30,37):
                if not IsQuestItem(day,seed):
                    continue
                if not IsRightRandomPerson(seed,day,["Robin","Lewis","Shane","Marnie"],"Shane"):
                    continue
                print(SeedUtility.getItemFromIndex(GetQuestItem(seed,day)))
