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
    def __init__(self, grid: gridSetup, chromosome=None, phenomena=None, count=0):
        self.grid = grid
        self.size_limit = 10
        self.fatigue = 80
        self.generation = 0
        self.fitness = 0
        self.rules = []
        self.knownPhenomena = phenomena if phenomena else ["b", "s", "m", "g"]
        self.currentObservations = []
        self.chromList = chromosome if chromosome else self.initChromosome()  ## alternatively: self.initChromosome_binnedActionLists()
        self.wonGame = False
        self.alive = True
        self.arrow = True
        self.gotGold = False
        self.killedWumpus = False
        self.id = count
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = [(3,3)]#self.getRandomCoordinates(grid)
        x, y = self.locatedAt[0]
        self.grid.grid.heatmap[y][x] += 1
        self.facing = choice(list(directions.values()))

    def initChromosome(self):  # initialises the agent with random chromosomes of random length (between 3 and self.size_limit)
        chrom_list = []
        chrom_list.append(('g','F'))
        for i in range(1, self.size_limit):  # starting to count at 1 because first pair is digging for gold
            item = choice(list(tab_of_act.keys()))
            key = choice(self.knownPhenomena)
            chrom_list.append((key, item))
            i += 1
        return chrom_list

    def initChromosome_binnedActionLists(self):
        chrom_list = []
        actions = sorted(tab_of_act.keys())
        for p in self.knownPhenomena:
            chrom_list.append((p, random.sample(actions, self.size_limit)))
        return chrom_list

    def getRandomCoordinates(self, grid):
        temp = (0, 0)
        while temp in grid.pitCoordinates or temp in grid.wumpusCoordinates or temp in grid.goldCoordinate or temp == (
                0, 0):
            temp = randrange(grid.grid.dimensions), randrange(grid.grid.dimensions)
        return [temp]

    def perceive(self, grid):  # check for perceptions and add to knownPhenomena if not already there
        loc = self.locatedAt
        perceptions = []
        perc = grid.grid.get_perc(loc)
        if len(perc) > 0:
            for p in perc:
                perceptions.append((self.facing, p))
        neighbors = grid.grid.neighboursOf(loc)
        for n in neighbors:
            perc = grid.grid.get_perc([n])
            if len(perc) > 0:
                direction = tuple(np.subtract(n, self.locatedAt[0]))
                for p in perc:
                    perceptions.append((direction, p))
        return perceptions

    ## ((1,0),b), ((0,-1),b) <-- perceptions
    ## (g, P), (s, f), (b, F), (b, L) <-- chromList

    def act(self, perceptions):  ## act prio by perc (one action per chromosome pair)
        perc_based_actions = []
        turn = self.facing
        if len(perceptions) == 0:
            action = choice(['F', 'B', 'L', 'R'])
        elif bool([(d, phen) for d, phen in perceptions if phen == 'g' and d == (0, 0)]):
            self.gotGold = True
            self.wonGame = True
            self.fitness += 200
            self.alive = False
            print(f'agent {self.id} found gold, ')

        else:
            for p, a in self.chromList:
                matches = [(d, phen) for d, phen in perceptions if p == phen.phen and phen.source != self.id]
                if len(matches) > 0:
                    matches.sort(key=lambda x: x[1].lvl,
                                 reverse=True)  # sort matches by lvl of intensitymatches.sort(key=lambda x: x[1].lvl, reverse=True) # sort matches by lvl of intensity
                    # cycle through list items in matches and if rand(0,1) <= currentItem, choose this match and break
                    for match in matches:
                        if random.uniform(0, 1) <= match[1].lvl:
                            turn, phen = match
                            # if matches then proceed
                            perc_based_actions = [a for p, a in self.chromList if p == phen.phen]
                            break
                    if len(perc_based_actions) > 0: ## for first matching perception
                        break
        action = perc_based_actions[0] if len(perc_based_actions) > 0 else choice(['F', 'B', 'L', 'R'])
        direction, action = tab_of_act[action]
        return turn, direction, action

    ## Another option to try with different chromosome model
    def act_binnedActionList(self, perceptions):  ## use this one if using binned action lists chromosome model
        if len(perceptions) == 0:
            turn = self.facing
            action = choice(['F', 'B', 'L', 'R'])
        else:
            turn, phen = choice(perceptions)  ## random choice now :\ we have to decide for something better here
            # print("Reacting to phenomenon", phen, " in direction ", drct)
            perc_based_actions = [a for p, a in self.chromList if
                                  p == phen]  ## e.g. returns [('F','P')] for chrom element ('f', ('F','P'))
            action = perc_based_actions[0][0] if len(perc_based_actions) > 0 else choice(
                ['F', 'B', 'L', 'R'])  ## should in example above return F as prioritized reaction and ignore the rest
        direction, action = tab_of_act[action]
        return turn, direction, action

    def random_move(self, grid):  # move randomly
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

    def shootTargetCoord(self, grid, direction):  # get the target coordinate where arrow will be shot
        angle = angles[direction]
        rotMat = rotationMatrix(angle)
        targDir = np.dot(self.facing, rotMat)
        newPos = tuple(self.locatedAt[0] + targDir)
        return newPos


def rotationMatrix(angle):
    a11 = np.cos(angle * (np.pi / 180))
    a12 = np.sin(angle * (np.pi / 180))
    return np.array([[a11, -a12], [a12, a11]]).astype(np.int)
