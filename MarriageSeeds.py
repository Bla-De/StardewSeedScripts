
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
    for seed in range(5817932,2147483648):
        if seed % 1000000 == 0:
            print("searching: "+str(seed))
        AnalyseSeed(seed,False,3)

def AnalyseSeed(seed,report=False,horseradishDay=0,strict=False):
    
    if report:
        print(seed)
    goodSpringItems = {16,18,20,22,24,190,192}
    goodSummerItems = {396,398,402}
    friendships = ["Robin","Lewis","Shane","Marnie"]

    if not report:
        if not IsQuestItem(seed,20) or not IsRightRandomPerson(seed,20,friendships,"Shane"):
            return
        if strict and not GetQuestItem(seed,7) == 24:
            return

    
    found = False
    possibleSteps = []
    possibleSteps2 = []
    steps = 0
    if strict:
        for steps in range(120):
            if SeedUtility.dishOfTheDay(seed,3,steps) == 215:
                possibleSteps.extend([steps])
                found = True

        if not found:
            return
        highestLuck = -999
        beststeps = 0
        for steps in possibleSteps:
            luck = SeedUtility.dailyLuck(seed,3,steps)
            if TrashCans.checkSpecificTrash(seed,3,5,False,luck) == 'DishOfTheDay':
                possibleSteps2.extend([steps])
                if luck > highestLuck:
                    beststeps = steps

        if possibleSteps2 == []:
            return
        steps = beststeps
        if report:
            print(possibleSteps2)
    if strict:
        for day in range(1,27):
            event = SeedUtility.nightEvent(seed,day)
            if event == "Meteor" or event == "Fairy" and day < 22:
                return


    
    count = 0
    firstQuest = False
    horseradishQuest = False
    dailyTrash = list()
    availableTrash = list()
    validDay = list()
    days = [6,8,10,16,20,22]
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

        luck = 0.08
        if count == 0 and not TrashCans.checkSpecificTrash(seed,day,5,False,luck) == 'DishOfTheDay':
            return


        if count < 3:
            recipes = 1
        else:
            recipes = 2
        item = GetQuestItem(seed, day,recipes)

        checkedTrash = False
        if strict:
            cans = [0,1,2,5,6]
        else:
            cans = [0,1,2,3,4,5,6,7]
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
    if count < 6:
        return
    horseradishFound = False
    for day in validDay:
        if day > 20:
            continue
        if horseradishDay == day or day > 6:
            tile = checkForGoodHorseradish(seed,day)
            if horseradishDay == day:
               if tile == None:
                    return
            else:
                if not tile == None or 16 in availableTrash:
                    horseradishFound = True

    if not report and horseradishFound:
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
    #AnalyseSeed(45903449,True)
    #for day in range(50):
    #    print(str(day)+" "+str(IsQuestItem(20896,day)))
    FindMarriageSeed()
    #checkQuests(611235816,range(1,29))
    if True:

        
    
        
        seeds=[3569713,4187296]
        for seed in seeds:
            days = AnalyseSeed(seed,True,3)
            #days = []
            for day in days:
                flag = False
                Cans = TrashCans.dayToYSD(day) + "\n"
                for i in range(8):
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
