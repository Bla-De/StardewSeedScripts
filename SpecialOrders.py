from CSRandom import CSRandom, MAX_INT

BASE_SPECIAL_ORDERS = ["Willy", "Pam", "Pierre", "Robin", "Emily", "Demetrius", "Demetrius2", "Gus", "Lewis", "Wizard", "Clint", "Linus",\
        "Evelyn", "Wizard2", "Robin2", "Gunther", "Caroline", "Willy2", "QiChallenge2", "QiChallenge3", "QiChallenge4", "QiChallenge5",\
        "QiChallenge6", "QiChallenge7", "QiChallenge8","QiChallenge9", "QiChallenge10", "QiChallenge12"]
SPECIAL_ORDERS_TITLES = { "Willy": "Juicy Bugs Wanted!", "Pam": "The Strong Stuff", "Pierre": "Pierre's Prime Produce", "Robin": "Robin's Project",\
        "Emily": "Rock Rejuvenation", "Demetrius": "Aquatic Overpopulation", "Demetrius2": "Biome Balance", "Gus": "Gus' Famous Omelet",\
        "Lewis": "Crop Order", "Wizard": "A Curious Substance", "Clint": "Cave Patrol", "Linus": "Community Cleanup", "Evelyn": "Gifts for George",\
        "Wizard2": "Prismatic Jelly", "Robin2": "Robin's Resource Rush", "Gunther": "Fragments of the past", "Caroline": "Island Ingredients",\
        "Willy2": "Tropical Fish", "QiChallenge2": "Qi's Crop", "QiChallenge3": "Let's Play A Game", "QiChallenge4": "Four Precious Stones",\
        "QiChallenge5": "Qi's Hungry Challenge", "QiChallenge6": "Qi's Cuisine", "QiChallenge7": "Qi's Kindness", "QiChallenge8": "Extended Family",\
        "QiChallenge9": "Danger In The Deep", "QiChallenge10": "Skull Cavern Invasion", "QiChallenge12": "Qi's Prismatic Grange"}

def handleSpecialOrder(specialOrder, season, newSeed):
    randomizedElementsSpecialOrders = {
        "Demetrius" : {"type": "season", "values": [
                ["Sunfish", "Sardine", "Flounder", "Largemouth Bass", "Halibut"],\
                ["Rainbow Trout", "Dorado", "Tilapia", "Tuna", "Red Mullet"],
                ["Tiger Trout", "Albacore", "Midnight Carp", "Salmon"],
                ["Squid", "Perch", "Lingcod"]
        ]},
        "Demetrius2": {"type":"simple", "values": ["river","ocean", "lake"]},
        "Lewis" : {"type": "season", "values": [
                ["Potato", "Green Bean", "Garlic", "Cauliflower"],\
                ["Tomato", "Blueberry", "Radish", "Melon", "Hot Pepper", "Wheat"],\
                ["Pumpkin", "Eggplant", "Cranberries", "Bok Choy", "Amaranth", "Grape", "Yam", "Artichoke"]
        ]},
        "Clint":  {"type":"simple", "values": ["Bat","Dust Spirit", "Skeleton", "Grub"]},
        "Robin2":  {"type":"pick", "values": ["Wood", "Stone"]},
        "Caroline":  {"type":"pick", "values": ["Pineapple", "Taro Root", "Ginger"]}
    } 
    if specialOrder in randomizedElementsSpecialOrders:
        rand2 = CSRandom(newSeed)
        randomizedElements = randomizedElementsSpecialOrders[specialOrder]
        if randomizedElements["type"] == "simple":
            res = randomizedElements["values"][rand2.Next(len(randomizedElements["values"]))]
        elif randomizedElements["type"] == "pick":
            rand2.Next()
            res = randomizedElements["values"][rand2.Next(len(randomizedElements["values"]))]
        else:
            rand2.Next()
            res = randomizedElements["values"][season][rand2.Next(len(randomizedElements["values"][season]))]
        return (specialOrder, res, newSeed)
    return (specialOrder, newSeed)

