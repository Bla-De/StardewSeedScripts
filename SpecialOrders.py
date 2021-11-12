from CSRandom import CSRandomLite

def checkSpecialOrders(seed, daysPlayed, currentAndcompletedSpecialOrders=None,gingerIsland=False, islandResort=False,sewingMachine=False,qiChallengeBoxInUse=False):
    if not currentAndcompletedSpecialOrders:
        currentAndcompletedSpecialOrders = set()
    season = int(daysPlayed / 28) % 4
    dayOfMonth = ((daysPlayed-1) % 28) + 1
    print("season", season, "dayOfMonth", dayOfMonth)
    repeatableSpecialOrders = {"QiChallenge2", "QiChallenge3", "QiChallenge4", "QiChallenge5", "QiChallenge6", "QiChallenge7", "QiChallenge8",\
        "QiChallenge9", "QiChallenge10", "QiChallenge12"}
    monthLongSpecialOrders = {"Pierre", "Lewis", "Evelyn", "Caroline", "QiChallenge2", "QiChallenge4"}
    baseSpecialOrders = ["Willy", "Pam", "Pierre", "Robin", "Emily", "Demetrius", "Demetrius2", "Gus", "Lewis", "Wizard", "Clint", "Linus",\
        "Evelyn", "Wizard2", "Robin2", "Gunther", "Caroline", "Willy2", "QiChallenge2", "QiChallenge3", "QiChallenge4", "QiChallenge5",\
        "QiChallenge6", "QiChallenge7", "QiChallenge8","QiChallenge9", "QiChallenge10", "QiChallenge12"]
    specialOrdersTitles = { "Willy": "Juicy Bugs Wanted!", "Pam": "The Strong Stuff", "Pierre": "Pierre's Prime Produce", "Robin": "Robin's Project",\
        "Emily": "Rock Rejuvenation", "Demetrius": "Aquatic Overpopulation", "Demetrius2": "Biome Balance", "Gus": "Gus' Famous Omelet",\
        "Lewis": "Crop Order", "Wizard": "A Curious Substance", "Clint": "Cave Patrol", "Linus": "Community Cleanup", "Evelyn": "Gifts for George",\
        "Wizard2": "Prismatic Jelly", "Robin2": "Robin's Resource Rush", "Gunther": "Fragments of the past", "Caroline": "Island Ingredients",\
        "Willy2": "Tropical Fish", "QiChallenge2": "Qi's Crop", "QiChallenge3": "Let's Play A Game", "QiChallenge4": "Four Precious Stones",\
        "QiChallenge5": "Qi's Hungry Challenge", "QiChallenge6": "Qi's Cuisine", "QiChallenge7": "Qi's Kindness", "QiChallenge8": "Extended Family",\
        "QiChallenge9": "Danger In The Deep", "QiChallenge10": "Skull Cavern Invasion", "QiChallenge12": "Qi's Prismatic Grange"}
    specialOrders = [specialOrder for specialOrder in baseSpecialOrders 
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
    rand = CSRandomLite(seed + int(daysPlayed  * 1.3))
    result = []
    for validList in [validSpecialOrders, validQiSpecialOrders]:
        newSpecialOrder = rand.Next(len(validList))
        result.append(validList[newSpecialOrder])
        validList.remove(validList[newSpecialOrder])
        rand.Next()
        newSpecialOrder = rand.Next(len(validList))
        result.append(validList[newSpecialOrder])
        rand.Next()
    return [f"{specialOrdersTitles[res]} ({res})" for res in result]


if __name__ == '__main__':
    

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