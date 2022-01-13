from random import choice, randrange

from Environment.gridSetup import gridSetup

class agentobject:

    def __init__(self, n_initChrom:int, grid:gridSetup, dimension:int):
        self.chromList = []
        self.tab_of_act = {
            'MN': ('move', 'N'),
            'MS': ('move', 'S'),
            'ME': ('move', 'E'),
            'MW': ('move', 'W'),
            'P': ('pickup'),
            'SN': ('shoot', 'N'),
            'SS': ('shoot', 'S'),
            'SE': ('shoot', 'E'),
            'SW': ('shoot', 'W')
        }
        self.initChromosome(n_initChrom)
        self.locatedAt = self.getRandomCoordinates(dimension, 1, grid)



    def initChromosome(self, n_initChrom:int):
        i=0
        while i<n_initChrom:
            if n_initChrom > len(self.tab_of_act):
                raise Exception(f'Initial number of chromosomes cannot be greater than total actions possible ({len(tab_of_act)+1})')
            item = choice(list(self.tab_of_act))
            if not ('always', item) in self.chromList:
                self.chromList.append(("always", item))
                i += 1
        return self.chromList

    def getRandomCoordinates(self, dimension, num, grid):
        i=0
        temp_list = []
        while i<num :
            temp = randrange(dimension), randrange(dimension)
            if (temp in grid.pitCoordinates  or temp in grid.wumpusCoordinates or temp in grid.goldCoordinate) and temp == (0,0):
                continue
            else:
                temp_list.append(temp)
                i+=1
        # print(temp_list)
        return temp_list




