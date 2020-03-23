import SeedUtility as su
def findMine50Seed():
    import Location;
    backwoods = Location.createBackwoods()
    mountain = Location.createMountain()
    for seed in range(117216547,999999999):
        if su.dailyLuck(seed,5,4) > 0.099 and not su.doesSeedHaveMonsterFloorMines(seed,5,50):
            backwoods.processDay(seed,5)
            mountain.processDay(seed,5)

            leekCount = 0
            for item in backwoods.items.items():
                if item[1] == "Leek":
                    leekCount = leekCount + 1

            for item in mountain.items.items():
                if item[1] == "Leek":
                    leekCount = leekCount + 1

            if leekCount < 10:
                continue

            print(str(seed) + " Leeks: " + str(leekCount))

if __name__ == '__main__':
    findMine50Seed();