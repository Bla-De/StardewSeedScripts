
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

def GetQuestItem(seed,daysPlayed):
    random = Cs(seed + daysPlayed)
    random.Sample() # Selecting person
    season = (daysPlayed-1) // 28 % 4
    if season != 3 and random.Sample() < 0.15:
        possibleCrops = GetPossibleCrops(season, daysPlayed % 28 <= 6)
        return possibleCrops[random.Next(len(possibleCrops))]
    return SeedUtility.randomItemFromSeason( seed, daysPlayed, 1000, False, True)

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
    for seed in range(54481,2147483648):
        if seed % 1000000 == 0:
            print("searching: "+str(seed))
        AnalyseSeed(seed)

def AnalyseSeed(seed,report=False):
    
    goodSpringItems = {16,18,20,22,24,190,192}
    goodSummerItems = {396,398,402}

    if not IsQuestItem(seed,20) or not IsRightRandomPerson(seed,20,("Robin","Lewis","Shane"),"Shane"):
        return
    item = GetQuestItem(seed,20)
    if report:
        print("20: " + SeedUtility.getItemFromIndex(item))
    if not item in goodSpringItems:
        return
    
    count = 1
    firstQuest = True
    dailyTrash = set()
    availableTrash = set()
    for day in range(1,29):
        if day in {13,20,24}:
            continue
        if not IsQuestItem(seed,day):
            continue
        if not firstQuest and not IsRightRandomPerson(seed,day,("Robin","Lewis","Shane"),"Shane"):
            continue
        item = GetQuestItem(seed, day)
        if report:
            print(str(day)+": "+SeedUtility.getItemFromIndex(item))

        checkedTrash = False
        if item not in goodSpringItems:
            dailyTrash.clear
            dailyTrash = TrashCans.checkAllTrash(seed,day,False,0.8)
            if item not in dailyTrash and item not in availableTrash:
                continue
            checkedTrash = True

        if day < 5 and item == 24:
            continue
        if day < 7 and item == 192:
            continue
        if day < 13 and item == 190:
            continue

        if not checkedTrash:
            dailyTrash.clear
            dailyTrash = TrashCans.checkAllTrash(seed,day)

        availableTrash = availableTrash.union(dailyTrash)
        firstQuest = False
        count = count + 1

        if report:
            print("Yes")
    if count < 7:
        return
    print(str(seed)+" "+str(count))

if __name__ == '__main__':
    #AnalyseSeed(45903449,True)
    #for day in range(50):
    #    print(str(day)+" "+str(IsQuestItem(20896,day)))
    #FindMarriageSeed()

    seeds = {49453}
    for seed in seeds:
        AnalyseSeed(seed,True)
