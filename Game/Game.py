from Actions.directionMappings import directions
from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject
import numpy as np




class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension):
        self.dimension = dimension
        self.n_agents = n_agents
        self.n_initChrom = n_initChrom
        self.cave = gridSetup(dimension, n_pits, n_golds, n_wumpus)
        self.agents = []
        self.agents = self.initialize_agents()
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
                    self.statusString = f'Agent {self.agents[i].id} move {direction},  '
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
                    self.agents[i].fatigue -= 1

                elif action == 'pickup':
                    if self.agents[i].locatedAt in self.cave.goldCoordinate:
                        self.agents[i].gotGold = True
                        self.agents[i].wonGame = True
                        self.agents[i].fitness += 200
                        self.statusString += f'agent {i} found gold, '
                    self.agents[i].fatigue -= 1
                self.updateStatus(self.agents[i], self.cave, self.statusString, action)
            print("\n")
            self.removeDeadAgents()

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
        self.cave.updateAgentCoordinates(self.agents, False)

    def updateStatus(self, agent, grid, statusString, action):  # check if agent alive/dead and assign fitness scores
        loc = agent.locatedAt
        # print(f'location {loc} p {grid.pitCoordinates} s {grid.stenchCoord}')
        if loc[0] in grid.goldCoordinate:
            if agent.gotGold:
                print(f'agent {agent.id} won game, has fitness {agent.fitness}, exiting')
                agent.alive = False
            else:
                print(f'agent {agent.id} could find gold')
                agent.fitness += 20
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
                source = "agent" + str(agent.id)
                currentPerc = agent.perceive(self.cave)
                if len(currentPerc)>0:  # add marker if the same agent has no marker in this location
                    for d, phen in currentPerc:  # if this agent has not left
                        if not phen.phen == 'm' and not phen.source == source:
                            self.cave.grid.set_perception(self.cave.grid.perceptions, source, agent.locatedAt, "m",
                                                          lvl=1, t=0,
                                                          now=self.loopIter, dec=0.5)

                else:  # if no markers in this location, directly add safe marker
                    self.cave.grid.set_perception(self.cave.grid.perceptions, source, agent.locatedAt, "m", lvl=1, t=0,
                                                  now=self.loopIter, dec=0.5)
        # if not agent.arrow:
        #     actions_left = [action[1] for action in agent.chromList]
        #     valid_actions = ['F', 'B', 'L', 'R']
        #     if not listIntersection(actions_left, valid_actions):
        #         agent.alive = False
        #         statusString += f'agent killed due to no move actions in chromList, but also out of arrows, '
        facing = list(directions.keys())[list(directions.values()).index(agent.facing)]
        statusString += f'Agent {agent.id} located {agent.locatedAt}, facing {facing} fatigue {agent.fatigue}, fitness {agent.fitness}'
        print(statusString)

def listIntersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3