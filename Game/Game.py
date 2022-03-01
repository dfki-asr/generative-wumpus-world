from Actions.directionMappings import directions
from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject
from itertools import chain




class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension, agents=None):
        self.dimension = dimension
        self.n_agents = n_agents
        self.n_initChrom = n_initChrom
        self.cave = gridSetup(dimension, n_pits, n_golds, n_wumpus)
        self.agents = []
        if not agents:
            self.agents = self.initialize_agents()
        else:
            for i in range(len(agents)):
                self.agents.append(agentobject(self.cave, chromosome=agents[i].chromList, phenomena=agents[i].knownPhenomena, count='f'+str(i)))
        self.cave.updateAgentCoordinates(self.agents, True)
        # self.print_agent_init_chromList()
        self.graveyard = []
        self.bestIndividual = None
        self.statusString = ""
        self.loopIter = 0

    def initialize_agents(self):    # init agents and add them to grid
        agents = []
        for i in range(self.n_agents):
            temp = agentobject(self.cave, count=i)
            agents.append(temp)
        return agents

    def print_agent_init_chromList(self):
        for i in range(self.n_agents):
            loc = self.agents[i].locatedAt
            print(f'agent {i} located at {loc} with chromosomes {self.agents[i].chromList}')
        print(self.cave.grid)

    def run_game(self):
        while(self.agents):
            self.loopIter += 1
            for i in range(len(self.agents)):
                self.statusString = ""
                # print(f'agent {i} located at {agents[i].locatedAt}')
                perc = self.agents[i].perceive(self.cave)
                turnFirst, action, direction = self.agents[i].act(perc)
                self.statusString += ""

                self.agents[i].facing = turnFirst
                if action == 'move':
                    self.agents[i].move(direction, self.cave)
                    self.statusString += f'Agent {self.agents[i].id} move {direction},  '
                    x, y = self.agents[i].locatedAt[0]
                    self.cave.grid.heatmap[y][x] += 1
                elif action == 'shoot':
                    if self.agents[i].arrow:
                        self.agents[i].arrow = False
                        targCoord = self.agents[i].shootTargetCoord(self.cave, direction)
                        self.statusString += f'agent {self.agents[i].id} shot from {self.agents[i].locatedAt} to {targCoord}, '
                        if targCoord in self.cave.wumpusCoordinates:
                            self.agents[i].killedWumpus = True
                            self.agents[i].fitness += 5
                            self.statusString += f'agent {self.agents[i].id} killed wumpus at {targCoord}, '
                        else:
                            self.statusString +=f'Arrow missed, '
                    else:
                        self.statusString += f'Agent {self.agents[i].id} shot, but no arrows, '
                    self.agents[i].fatigue -= 1

                self.updateStatus(self.agents[i], self.cave, self.statusString, action)
            print("\n")
            self.evolvePerceptions()
            self.removeDeadAgents()
            self.cave.updateAgentCoordinates(self.agents, False)
        for indiv in self.graveyard:
            print(f' overall: {indiv.fitness}, {indiv.chromList}')
        fitness_list = [indiv.fitness for indiv in self.graveyard]
        self.graveyard.sort(key=lambda element: element.fitness, reverse=True) # graveyard sorted (desc) by fitness
        self.bestIndividual = self.graveyard[0].chromList
        print(f'The best individual\'s chromosome is {self.bestIndividual}')


    def removeDeadAgents(self):
        dead_agents = []
        for i in range(len(self.agents)):
            if not self.agents[i].alive:
                dead_agents.append(self.agents[i])
            else:
                continue
        # print(dead_agents)
        for i in range(len(dead_agents)):
            self.graveyard.append(dead_agents[i])
            self.agents.remove(dead_agents[i])

    def evolvePerceptions(self):
        flat_perceptions = list(chain.from_iterable(self.cave.grid.perceptions))
        val_perc = [item for item in flat_perceptions if len(item)>0]
        to_be_removed = []
        for item in val_perc:
            for i in range(len(item)):
                item[i].setLevel(self.loopIter)
                if item[i].lvl <= 0:
                    to_be_removed.append(item[i])
            self.removePerception(to_be_removed)

    def updateStatus(self, agent, grid, statusString, action):  # check if agent alive/dead and assign fitness scores
        loc = agent.locatedAt
        # print(f'location {loc} p {grid.pitCoordinates} s {grid.stenchCoord}')
        if loc[0] in grid.goldCoordinate:
            if agent.alive:
                agent.fitness += 200
                print(f'agent {agent.id} won game, has fitness {agent.fitness}, exiting')
                agent.alive = False
            # else:
            #     print(f'agent {agent.id} could find gold')
            #     agent.fitness += 20
            if agent.fatigue <= 0:
                agent.alive = False

        if agent.fatigue <= 0:
            statusString += f'agent {agent.id} located at {agent.locatedAt} starved to death, '
            agent.alive = False

        elif loc[0] in grid.wumpusCoordinates:
            print(f'agent {agent.id} located at {agent.locatedAt} was eaten by Wumpus')
            agent.alive = False
            agent.fitness -= 10
            print("------------------")
            return
        elif loc[0] in grid.pitCoordinates:
            print(f'agent {agent.id} located at {agent.locatedAt} fell into a pit')
            agent.alive = False
            agent.fitness -= 10
            print("------------------")
            return

        if action == 'move':  # if agent moves
            if agent.alive:     # and remains alive after move
                currentPerc = self.cave.grid.get_perc(agent.locatedAt)
                level = 0.1
                if(len(currentPerc) > 0):
                    existingLevel = [p.lvl for p in currentPerc if p.source == agent.id]
                    if len(existingLevel)>0:
                        level = level+existingLevel[0]
                        level = min(level, 1)

                self.cave.grid.set_perception(self.cave.grid.perceptions, agent.id, agent.locatedAt, "m", lvl=level, t=self.loopIter,
                                                  dec=0.5)
        # if not agent.arrow:
        #     actions_left = [action[1] for action in agent.chromList]
        #     valid_actions = ['F', 'B', 'L', 'R']
        #     if not listIntersection(actions_left, valid_actions):
        #         agent.alive = False
        #         statusString += f'agent killed due to no move actions in chromList, but also out of arrows, '
        facing = list(directions.keys())[list(directions.values()).index(agent.facing)]
        statusString += f'Agent {agent.id} located {agent.locatedAt}, facing {facing} fatigue {agent.fatigue}, fitness {agent.fitness}'
        print(statusString)

    def removePerception(self, items):
        for i,row in enumerate(self.cave.grid.perceptions):
            for j, element in enumerate(row):
                for item in items:
                    if item in element:
                        self.cave.grid.perceptions[i][j].remove(item)

def listIntersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3