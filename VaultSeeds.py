from CSRandom import CSRandomLite
from ObjectInfo import ObjectInfo
from SeedUtility import giantCrop,nightEvent,fairyCropIndex

def findVaultGiantCropSeed():

    for seed in range(56680903,2147483648):
        #if seed % 1000000 == 0:
            #print(str(seed) + " - not yet found" )
        sum14 = giantCrop(seed,42,73,23)

        if not sum14:
            continue

        #sum26 = giantCrop(seed,54,73,22)
        #sum28 = giantCrop(seed,56,73,20)
        fall14 = giantCrop(seed,70,67,22)
        fall16 = giantCrop(seed,72,67,20)
        fall26 = giantCrop(seed,82,72,21)
        fall28 = giantCrop(seed,84,72,19)

        fall23 = giantCrop(seed,79,65,22)
        fall25 = giantCrop(seed,81,65,20)

        if fall14 and fall16 and fall26 and fall28 and fall23 and fall25:
             for day in range(30,40):
                 if nightEvent(seed,day) == "Fairy":
                     if checkForForageSpawns(seed):
                        print(str(seed) + " Fairy: " + str(day))
                        break

def checkForForageSpawns(seed,printOutput = False):
    import Location;
    busstop = Location.createBusstop("1.3")
    backwoods = Location.createBackwoods("1.3")
    town = Location.createTown("1.3")
    forest = Location.createForest("1.3")
    
    busstop.processDay(seed, 29 )
    if printOutput:
        print("busstop" + str(busstop.items))
    grape = False
    sweetPea = False
    spice = False
    for item in busstop.items.items():
        if item[1] == "Grape":
            grape = True
            if spice and sweetPea:
                break
            continue
        if item[1] == "Spice Berry":
            spice = True
            if grape and sweetPea:
                break
            continue
        if item[1] == "Sweet Pea":
            if grape and spice:
                break
            continue
    if not grape or not spice:
        return False

    town.processDay(seed,29)
    if printOutput:
        print("town" + str(town.items))
    for item in town.items.items():
        if item[1] == "Sweet Pea":
            sweetPea = True
            break
    if not sweetPea:
        return False

    busstop.processDay(seed, 57)
    if printOutput:
        print("busstop" + str(busstop.items))
    plum = False
    hazelnut = False
    for item in busstop.items.items():
        if item[1] == "Wild Plum":
            plum = True
            if hazelnut:
                break
            continue
        if item[1] == "Hazelnut":
            hazelnut = True
            if plum:
                break
            continue

    forest.processDay(seed, 57)
    if printOutput:
        print("forest" + str(forest.items))
    mushroom = False
    blackberry = False
    for item in forest.items.items():
        if item[1] == "Common Mushroom":
            mushroom = True
            if blackberry:
                break
            continue
        if item[1] == "Blackberry":
            blackberry = True
            if mushroom:
                break
            continue

    if not plum or not hazelnut or not mushroom:
        return False

    town.processDay(seed, 57)
    if printOutput:
        print("town" + str(town.items))
    for item in town.items.items():
        if item[1] == "Blackberry":
            blackberry = True
            break

    if not blackberry:
        return False

    busstop.processDay(seed, 90)
    if printOutput:
        print("busstop" + str(busstop.items))
    fruit = False
    crocus = False
    for item in busstop.items.items():
        if item[1] == "Crystal Fruit":
            fruit = True
            if crocus:
                break
            continue
        if item[1] == "Crocus":
            crocus = True
            if fruit:
                break
            continue

    if not fruit or not crocus:
        return False

    return True

def fairyCropNumbers(seed,days):
    rand = CSRandomLite(seed+days)
    for i in range(100):
        print(rand.Sample())

if __name__ == '__main__':
    findVaultGiantCropSeed();
    seeds = [50743290,
             51008526,
             55101356]
    seeds = []
    for seed in seeds:
        for day in range(30,40):
            if nightEvent(seed,day) == "Fairy":
                print(seed)
                print(day)
                fairyCropNumbers(seed,day)
       # checkForForageSpawns(seed,True)