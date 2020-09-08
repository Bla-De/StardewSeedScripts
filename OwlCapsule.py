from CSRandom import CSRandomLite
import Location

def isEvent(seed):
    rand = CSRandomLite(seed)
    if rand.Sample() < 0.01:
        return 0
    if rand.Sample() < 0.01:
        return 0
    if rand.Sample() < 0.01:
        return 0
    if rand.Sample() < 0.01:
        return 1
    if rand.Sample() < 0.01:
        return 2
    return 0

def checkTiles(seed,farm):
    rand = CSRandomLite(seed)
    for index in range(50):
        x = rand.Next(5,60)
        y = rand.Next(5,60)
        coordinate = (x,y)
        if coordinate not in farm.back:
            return False

        if coordinate in farm.buildings:
            return False

        if coordinate in farm.notPassable:
            return False

        if coordinate in farm.noFurniture:
            return False

        if coordinate in farm.water:
            return False

        if coordinate in farm.terrainFeatures:
            return False

    return True

def findTileSeeds():
    farm = Location.createFarm()
    day = 2;
    for seed in range(0,2147483648,2):
        if isEvent(seed/2+day) != 2:
            continue
        
        if checkTiles(seed+day,farm):
            print(seed)
        if checkTiles(seed+day+1,farm):
            print(seed+1)


if __name__ == '__main__':
    findTileSeeds()

    seeds = []
    #farm = Location.createFarm()
    #checkTiles(seeds[0],farm)
