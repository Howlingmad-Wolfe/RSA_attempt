from math import floor as floor

class SearchTree(list):


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