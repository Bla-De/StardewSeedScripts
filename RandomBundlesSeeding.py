import json
from CSRandom import CSRandomLite as CSRandom

with open('RandomBundles.json', 'r') as f:
    randomBundleData = json.load(f)

seasonalIds = {
    "Hazelnut": 408,
    "Snow Yam": 416,
    "Crocus": 418,
    "Holly": 283,
    "Eggplant": 272,
    "Pumpkin": 276,
    "Summer Spangle": 593,
    "Fairy Rose": 595,
    "Sunflower": 421,
    "Tiger Trout": 699,
    "Walleye": 140,
    "Red Snapper": 150,
    "Poppy": 376,
    "Beet": 284,
    "Amaranth": 300,
    "Starfruit": 268,
    "Red Cabbage": 266,
    "Melon": 254,
    "Blueberry": 258,
    "Hot Pepper": 260,
    "Tomato": 256,
    "Wheat": 262




    }


# duplicates of the Utility functions
def GetRandom(l, random):
    if l is None or len(l) == 0:
        return None
    return l[random.Next(len(l))]
def ParseItemList(items, pick, required, random):
    item_list = ParseRandomTags(items, random).split(',')
    if pick < 0:
        pick = len(item_list)
    if required < 0:
        required = pick
    while len(item_list) > pick:
        index_to_remove = random.Next(len(item_list))
        item_list.pop(index_to_remove)
    return item_list, required
def ParseRandomTags(data, random):
    open_index = 0
    while open_index != -1:
        open_index = data.rfind('[')
        if open_index != -1:
            close_index = data.find(']', open_index)
            if close_index == -1:
                return data
            #print(data, data[open_index+1:close_index])
            val = GetRandom(data[open_index+1:close_index].split('|'), random)
            data = data[:open_index] + val + data[close_index+1:]
            #print('\t',data)
    return data

def generate_random_bundles(seed, full=False):
    random = CSRandom(seed*9)
    bundleData = {}

    for area_data in randomBundleData:
        index_lookups = []
        selected_bundles = {}

        # create keys for bundles to fill into
        for index_string in area_data['Keys'].strip().split(' '):
            index_lookups.append(int(index_string))

        # load the set bundles into their keys
        bundle_set = GetRandom(area_data['BundleSets'], random)
        if bundle_set != None:
            for bundle_data in bundle_set['Bundles']:
                selected_bundles[bundle_data['Index']] = bundle_data

        # build the random pool
        random_bundle_pool = []
        for bundle_data in area_data['Bundles']:
            random_bundle_pool.append(bundle_data)
        for i in range(len(index_lookups)):
            if i not in selected_bundles:
                index_bundles = []
                for bundle_data in random_bundle_pool:
                    if bundle_data['Index'] == i:
                        index_bundles.append(bundle_data)

                if not index_bundles:
                    for bundle_data in random_bundle_pool:
                        if bundle_data['Index'] == -1:
                            index_bundles.append(bundle_data)
                if index_bundles:
                    selected_bundle = GetRandom(index_bundles, random)
                    random_bundle_pool.remove(selected_bundle)
                    selected_bundles[i] = selected_bundle
        for key,val in selected_bundles.items():
            color = val['Color'] if 'Color' in val else 'Green'
            items,req = ParseItemList(val['Items'], val['Pick'], val['RequiredItems'], random)
            if full:
                bundle_data = {
                    'Name': val['Name'], 
                    'Color': color, 
                    'Required': req, 
                    'Items': items, 
                    'Reward': val['Reward'],
                    'Sprite': val['Sprite'],
                    'Index': val['Index']
                }
            else:
                bundle_data = {
                    'Name': val['Name'], 
                    'Items': items, 
                }
            bundleData[area_data['AreaName'] + '/'  + str(index_lookups[key])] = bundle_data
    return bundleData

def getAllSeasonalRequiredItems(seed, fairyBundles=[],impossibleBundles=[]):
    bundleData = generate_random_bundles(seed)

    requiredItems = []
    fairyBundle = False
    for bundle in bundleData.values():
        if bundle["Name"] in impossibleBundles:
            return [-1],False;
        if bundle["Name"] in fairyBundles:
            fairyBundle = True
        for item in bundle["Items"]:
            itemName = item[item.index(" ",1)+1:]
            if itemName in seasonalIds:
                requiredItems.append(seasonalIds[itemName])

    return requiredItems,fairyBundle
    
if __name__ == '__main__':
    requiredItems,fairyBundle = getAllSeasonalRequiredItems(100595633)

    print(requiredItems)
    print(fairyBundle)