import TravelingCart
import CSRandom
from ObjectInfo import ObjectInfo
import json

with open('ObjectInformation.json','r') as f:
    ObjectInfo = json.load(f)['content']
ObjectInfo = dict(zip(map(lambda x:int(x),ObjectInfo.keys()),map(lambda x: x.split('/'),ObjectInfo.values())))
for key in ObjectInfo.keys():
    ObjectInfo[key][1] = int(ObjectInfo[key][1])
ObjectInfo[174][0] = 'Large EggW'
ObjectInfo[182][0] = 'Large EggB'

objectsOffLimits = [79, 158, 159, 160, 161, 162, 163, 261, 277, 279,
                   305, 308, 326, 341, 413, 417, 437, 439, 447, 454, 
                   460, 645, 680, 681, 682, 688, 689, 690, 774, 775,
                   797, 798, 799, 800, 801, 802, 803, 807, 812]
validObjects = set()
for key,array in ObjectInfo.items():
    if '-' in array[3] and array[1] > 0 and '-13' not in array[3] and 'Quest' != array[3] \
        and 'Weeds' != array[0] and 'Minerals' not in array[3] and 'Arch' not in array[3]:
        if key < 790 and key not in objectsOffLimits:
            validObjects.add(key)

def determine():

    day = 49;
    items = [[766, 1000, 5], [264, 1000, 1], [591, 600, 1], [496, 500, 1], [78, 200, 1], [628, 4250, 1], [20, 240, 1], [444, 700, 1], [684, 300, 1], [629, 1500, 1]]

    for seed in range(250323847,263323847):

    #    if seed == 1265133:
    #        print("")
        if checkSeed(seed,day,items):
            print(seed)

def checkSeed(seed,day,items):
    random = CSRandom.CSRandomLite(seed + day)

    currentStock = dict()
    found = True;
    for i in range(len(items)):
        num = random.Next(2, 790)
        while True:
            num = (num+1) % 790;
            if num in validObjects:
                cost = max(random.Next(1,11)* 100, ObjectInfo[num][1]*random.Next(3,6))
                qty = 1 if not (random.Sample() < 0.1) else 5
                if num not in currentStock:
                    if num != items[i][0] or cost != items[i][1] or qty != items[i][2]:
                        found = False;
                    currentStock[num] = [cost,qty]
                    break
        if not found:
            break

    return found

if __name__ == '__main__':
    determine()
    print("");