def checkSpecialOrdersWithRandom(seed, daysPlayed, currentAndcompletedSpecialOrders=None,gingerIsland=False, islandResort=False,sewingMachine=False,qiChallengeBoxInUse=False):
    if not currentAndcompletedSpecialOrders:
        currentAndcompletedSpecialOrders = set()
    season = int(daysPlayed / 28) % 4
    dayOfMonth = ((daysPlayed-1) % 28) + 1
    print(dayOfMonth, season)
    # We're ignoring the repeatable non-qi special orders since they're triggered only if the rest has been done.
    repeatableSpecialOrders = {"QiChallenge2", "QiChallenge3", "QiChallenge4", "QiChallenge5", "QiChallenge6", "QiChallenge7", "QiChallenge8",\
        "QiChallenge9", "QiChallenge10", "QiChallenge12"}
    monthLongSpecialOrders = {"Pierre", "Lewis", "Evelyn", "Caroline", "QiChallenge2", "QiChallenge4"}
    specialOrders = [specialOrder for specialOrder in BASE_SPECIAL_ORDERS 
        if (specialOrder not in (currentAndcompletedSpecialOrders - repeatableSpecialOrders) and
            (dayOfMonth <= 15 or specialOrder not in monthLongSpecialOrders) and
            (gingerIsland or specialOrder != "Caroline") and
            (islandResort or specialOrder != "Willy2") and
            (sewingMachine or specialOrder != "Emily") and
            (not qiChallengeBoxInUse or specialOrder not in ["QiChallenge12", "QiChallenge4"]) and
            (season == 0 or specialOrder not in ["Pam", "Evelyn"]) and 
            (season != 3 or specialOrder != "Lewis")
        )]
    validQiSpecialOrders = [specialOrder for specialOrder in specialOrders if specialOrder.startswith("QiChallenge")]
    validSpecialOrders = [specialOrder for specialOrder in specialOrders if specialOrder not in validQiSpecialOrders]
    if daysPlayed % 10 == 0: #if number*1.3 is an integer the triple casting makes c# round down
        rand = CSRandom(seed - 1 + int(daysPlayed  * 1.3))
    else:
        rand = CSRandom(seed + int(daysPlayed  * 1.3))
    result = []
    for validList in [validSpecialOrders, validQiSpecialOrders]:
        newSpecialOrder = validList[rand.Next(len(validList))]
        res = handleSpecialOrder(newSpecialOrder, season, rand.Next(minVal=0, maxVal=MAX_INT))
        result.append(res)
        validList.remove(newSpecialOrder)
        newSpecialOrder = validList[rand.Next(len(validList))]
        res = handleSpecialOrder(newSpecialOrder, season, rand.Next(minVal=0, maxVal=MAX_INT))
        result.append(res)
    return result

