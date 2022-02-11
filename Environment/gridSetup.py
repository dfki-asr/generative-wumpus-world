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
        self.grid.set_perception(self.grid.perceptions,self.breezeCoord, 'b')
        self.grid.set_perception(self.grid.perceptions, self.stenchCoord, 's')
        self.grid.set_perception(self.grid.perceptions, self.glitterCoord, 'g')


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
        old = self.grid.get_coord('A')
        # print(f'previous coordinates are {old}')
        if newGen:                     # if there no agents are in the grid, i.e at the beginning of the run
            for agent in agents:
                self.grid.set_coord(agent.locatedAt, 'A')       # put agents on the grid
        else:                                # after an iteration, where agents are populated at least once
            for i,agent in enumerate(agents):      # loop to remove all previous positions of indiv. agents
                val = self.grid.grid[old[i][0]][old[i][1]]
                # print(f'val at {old[i]} is {val}')
                while 'A' in val:           # to remove multiple agents which may be in the same position
                    if '+A' in val:
                        val = val.replace('+A', '')
                    elif 'A' in val:        # to romove agent when it is the only entity in that position
                        val = val.replace('A', '')
                self.grid.grid[old[i][0]][old[i][1]] = val  # previous contents of grid, after removing agents
            for agent in agents:
                 if agent.alive:
                    self.grid.set_coord(agent.locatedAt, 'A')  # populate new agent locations on grid

    def resetGrid(self, agent:list, newGen):
        self.grid = Grid(self.dimension)
        self.grid.set_coord(self.wumpusCoordinates, 'W')
        self.grid.set_coord(self.pitCoordinates, 'P')
        self.grid.set_coord(self.goldCoordinate, 'G')
        self.grid.set_perc(self.breezeCoord, 'b')
        self.grid.set_perc(self.stenchCoord, 's')
        self.grid.set_perc(self.glitterCoord, 'g')
        self.updateAgentCoordinates(agent, newGen)
