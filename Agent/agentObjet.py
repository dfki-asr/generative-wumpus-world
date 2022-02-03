from random import choice, randrange
from Actions.actionMappings import tab_of_act
from Environment.gridSetup import gridSetup
from Actions.directionMappings import directions, angles
import numpy as np


def isValidDirection(grid, position):
    if position[0] > grid.grid.dimensions - 1 or position[1] > grid.grid.dimensions - 1 or position[0] < 0 or \
            position[
                1] < 0:
        return False
    else:
        return True


class agentobject:
    def __init__(self, grid: gridSetup, chromosome = None, phenomena = None, count=0):
        self.grid = grid
        self.size_limit = 10
        self.fatigue = 40
        self.generation = 0
        self.fitness = 0
        self.rules = []
        self.knownPhenomena = phenomena if phenomena else ["g"]
        self.currentObservations = []
        self.chromList = chromosome if chromosome else self.initChromosome()
        self.wonGame = False
        self.alive = True
        self.arrow = True
        self.gotGold = False
        self.killedWumpus = False
        self.id = count
        self.initChromosome()
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = self.getRandomCoordinates(1, grid)
        self.facing =  choice(list(directions.values()))

        # print(f'AGENT FACING: {list(directions.keys())[list(directions.values()).index(self.facing)]}')

    def initParameters(self, count):
        self.size_limit = 10
        self.fatigue = 40
        self.fitness = 0
        self.wonGame = False
        self.alive = True
        self.arrow = True
        self.gotGold = False
        self.killedWumpus = False
        self.id = count
        self.initChromosome()
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = self.getRandomCoordinates(1, self.grid)

    def initChromosome(self):    # initialises the agent with random chromosomes of random length (between 3 and self.size_limit)
        chrom_list = []
        rand_size = randrange(3, self.size_limit)
        i = 0
        chrom_list.append(('g','P')) # digging for gold is the initial instinct of any agent
        while i < rand_size:
            item = choice(list(tab_of_act.keys()))
            key = choice(self.knownPhenomena)
            chrom_list.append((key, item))
            i += 1
        return chrom_list

    def getRandomCoordinates(self, num, grid):   # get "num" number of random coordinates which are unique for pits/wumpus/start
        i = 0
        temp_list = []
        while i < num:
            temp = randrange(grid.grid.dimensions), randrange(grid.grid.dimensions)
            if temp in grid.pitCoordinates or temp in grid.wumpusCoordinates or temp in grid.goldCoordinate or temp == (
                    0, 0):
                continue
            else:
                temp_list.append(temp)
                i += 1
        return temp_list

    def act(self, perception):        # choose a random action from chromosome list
        if len(perception) > 0:
            # print(f'there is a perception of {perception} in act method')
            perc_based_actions = [item for item in self.chromList if item[0] == perception]
            if len(perc_based_actions)>0:
                # print(f'corresponding chromosome for {perception} in {self.chromList}')
                obs, action = choice(perc_based_actions)
            else:
                random_actions = [item for item in self.chromList if item[0] == 'always']
                if len(random_actions) > 0:
                    obs, action = choice(random_actions)
                else:
                    obs, action = choice(self.chromList)
                # print(f'random actions are as follows {random_actions}')
        else:
            random_actions = [item for item in self.chromList if item[0] == 'always']
            if len(random_actions) > 0:
                obs, action = choice(random_actions)
            else:
                obs, action = choice(self.chromList)
        print(f'chosen action {tab_of_act[action]}')
        return tab_of_act[action]


    def random_move(self, grid):    # move randomly
        valid = False
        while not valid:
            dir = choice(list(directions))
            toPos = self.locatedAt[0][0] + directions[dir][0], self.locatedAt[0][1] + directions[dir][1]
            if toPos[0] > grid.grid.dimensions - 1 or toPos[1] > grid.grid.dimensions - 1 or toPos[0] < 0 or toPos[
                1] < 0:
                continue
            else:
                valid = True
        self.locatedAt.pop(0)
        self.locatedAt.append(toPos)

    def move(self, direction, grid):  # move in given "direction" on the "grid"
        angle = angles[direction]
        rotMat = rotationMatrix(angle)
        targDir = np.dot(self.facing, rotMat)
        newPos = tuple(self.locatedAt[0] + targDir)
        self.facing = tuple(targDir)
        self.fatigue -= 1
        if isValidDirection(grid, newPos):
            self.locatedAt.pop(0)
            self.locatedAt.append(newPos)
            self.fitness += 1

    def shootTargetCoord(self, grid, direction):  #  get the target coordinate where arrow will be shot
        angle = angles[direction]
        rotMat = rotationMatrix(angle)
        targDir = np.dot(self.facing, rotMat)
        newPos = tuple(self.locatedAt[0] + targDir)
        return newPos

def rotationMatrix(angle):
    a11 = np.cos(angle * (np.pi / 180))
    a12 = np.sin(angle * (np.pi / 180))
    return np.array([[a11, -a12], [a12, a11]]).astype(np.int)
