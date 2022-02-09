from random import choice, randrange
import random
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
        self.knownPhenomena = phenomena if phenomena else ["g", "b", "s"]
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
        random.seed(self.id)
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
            perceptions.append((self.facing,perc))
        neighbors = grid.grid.neighboursOf(loc)
        for n in neighbors:
            perc = grid.grid.get_perc([n])
            if len(perc) > 0:
                direction = tuple(np.subtract(n, self.locatedAt[0]))
                perceptions.append((direction, perc))
        return perceptions

    ## ((1,0),b), ((0,-1),b) <-- perceptions
    ## (g, P), (s, f), (b, F), (b, L) <-- chromList

    def act(self, perceptions): ## act prio by perc (one action per chromosome pair)
        perc_based_actions = []
        turn = self.facing
        if len(perceptions) == 0:
            action = choice(['F','B','L','R'])
        else:
            matches = []
            for p , a in self.chromList :
              matches = [(d, phen) for d, phen in perceptions if p == phen]
              if len(matches) > 0 :
                  turn, phen = choice(matches) ## random choice now :\ we have to decide for something better here
                  perc_based_actions = [a for p,a in self.chromList if p == phen]
                  break ## for first matching perception
        action = choice(perc_based_actions) if len(perc_based_actions) > 0 else choice(['F','B','L','R'])
        direction, action = tab_of_act[action]
        return turn, direction, action

    ## Another option to try with different chromosome model
    def act_prio_by_action(self, perceptions):
        if len(perceptions) == 0:
            turn = self.facing
            action = choice(['F','B','L','R'])
        else:
            turn, phen = choice(perceptions) ## random choice now :\ we have to decide for something better here
            # print("Reacting to phenomenon", phen, " in direction ", drct)
            perc_based_actions = [a for p, a in self.chromList if p == phen]  ## e.g. returns [('F','P')] for chrom element ('f', ('F','P'))
            action = perc_based_actions[0][0] ## should in example above return F as prioritized reaction and ignore the rest
        direction, action = tab_of_act[action]
        return turn, direction, action


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