# def checkSpecialOrders(seed, daysPlayed, currentAndcompletedSpecialOrders=None,gingerIsland=False, islandResort=False,sewingMachine=False,qiChallengeBoxInUse=False):
#     if not currentAndcompletedSpecialOrders:
#         currentAndcompletedSpecialOrders = set()
#     season = int(daysPlayed / 28) % 4
#     dayOfMonth = ((daysPlayed-1) % 28) + 1
#     print(dayOfMonth, season)
#     repeatableSpecialOrders = {"QiChallenge2", "QiChallenge3", "QiChallenge4", "QiChallenge5", "QiChallenge6", "QiChallenge7", "QiChallenge8",\
#         "QiChallenge9", "QiChallenge10", "QiChallenge12"}
#     monthLongSpecialOrders = {"Pierre", "Lewis", "Evelyn", "Caroline", "QiChallenge2", "QiChallenge4"}
#     specialOrders = [specialOrder for specialOrder in BASE_SPECIAL_ORDERS 
#         if (specialOrder not in (currentAndcompletedSpecialOrders - repeatableSpecialOrders) and
#             (dayOfMonth <= 15 or specialOrder not in monthLongSpecialOrders) and
#             (gingerIsland or specialOrder != "Caroline") and
#             (islandResort or specialOrder != "Willy2") and
#             (sewingMachine or specialOrder != "Emily") and
#             (not qiChallengeBoxInUse or specialOrder not in ["QiChallenge12", "QiChallenge4"]) and
#             (season == 0 or specialOrder not in ["Pam", "Evelyn"]) and 
#             (season != 3 or specialOrder != "Lewis")
#         )]
#     validQiSpecialOrders = [specialOrder for specialOrder in specialOrders if specialOrder.startswith("QiChallenge")]
#     validSpecialOrders = [specialOrder for specialOrder in specialOrders if specialOrder not in validQiSpecialOrders]
#     if daysPlayed % 10 == 0: #if number*1.3 is an integer the triple casting makes c# round down
#         rand = CSRandom(seed - 1 + int(daysPlayed  * 1.3))
#     else:
#         rand = CSRandom(seed + int(daysPlayed  * 1.3))
#     result = []
#     for validList in [validSpecialOrders, validQiSpecialOrders]:
#         newSpecialOrder = rand.Next(len(validList))
#         result.append(validList[newSpecialOrder])
#         validList.remove(validList[newSpecialOrder])
#         rand.Next()
#         newSpecialOrder = rand.Next(len(validList))
#         result.append(validList[newSpecialOrder])
#         rand.Next()
#     return result

def findSeed(startingDay, dayLimit, targetMission, currentAndCompleted=None, maxDepth=2, gingerIsland=False, islandResort=False,sewingMachine=False,qiChallengeBoxInUse=False):
    def _rec_findSeed(_startingDay, path, depth):
        currentDay = _startingDay
        while currentDay <= dayLimit:
            baseOrders = checkSpecialOrders(seed, currentDay, set(path), gingerIsland, islandResort,sewingMachine,qiChallengeBoxInUse)
            if targetMission in baseOrders:
                return [{"seed" : seed, "day": currentDay, "order" : path}]
            if depth > 0:
                orders1 = _rec_findSeed(currentDay + 7, path + [baseOrders[0]], depth - 1)
                orders2 = _rec_findSeed(currentDay + 7, path + [baseOrders[1]], depth - 1)
                if not orders1 and not orders2: 
                    return
                resDepth = []
                if orders1:
                    resDepth += orders1
                if orders2:
                    resDepth += orders2
                return resDepth
            currentDay += 7
        return

    if dayLimit < startingDay:
        return
    if not currentAndCompleted:
        currentAndCompleted = []
    actualStartingDay = 7 * int(startingDay / 7) + 1
    seed = 0
    while 1:
        if seed % 10000 == 1:
            print(seed - 1)
        seed_res = _rec_findSeed(actualStartingDay, currentAndCompleted, maxDepth)
        if seed_res:
            print(seed_res)
        seed += 1

