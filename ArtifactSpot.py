import Utility
from CSRandom import CSRandomLite

archDict = {'Town': [(100, .04), (103, .01), (105, .01), (106, .008), (110, .05), (119, .005), (123, .005), (126, .001), (127, .001), (579, .01)], 'Mountain': [(101, .02), (103, .04), (105, .02), (107, .008), (109, .008), (112, .05), (114, .01), (115, .03), (119, .01), (120, .05), (126, .001), (127, .001), (581, .01), (587, .01), (589, .03)], 'Forest': [(101, .02), (103, .03), (104, .01), (105, .02), (106, .01), (109, .01), (114, .01), (115, .03), (119, .01), (120, .05), (123, .01), (126, .001), (127, .001), (580, .01), (587, .01), (588, .01), (589, .03)], 'BusStop': [(101, .02), (103, .03), (115, .04), (120, .05), (123, .01), (126, .001), (127, .001), (584, .01)], 'Beach': [(106, .02), (116, .1), (117, .05), (118, .1), (126, .001), (127, .001), (582, .01), (586, .03), (588, .01), (589, .03)], 'Mine': [(107, .01)], 'UndergroundMine': [(108, .01), (119, .02), (121, .01), (122, .001), (123, .02), (126, .001), (127, .001), (585, .01)], 'Farm': [(111, .1), (113, .1), (126, .001), (127, .001), (583, .01)], 'Desert': [(124, .04), (125, .08), (588, .1)]}
locationDict = {
"Farm": [(382, .05), (770, .1), (390, .25), (330, 1)],
"UndergroundMine": [(107, .01)],
"Desert": [(390, .25), (330, 1)],
"BusStop": [(584, .08), (378, .15), (102, .15), (390, .25), (330, 1)],
"Forest": [(378, .08), (579, .1), (588, .1), (102, .15), (390, .25), (330, 1)],
"Town": [(378, .2), (110, .2), (583, .1), (102, .2), (390, .25), (330, 1)],
"Mountain": [(382, .06), (581, .1), (378, .1), (102, .15), (390, .25), (330, 1)],
"Backwoods": [(382, .06), (582, .1), (378, .1), (102, .15), (390, .25), (330, 1)],
"Railroad": [(580, .1), (378, .15), (102, .19), (390, .25), (330, 1)],
"Beach": [(384, .08), (589, .09), (102, .15), (390, .25), (330, 1)],
"Woods": [(390, .25), (330, 1)],
"IslandNorth": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandSouth": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandWest": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandSouthEast": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandSouthEastCave": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandSecret": [(791, .05), (292, .05), (774, .1), (749, 1)],
"IslandNorthCave1": [(107, .01)]
}

def artifactSpot(seed,day,x,y,location):
    #GameLocation::digUpArtifactSpot
    r = CSRandomLite(x*2000+y+seed/2 + day)

    toDigUp = -1
    locationList = archDict[location]
    for entry in locationList:
        if r.Sample() < entry[1]:
            toDigUp = entry[0]
            break

    if r.Sample() < 0.2 and location != "Farm":
        toDigUp = 102

    if toDigUp != -1:
        return toDigUp

    season = Utility._dayToSeason(day)
    if season == "Winter":
        if r.Sample() < 0.5 and location != "Desert":
            if r.Sample() < 0.4:
                return 416
            return 412
    if season == "Spring":
        if r.Sample() < 0.0625 and location != "Desert" and location != "Beach":
            return 273

    locationList = locationDict[location]

    for entry in locationList:
        if r.Sample() < entry[1]:
            return entry[0]

if __name__ == '__main__':
    from ObjectInfo import ObjectInfo
    for x in range(10):
        for y in range(10):
            item = artifactSpot(0,1,x,y,"Mountain")
            string = ObjectInfo[item].split('/')[0]
            print(f"({x}, {y}): {string}")