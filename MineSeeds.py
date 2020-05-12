import SeedUtility as su
import TrashCans
def findMine50Seed():
    import Location;
    backwoods = Location.createBackwoods()
    mountain = Location.createMountain()
    busstop = Location.createBusstop()
    #seeds = [10403262,13754340,25570430,25570472,35218188,40465024,57766188,58102146,68259952,82070350,84812874,84812876,98049168,115686278,130244860,131297220,132413232,140738670,150386318,159698094,162202406,163286626,163286698,175676880,180923750,182007970,188913146,189997390,204891996,217432956,220870788,226691734,233260920,257229186,259733536,266876812,274866242,277034684,277370624,283939828,287018314,287018316,295755912,303745350,303745352,317811860,318639990,325547646,326629332,330792014,351171634,361329492,365492130,380050702,380050790,388376138,393861166,412344316,412344340,415324968,420571828,462177108,465765748,466003824,470166534,479240194,485061170,488664542,494134766,502124164,503208370,512856042,520845452,523349808,554511114,554511178,554511180,561366536,577345370,577345374,578429504,594408300,598235046,604056036,608966982,637671954,660219954,664382658,676534746,685272308,688350866]
    for seed in range(101147684,999999999,2):
        #if seed % 1000000 == 0:
            #print("searching: " + str(seed))

        if not su.dishOfTheDay(seed,5,4) == 204:
            continue

        luck = su.dailyLuck(seed,5,4)
        if luck < 0.1:
           continue
        if not TrashCans.checkTrash(seed, 5, 5,0,0,False,luck,"1.4") == 'DishOfTheDay':
           continue

        if su.doesSeedHaveMonsterFloorMines(seed,5,50):
            continue

        if su.doesSeedHaveUnusualDarkFloor(seed,5,30):
            continue

        #busstop.processDay(seed,5)
       # mountain.processDay(seed,5)

        leekCount = 0
        for item in busstop.items.items():
            if item[1] == "Leek":
                leekCount = leekCount + 1

        for item in mountain.items.items():
            if item[1] == "Leek":
                leekCount = leekCount + 1

        if leekCount < 5:
            continue

        print(str(seed) + " Leeks: " + str(leekCount))

if __name__ == '__main__':
    findMine50Seed();