from math import floor as floor

class SearchTree(list):
    """  Binary search """

    def __init__(self, array=None):
        if array == None:
            self.array = []
        else:
            self.array = array


    def search(self, subject):
        rangeStart = 0
        rangeStop = len(self.array) - 1 
        while rangeStart <= rangeStop:

            node = int( floor( (rangeStart + rangeStop) /2 ) )
            
            if subject > self.array[node]:
                rangeStart = node + 1

            elif subject < self.array[node]:
                rangeStop = node - 1

            elif subject == self.array[node]:
                return self.array[node]

            else:
                return False


def findFile(subject):
    """ Finds the file that the proposed prime will be in"""
    if subject <= 15485863:
        return "primes1.json"
    elif subject <= 32452843:
        return "primes2.json"
    elif subject <= 49979687:
        return "primes3.json"
    elif subject <= 67867967:
        return "primes4.json"
    elif subject <= 86028121:
        return "primes5.json"
    elif subject <= 104395301:
        return "primes6.json"
    elif subject <= 122949823:
        return "primes7.json"
    elif subject <= 141650939:
        return "primes8.json"
    elif subject <= 160481183:
        return "primes9.json"
    elif subject <= 179424673:
        return "primes10.json"
    elif subject <= 198491317:
        return "primes11.json"
    elif subject <= 217645177:
        return "primes12.json"
    elif subject <= 236887691:
        return "primes13.json"
    elif subject <= 256203161:
        return "primes14.json"
    elif subject <= 275604541:
        return "primes15.json"
    elif subject <= 295075147:
        return "primes16.json"
    elif subject <= 314606869:
        return "primes17.json"
    elif subject <= 334214459:
        return "primes18.json"
    elif subject <= 353868013:
        return "primes19.json"
    elif subject <= 373587883:
        return "primes20.json"
    elif subject <= 393342739:
        return "primes21.json"
    elif subject <= 413158511:
        return "primes22.json"
    elif subject <= 433024223:
        return "primes23.json"
    elif subject <= 452930459:
        return "primes24.json"
    elif subject <= 472882027:
        return "primes25.json"
    elif subject <= 492876847:
        return "primes26.json"
    elif subject <= 512927357:
        return "primes27.json"
    elif subject <= 533000389:
        return "primes28.json"
    elif subject <= 553105243:
        return "primes29.json"
    elif subject <= 573259391:
        return "primes30.json"
    elif subject <= 593441843:
        return "primes31.json"
    elif subject <= 613651349:
        return "primes32.json"
    elif subject <= 633910099:
        return "primes33.json"
    elif subject <= 654188383:
        return "primes34.json"
    elif subject <= 674506081:
        return "primes35.json"
    elif subject <= 694847533:
        return "primes36.json"
    elif subject <= 715225739:
        return "primes37.json"
    elif subject <= 735632791:
        return "primes38.json"
    elif subject <= 756065159:
        return "primes39.json"
    elif subject <= 776531401:
        return "primes40.json"
    elif subject <= 797003413:
        return "primes41.json"
    elif subject <= 817504243:
        return "primes42.json"
    elif subject <= 838041641:
        return "primes43.json"
    elif subject <= 858599503:
        return "primes44.json"
    elif subject <= 879190747:
        return "primes45.json"
    elif subject <= 899809343:
        return "primes46.json"
    elif subject <= 920419813:
        return "primes47.json"
    elif subject <= 941083981:
        return "primes48.json"
    elif subject <= 961748927:
        return "primes49.json"
    else: 
        return "primes50.json"