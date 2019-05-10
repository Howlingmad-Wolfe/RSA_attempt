from math import floor as floor

class SearchTree(list):


    def __init__(self, array=None):
        if array == None:
            self.array = []
        else:
            self.array = array


    def search_2(self, subject, node=None, searchDepth=None):
        if searchDepth == None:
            searchDepth = 1
            node = int(floor( len(self.array) / pow(2, searchDepth) ) )
            print node, " root node\n"
        else:
            searchDepth += 1

        block = float( len(self.array) / pow( 2, searchDepth ) )
        print block, " float block\n"

        if len(self.array) / pow( 2, searchDepth ) < 1.0:
            return False

        elif subject > self.array[node]:
            node = node + int(floor(block))
            print node, " next node\n"
            return self.search(subject, node, searchDepth)

        elif subject < self.array[node]:
            node = node - int(floor( block ))
            print node, " next node\n"
            return self.search(subject, node, searchDepth)

        elif subject == self.array[node]:
            return True

        else:
            return False


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

test = SearchTree()

for i in range(0,2000, 3):
    test.array.append(i)

print test.array
print ""

#print test.search(1)

newtest = []

for i in range(0, 2000):
    if test.search(i):
        newtest.append(i)
    elif test.search(i) == 0:
        newtest.append(i)

print newtest

#print test.search(0)