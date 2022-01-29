from random import choice, randrange
from Actions import actionMappings
from Actions.actionMappings import tab_of_act
from Environment.gridSetup import gridSetup
from Actions.directionMappings import directions


def isValidDirection(grid, position):
    if position[0] > grid.grid.dimensions - 1 or position[1] > grid.grid.dimensions - 1 or position[0] < 0 or \
            position[
                1] < 0:
        return False
    else:
        return True


class agentobject:
    def __init__(self, grid: gridSetup, chromosome = None):
        self.size_limit = 10
        self.fatigue = 20
        self.generation = 0
        self.fitness = 0
        self.rules = []
        self.knownPhenomena = []
        self.currentObservations = []
        self.chromList = chromosome if chromosome else self.initChromosome()
        self.wonGame = False
        self.alive = True
        self.arrow = True
        self.gotGold = False
        self.killedWumpus = False
        self.initChromosome()
        self.action_generator = (act for act in self.chromList)
        self.locatedAt = self.getRandomCoordinates(1, grid)

    def initChromosome(self):    # initialises the agent with random chromosomes of random length (between 3 and self.size_limit)
        chrom_list = []
        rand_size = randrange(3, self.size_limit)
        i = 0
        while i < rand_size:
            item = choice(list(tab_of_act.keys()))
            chrom_list.append(("always", item))
            i += 1
        return chrom_list

    def addPhenomenaToChromosome(self, perception):     # adds newly discovered perception with a random action to chromList
        item = choice(list(tab_of_act.keys()))
        self.chromList.append((perception, item))
        print(f'new chromList {self.chromList}')

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
        # print(temp_list)
        return temp_list

    def act(self, ):        # choose a random action from chromosome list
        obs, act = choice(self.chromList)
        return tab_of_act[act]


    def random_move(self, grid):    # move randomly
        valid = False
        while not valid:
            dir = choice(list(directions))
            toPos = self.locatedAt[0][0] + directions[dir][0], self.locatedAt[0][1] + directions[dir][1]
            if toPos[0] > grid.grid.dimensions - 1 or toPos[1] > grid.grid.dimensions - 1 or toPos[0] < 0 or toPos[
                1] < 0:
                # print(f'continuing because toPos = {toPos}')
                continue
            else:
                valid = True
        self.locatedAt.pop(0)
        self.locatedAt.append(toPos)

    def move(self, direction, grid):    # move in given "direction" on the "grid"
        x, y = self.locatedAt[0]

        if direction == 'N':
            newPos = self.locatedAt[0][0] - 1, y

        elif direction == 'S':
            newPos = self.locatedAt[0][0] + 1, y

        elif direction == 'E':
            newPos = self.locatedAt[0][0], y + 1

        elif direction == 'W':
            newPos = self.locatedAt[0][0], y - 1

        self.fatigue -= 1

        if isValidDirection(grid, newPos):
            self.locatedAt.pop(0)
            self.locatedAt.append(newPos)
            self.fitness += 1


    def shootTargetCoord(self, grid, direction):  #  get the target coordinate where arrow will be shot
        x, y = self.locatedAt[0]

        if direction == 'N':
            targetPos = self.locatedAt[0][0] - 1, y

        elif direction == 'S':
            targetPos = self.locatedAt[0][0] + 1, y

        elif direction == 'E':
            targetPos = self.locatedAt[0][0], y + 1

        elif direction == 'W':
            targetPos = self.locatedAt[0][0], y - 1

        if isValidDirection(grid, targetPos):
            return targetPos

