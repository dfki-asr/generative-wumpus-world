from random import randrange
import numpy as np

class gridSetup():
    def __init__(self, dimension, n_pits=3, n_golds=1, n_wumpus=1):
        self.grid = np.empty((dimension, dimension), str)
        self.pitCoordinates = []
        self.wumpusCoordinates = []
        self.pitCoordinates = self.getRandomCoordinates(dimension, n_pits)
        self.wumpusCoordinates = self.getRandomCoordinates(dimension, n_wumpus)
        for _ in range(len(self.pitCoordinates)):
            self.grid[self.pitCoordinates[_]] = 'p'
        for _ in range(len(self.wumpusCoordinates)):
            self.grid[self.wumpusCoordinates[_]] = 'w'
        print(self.grid)

    def getRandomCoordinates(self, dimension, num):
        i=0
        temp_list = []
        while i<num :
            temp = randrange(dimension), randrange(dimension)
            if temp in self.pitCoordinates  or temp in self.wumpusCoordinates:
                continue
            else:
                temp_list.append(temp)
                i+=1
        print(temp_list)
        return temp_list
