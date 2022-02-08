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
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = self.getRandomCoordinates(grid)
        self.facing =  choice(list(directions.values()))


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
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = self.getRandomCoordinates(self.grid)

    def initChromosome(self):    # initialises the agent with random chromosomes of random length (between 3 and self.size_limit)
        chrom_list = []
        chrom_list.append(('g','P')) # digging for gold is the initial instinct of any agent
        for i in range(1, self.size_limit): # starting to count at 1 because first pair is digging for gold
            item = choice(list(tab_of_act.keys()))
            key = choice(self.knownPhenomena)
            chrom_list.append((key, item))
            i += 1
        return chrom_list

    def getRandomCoordinates(self, grid):
        temp = (0,0)
        while temp in grid.pitCoordinates or temp in grid.wumpusCoordinates or temp in grid.goldCoordinate or temp == (
                0, 0):
                temp = randrange(grid.grid.dimensions), randrange(grid.grid.dimensions)
        return [temp]


    def perceive(self, grid):   # check for perceptions and add to knownPhenomena if not already there
        loc = self.locatedAt
        perceptions = []
        perc = grid.grid.get_perc(loc)
        if len(perc) > 0 :
            perceptions.append((np.array([[1,0],[0,1]]),perc))
        neighbors = grid.grid.neighboursOf(loc)
        for n in neighbors:
            perc = grid.grid.get_perc([n])
            if len(perc) > 0:
                direction = self.getDirectionOfPerception(n)
                perceptions.append((direction, perc))
        return perceptions

    def getDirectionOfPerception(self, cell):
        if cell == self.locatedAt[0] :
            rotM = np.array([[1,0],[0,1]]) # identity matrix; no adaption needed if reacting to same cell
        else:
            from_to = np.subtract(cell, self.locatedAt[0])
            rotM = rotationMatrixByVec(self.facing, from_to)
        return rotM

    def act(self, perceptions):
        # print("PERCPTIONS :", perceptions)
        if len(perceptions) == 0:
            drct = np.array([[1,0],[0,1]])
            action = choice(['F','B','L','R'])
        else:
            drct, phen = choice(perceptions) ## random choice now :\ we have to decide for something better here
            # print("Reacting to phenomenon", phen, " in direction ", drct)
            perc_based_actions = [a for p,a in self.chromList if p == phen]
            action = choice(perc_based_actions) if len(perc_based_actions) > 0 else choice(['F','B','L','R'])
        return drct, tab_of_act[action]


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

def rotationMatrixByVec(a, b):
    a11 = a[0]*a[1] + b[0]*b[1]
    a12 = a[1]*b[0] - a[0]*b[1]
    a21 = a[0]*b[1] - a[1]*b[0]
    a22 = a11
    return np.array([[a11, a12], [a21, a22]]).astype(np.int)
