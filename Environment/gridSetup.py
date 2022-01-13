from random import randrange
from GridObject import Grid
class gridSetup():
    def __init__(self, dimension, n_pits: int, n_golds: int, n_wumpus:int):
        self.grid = Grid(dimension)
        self.pitCoordinates = []
        self.wumpusCoordinates = []
        self.stenchCoord = []
        self.breezeCoord = []
        self.glitterCoord = []
        self.goldCoordinate = []
        self.goldCoordinate = self.getRandomCoordinates(dimension, n_golds)
        self.pitCoordinates = self.getRandomCoordinates(dimension, n_pits)
        self.wumpusCoordinates = self.getRandomCoordinates(dimension, n_wumpus)
        self.grid.set_coord(self.wumpusCoordinates, 'W')
        self.grid.set_coord(self.pitCoordinates, 'P')
        self.grid.set_coord(self.goldCoordinate, 'G')
        self.breezeCoord = self.grid.neighboursOf(self.pitCoordinates)
        self.stenchCoord = self.grid.neighboursOf(self.wumpusCoordinates)
        self.glitterCoord = self.grid.neighboursOf(self.goldCoordinate)
        self.grid.set_coord(self.breezeCoord, 'b')
        self.grid.set_coord(self.stenchCoord, 's')
        self.grid.set_coord(self.glitterCoord, 'g')


    def getRandomCoordinates(self, dimension, num):
        i=0
        temp_list = []
        while i<num :
            temp = randrange(dimension), randrange(dimension)
            if (temp in self.pitCoordinates  or temp in self.wumpusCoordinates or temp in self.goldCoordinate) and temp == (0,0):
                continue
            else:
                temp_list.append(temp)
                i+=1
        # print(temp_list)
        return temp_list

    def updateAgentCoordinates(self, agents:list):
        for agent in agents:
            self.grid.set_coord(agent.locatedAt, 'A')