if __name__ == '__main__':
    # print(checkSpecialOrdersWithRandom(315083800, 1)) #Gus 282967189 Linus 909679364 3 5
    # print(checkSpecialOrdersWithRandom(315083800, 8)) #Pierre Gunther 4 5
    # print(checkSpecialOrdersWithRandom(315083800, 15)) #Wizard2 Robin 5 4
    # print(checkSpecialOrdersWithRandom(315083800, 22)) #Wizard Gus 7 6
    # print(checkSpecialOrdersWithRandom(315083800, 29)) #Demetrius Tilapia Wizard2 6 5
    # print(checkSpecialOrdersWithRandom(315083800, 36)) #Gunther Pierre 7 5
    # print(checkSpecialOrdersWithRandom(315083800, 43)) #Clint Dust Spirit 2096743366 Demetrius2 ocean 2039080209 7 5
    # print(checkSpecialOrdersWithRandom(315083800, 50)) #Gus 1325297572 Linus 1869399742 9 7 
    # print(checkSpecialOrdersWithRandom(315083800, 57)) #Wizard Linus 3 12
    # print(checkSpecialOrdersWithRandom(315083800, 64, {"Wizard"})) #Demetrius Albacore Gunther 4 12 
    # print(checkSpecialOrdersWithRandom(315083800, 71, {"Wizard", "Gunther"})) #Willy Demetrius Salmon 4 2
    # print(checkSpecialOrdersWithRandom(315083800, 78, {"Wizard", "Gunther", "Willy"})) #Linus Gus 6 3
    # print(checkSpecialOrdersWithRandom(315083800, 85, {"Wizard", "Gunther", "Willy", "Gus"})) # [('Demetrius2', 'ocean', 245663932), ('Wizard2', 1479362610), ('QiChallenge6', 920959261), ('QiChallenge2', 1432624261)]
    # print(checkSpecialOrdersWithRandom(315083800, 92, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"})) # [('Pierre', 1621701785), ('Robin', 1309682143), ('QiChallenge6', 631221326), ('QiChallenge3', 391437485)]
    print(checkSpecialOrdersWithRandom(315083800, 99, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"})) # Linus Demetrius2 7 3 ERROR ON SECOND
    # print(checkSpecialOrdersWithRandom(315083800, 106, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"})) # [('Clint', 'Skeleton', 78810197), ('Linus', 970321209), ('QiChallenge8', 51745456), ('QiChallenge5', 456547580)]
    # print(checkSpecialOrdersWithRandom(315083800, 113, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2", "Clint"})) # [('Pierre', 1454848050), ('Pam', 800640742), ('QiChallenge8', 1909491168), ('QiChallenge3', 1562844451)]
    # print(checkSpecialOrdersWithRandom(315083800, 120, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2", "Clint"})) # [('Robin2', 'Wood', 683402256), ('Robin', 630960275), ('QiChallenge9', 1619753233), ('QiChallenge4', 521657675)]
    # print(checkSpecialOrdersWithRandom(315083800, 127, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2", "Clint", "Robin2"})) # [('Pierre', 542068145), ('Demetrius', 'Largemouth Bass', 919645011), ('QiChallenge4', 1059212900), ('QiChallenge9', 557829950)]
    # print(checkSpecialOrdersWithRandom(315083800, 134, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2", "Clint", "Robin2", "Pierre"})) # [('Linus', 1918105998), ('Demetrius', 'Flounder', 749964544), ('QiChallenge6', 769474965), ('QiChallenge10', 1664126821)]
    print(checkSpecialOrdersWithRandom(315083800, 141, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))
    # print(checkSpecialOrdersWithRandom(315083800, 141, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))
    #print(checkSpecialOrdersWithRandom(315083800, 148, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))
    #print(checkSpecialOrdersWithRandom(315083800, 155, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))

def __testFindSeed():
    # print(findSeed(57, 57, "Caroline", gingerIsland=True))

    print(findSeed(57, 100, "Caroline", gingerIsland=True))


def __testCheckSpecialOrders():
    print(checkSpecialOrders(295358305, 57, None, gingerIsland=True))
    print(checkSpecialOrders(315083800, 57, {}))
    print(checkSpecialOrders(315083800, 64, {"Wizard"}))
    print(checkSpecialOrders(315083800, 71, {"Wizard", "Gunther"}))
    print(checkSpecialOrders(315083800, 78, {"Wizard", "Gunther", "Willy"}))
    print(checkSpecialOrders(315083800, 85, {"Wizard", "Gunther", "Willy", "Gus"}))
    print(checkSpecialOrders(315083800, 92, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"}))
    print(checkSpecialOrders(315083800, 99, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"}))
    print(checkSpecialOrders(315083800, 106, {"Wizard", "Gunther", "Willy", "Gus", "Wizard2"}))
    print(checkSpecialOrders(315083800, 148, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))
    print(checkSpecialOrders(315083800, 155, {"Wizard","Gunther","Willy","Gus","Wizard2","Clint","Robin2", "Pierre"}, gingerIsland=True))

    # print(checkSpecialOrders(295617936, 8))
    # print(checkSpecialOrders(290465963, 64))