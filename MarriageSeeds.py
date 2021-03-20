
from CSRandom import CSRandomLite as Cs
import Location
import SeedUtility
import TrashCans
import sys
from os import path

absolute_path = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
filename = path.abspath(path.join(absolute_path, 'MarriageResults.txt'))

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
    for seed in range(1000000000): #TAS - 886567826
        if seed % 1000000 == 0:
            print("searching: "+str(seed))
            f = open(filename,"at")
            f.write("searching: " + str(seed) + '\n')
            f.close()
        AnalyseSeed(seed,False,0,False,0.1)

def AnalyseSeed(seed,report=False,horseradishDay=0,strict=False,inputluck=0.08):
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
            if SeedUtility.dishOfTheDay(seed,20,steps)[0] == 215:
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


        if count < 1:
            recipes = 1
        else:
            recipes = 2

        #if day > 46: #7 heart
        #    recipes = recipes + 1

        item = GetQuestItem(seed, day,recipes)

        if day == 30 and item in {254,256,264,262,260}:
            return

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
        f = open(filename,"at")
        f.write(str(seed)+" "+str(count) + '\n')
        f.close()

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



    #print(SeedUtility.getItemFromIndex(GetQuestItem(1946946589,20,2)))
    #for num in range(6):
    #    print(SeedUtility.getItemFromIndex(GetQuestItem(1165064550, 47,num)))

    #FindMarriageSeed()

    if True:

        
    
        
        seeds = [191133379,222164048,252430246,295907385,322022582,548659496,568322253,610124655,756748197,758980005,191133379,252430246,295907385,4864038,15242800,38670543,71231224,71624195,77152568,102636559,123100397,125211449,138193519,169269226,180146978,218577365,249362552,269478859,274441465,286350239,294040477,298776308,316615367,322548818,334400179,365109916,413749435,445895674,453773579,478332031,478622551,505869527,534937035,571864143,594832004,627849401,635051173,647908295,697170994,745489581,747140751,758206170,768690549,774681413,793146550,826659369,833748166,835399336,854094414,861657162,893256764,894390371,898296916,903717264,907269990,938859826,939540151,941753654,957484827,958851809,973963236]
        for seed in seeds:
            days = AnalyseSeed(seed,True,0,True,0.08)
            if days == None:
                continue
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
