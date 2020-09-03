from CSRandom import CSRandomLite
import copy

def simulateHand(seed, day=0,timesPlayed = 0,report=False):
    
    rand,playerTotal,dealerTotal = setupHand(seed,day,timesPlayed,report )

    numberOfHits = analyseHand(copy.copy(rand),playerTotal,dealerTotal)
    return numberOfHits;

def setupHand(seed, day=0, timesPlayed = 0, report=False):
    rand = CSRandomLite(seed+day+timesPlayed);

    card1 = rand.Next(1,12);
    card2 = rand.Next(1,10);
    dealerTotal = card1 + card2;
    card3 = rand.Next(1,12);
    card4 = rand.Next(1,10);
    playerTotal = card3 + card4

    if report:
        print("Dealer cards:")
        print(card1)
        print(card2)
        print("Player cards:")
        print(card3)
        print(card4)
    return rand,playerTotal,dealerTotal;

def analyseHand(rand,playerTotal,dealerTotal):
    #Use copy of random
    if winOnStand(copy.copy(rand),playerTotal,dealerTotal):
        return 0;
    hits = 0;
    while playerTotal < 21:
        hits+=1;
        #Use actual random, as we need it advanced
        playerTotal += simulateHit(rand,playerTotal)

        if winOnStand(copy.copy(rand),playerTotal,dealerTotal):
            return hits;
    return -1;


def winOnStand(rand,playerTotal,dealerTotal,report=False):
    if playerTotal == 21:
        return True;

    while dealerTotal < 18 or dealerTotal < playerTotal and playerTotal <= 21:
        num3 = rand.Next(1, 10);
        num4 = 21 - dealerTotal;
        if (playerTotal == 20 and rand.Sample() < 0.5):
            num3 = num4 + rand.Next(1, 4);
        elif (playerTotal == 19 and rand.Sample() < 0.25):
            num3 = num4 + rand.Next(1, 4);
        elif (playerTotal == 18 and rand.Sample() < 0.1):
            num3 = num4 + rand.Next(1, 4);
        dealerTotal+= num3;
    
        if (dealerTotal > 21):
            return True
    return False;

def simulateHit(rand,playerTotal):
    num2 = rand.Next(1,10);
    num3 = num2 - playerTotal;
    if num3 > 1 and num3 < 6 and rand.Sample() < (1/num3):
        if rand.Sample() < 0.5:
            num2 = num3;
        else:
            num2 = num3 - 1;
    return num2;

def reportHand(hits,seed, day=0, timesPlayed = 0):
    print(seed+day+timesPlayed)
    rand,playerTotal,deaterTotal = setupHand(seed,day,timesPlayed,True)
    if hits == -1:
        print("bust")
        return
    for hit in range(hits):
        num = simulateHit(rand,playerTotal)
        print("Hit:")
        print(num)
        playerTotal+=hit

def analyseSeeds(seeds):
    bit = 0;
    count = 0;
    byteString = "";
    bin_array = bytearray()
    for seed in seeds:
        hits = simulateHand(seed);

        if hits == -1:
            bit = "X";
        else:
            bit = hits;

        print(hits)

def loadFile():
    file = open("F:\SDV\calicojack","rb")
    content = file.read()
    array = bytearray(content)
    byteString = "";
    for b in array:
        byteString+= int2base(b,2)
    print(byteString)
    
def int2base(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    if b<2 or b>len(alphabet):
        if b==64: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        else:
            raise AssertionError("int2base base out of range")
    if isinstance(x,complex): # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets

def searchForLuck(seed):
    for day in range(5,20):
        if not su.dishOfTheDay(seed,day,day-1) == 226:
                continue

        luck = su.dailyLuck(seed,day,day-1)
        if luck < 0.1:
            continue
        if not TrashCans.checkTrash(seed, day, 5,0,0,False,luck,"1.4") == 'DishOfTheDay':
            continue

        print(str(seed) + " " + str(day))

if __name__ == '__main__':
    seed = 274461447
    day = 31
    analyseSeeds(range(seed+day,seed+200+day))
    #loadFile()
    #for num in range(1,11):
    #    reportHand(simulateHand(256212373,5,num),256212373,5,num);