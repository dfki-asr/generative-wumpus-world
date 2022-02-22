from random import randrange
from .GridObject import Grid
class gridSetup():
    def __init__(self, dimension, n_pits: int, n_golds: int, n_wumpus:int):
        self.grid = Grid(dimension)
        self.dimension = dimension
        self.pitCoordinates = []
        self.wumpusCoordinates = []
        self.stenchCoord = []
        self.breezeCoord = []
        self.glitterCoord = []
        self.goldCoordinate = []
        self.goldCoordinate = self.getRandomCoordinates(dimension, n_golds)
        self.pitCoordinates = self.getRandomCoordinates(dimension, n_pits)
        self.wumpusCoordinates = self.getRandomCoordinates(dimension, n_wumpus)
        self.grid.set_coord(self.grid.grid, self.wumpusCoordinates, 'W')
        self.grid.set_coord(self.grid.grid, self.pitCoordinates, 'P')
        self.grid.set_coord(self.grid.grid, self.goldCoordinate, 'G')
        self.breezeCoord = self.grid.neighboursOf(self.pitCoordinates)
        self.stenchCoord = self.grid.neighboursOf(self.wumpusCoordinates)
        self.glitterCoord = self.goldCoordinate
        self.grid.set_perception(self.grid.perceptions, "grid", self.breezeCoord, 'b', lvl=1, t=0,  dec=0)
        self.grid.set_perception(self.grid.perceptions, "grid", self.stenchCoord, 's', lvl=1, t=0, dec=0)
        self.grid.set_perception(self.grid.perceptions, "grid", self.glitterCoord, 'g', lvl=1, t=0,  dec=0)


    def getRandomCoordinates(self, dimension, num):
        i=0
        temp_list = []
        while i<num :
            temp = randrange(dimension), randrange(dimension)
            if temp in self.pitCoordinates  or temp in self.wumpusCoordinates or temp in self.goldCoordinate or temp == (0,0):
                continue
            else:
                if temp not in temp_list:
                    temp_list.append(temp)
                    i+=1
                else:
                    continue
        # print(temp_list)
        return temp_list

    def updateAgentCoordinates(self, agents:list, newGen):
        self.grid.remov_value_from_grid('A') # remove previous locations of agents from grid
        # print(f'previous coordinates are {old}')
        for agent in agents:
             if agent.alive:
                self.grid.set_coord(self.grid.grid, agent.locatedAt, 'A')  # populate new agent locations on grid

    def resetGrid(self, agent:list, newGen):
        self.grid = Grid(self.dimension)
        self.grid.set_coord(self.grid.grid, self.wumpusCoordinates, 'W')
        self.grid.set_coord(self.grid.grid,self.pitCoordinates, 'P')
        self.grid.set_coord(self.grid.grid, self.goldCoordinate, 'G')
        self.grid.set_perception(self.grid.perceptions, "grid", self.breezeCoord, 'b', lvl=1, t=0, dec=0)
        self.grid.set_perception(self.grid.perceptions, "grid", self.stenchCoord, 's', lvl=1, t=0,  dec=0)
        self.grid.set_perception(self.grid.perceptions, "grid", self.glitterCoord, 'g', lvl=1, t=0, dec=0)
        self.updateAgentCoordinates(agent, newGen)
