
from CSRandom import CSRandomLite as Cs
import Location
import SeedUtility
import TrashCans

def IsQuestItem(seed,daysPlayed):
    result = Cs(seed + daysPlayed).Sample()
    return result >= 0.6

def GetRandomPerson(seed,daysPlayed,list):
    return list[Cs(seed + daysPlayed).Next(len(list))]

def IsRightRandomPerson(seed,daysPlayed,list,person,report=False):
    foundPerson = GetRandomPerson(seed,daysPlayed,list)
    if report:
        print(foundPerson)
    return foundPerson == person

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
            return [254,256]
        return [254,256,264,262,260]
    elif season == 2:
        if firstWeek:
            return [272,278]
        return [270,276,280,272,278]

def FindMarriageSeed():
    for seed in range(-2147483648,0): #TAS - 886567826
        #if seed % 1000000 == 0:
        #    print("searching: "+str(seed))
        AnalyseSeed(seed,False,0,False,0.08)

def AnalyseSeed(seed,report=False,horseradishDay=0,strict=False,inputluck=0.8):
    result = Cs(seed + 20).Sample()
    if not( 0.75 <= result < 0.7599646317 ):
         return


    if report:
        print(seed)
    goodSpringItems = {16,18,20,22,24}
    goodSummerItems = {396,398,402,254,256,264,262,260}
    friendships = ["Robin","Lewis","Shane","Marnie"]
    
    found = False
    possibleSteps = []
    possibleSteps2 = []
    steps = 0
    if strict:
        for steps in range(240):
            if SeedUtility.dishOfTheDay(seed,20,steps) == 215:
                possibleSteps.extend([steps])
                found = True

        if not found:
            return
        lowestLuck = 999
        beststeps = 0
        for steps in possibleSteps:
            luck = SeedUtility.dailyLuck(seed,20,steps)
            if TrashCans.checkSpecificTrash(seed,20,5,False,luck) == 'DishOfTheDay':
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
    days = [20,22,26,28,30,43,45,47,49,51,53]
    for day in days:
        luck = inputluck
        if strict:
            if count == 0:
                luck = SeedUtility.dailyLuck(seed,3,beststeps)

        if count == 0 and not TrashCans.checkSpecificTrash(seed,day,5,False,luck) == 'DishOfTheDay':
            return


        if count < 2:
            recipes = 1
        else:
            recipes = 2

        if day > 46: #7 heart
            recipes = recipes + 1

        item = GetQuestItem(seed, day,recipes)

        checkedTrash = False
        cans = [0,1,2,5,6]
        if not ( item in goodSpringItems or item in goodSummerItems ):
            dailyTrash.clear
            dailyTrash = TrashCans.checkCans(seed,day,cans,False,luck)
            if (dailyTrash == None or item not in dailyTrash) and (availableTrash == None or item not in availableTrash ):
                if day == 20:
                    return

                continue
            checkedTrash = True

        if day == 30 and item in {254,256,264,262,260}:
            return

        if not checkedTrash:
            dailyTrash.clear
            dailyTrash = TrashCans.checkCans(seed,day,cans,False,luck)

        availableTrash.extend(dailyTrash)
        if checkedTrash:
            availableTrash.remove(item)
        firstQuest = False
        count = count + 1

        validDay.extend([day])
        if report:
            print(str(day)+": "+SeedUtility.getItemFromIndex(item))
    if count < 8:
        return

    if not report:
        print(str(seed)+" "+str(count))

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

    for daysPlayed in range(2,8):
        print(Cs(256151046 + daysPlayed).Sample())

    #print(SeedUtility.getItemFromIndex(GetQuestItem(1946946589,20,2)))
    for num in range(6):
        print(SeedUtility.getItemFromIndex(GetQuestItem(1165064550, 47,num)))

    #FindMarriageSeed()

    if False:

        
    
        
        #seeds=[1099580,1621067,13197449,13253836,14376653,23354966,24482084,29668500,33019044,36418818,39202837,41906902,45199074,47174141,58989516,68616293,76541221,79856740,107002132,120373944,124277074,124503849,137900763,140263851,148611917,150719914,153647209,164633610,172780564,176114497,179064913,179106986,185977685,195590144,208195965,230090530,240206824,252190399,270198820,275841751,277303269,280970553,282394948,302843647,305426554,317030988,319715027,325405092,331705851,332510500,334379504,335984966,336623419,339655885,345086154,348397479,359311284,371149357,374137453,379780696,403210223,405725193,416407920,420275357,424285825,425071767,434147292,436587570,439563448,445248653,462407387,467143218,477592681,479112571,484844133,494786331,501138416,508349441,511348886,512186355,519899201,536071639,537104583,546205120,548215865,721979759]
        seeds=[44385714,57349479,59812744,114516816,122349683,123819116,130518108,135257930,199942152,211876790,289882631,352417095,361177195,390981616,485026073,506297726,596271226,677983771,711924098,739797732,745502758,795905664,826738766,829957829,841368015,849902299,883793329,897744148,909969105,914770576,954644934,965275933,995043342,1048059879,1162594997,1165064550,1183904531,1283823644,1288378965,1308015858,1314393026,1378160405,1402229365,1480775199,1482135024,1524641318,1547839120,1587720635,1597189131,1604706885,1662107285,1704962582,1746561776,1757330165,1793763545,1813217832,1881072467,1890478489,1897949109,1902878694,1909128127,1912200258,1929262739,1981818569,1983617630,1987136265,2009648681,2064171663,2145893461,2146639426]
        seeds = [-2057812015,-1995562430,-1983690601,-1888760827,-1863134029,-1778107238,-1754139391,-1675335501,-1667892060,-1626122478,-1614979312,-1599966278,-1591269789,-1469932983,-1329079527,-1309098380,-1295591100,-1283344025,-1211611630,-1156969653,-1030060506,-1016577038,-993318657,-952301194,-595166287,-549031214,-534546757,-516595749,-506706902,-464253517,-300001392,-213715221,-95365441,-40779918,-28227452]
        seeds = [-40779918]
        for seed in seeds:
            days = AnalyseSeed(seed,True,0,True,-0.1)
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
