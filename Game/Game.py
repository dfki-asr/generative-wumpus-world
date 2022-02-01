from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject
import numpy as np

def perceive(agent, grid, agent_id):   # check for perceptions and add to knownPhenomena if not already there
    loc = agent.locatedAt
    perc = grid.grid.get_perc(loc)
    if len(perc) > 0:
        if perc not in agent.knownPhenomena:
            agent.knownPhenomena = set().union(agent.knownPhenomena, perc.split("+"))
            print(f'At {loc}, there is a {perc} perception for agent {agent_id}')


def updateStatus(agent, grid, agent_id):  # check if agent alive/dead and assign fitness scores
    loc = agent.locatedAt
    # print(f'location {loc} p {grid.pitCoordinates} s {grid.stenchCoord}')
    if loc[0] in grid.goldCoordinate:
        if agent.gotGold:
            print(f'agent {agent_id} won game, has fitness {agent.fitness}, exiting')
            agent.alive = False
        else:
            print(f'agent {agent_id} could find gold')
            agent.fitness += 20
        return 0
    if agent.fatigue <= 0 :
        print(f'agent {agent_id} located at {agent.locatedAt} starved to death')
        agent.alive = False
        return
    elif loc[0] in grid.wumpusCoordinates :
        print(f'agent {agent_id} located at {agent.locatedAt} was eaten by Wumpus')
        agent.alive = False
        agent.fitness -= 10
        print("------------------")
        return
    elif loc[0] in grid.pitCoordinates :
        print(f'agent {agent_id} located at {agent.locatedAt} fell into a pit')
        agent.alive = False
        agent.fitness -= 10
        print("------------------")
        return

    if not agent.arrow:
        actions_left = [action[1] for action in agent.chromList]
        valid_actions = ['E', 'W', 'N', 'S']
        if not listIntersection(actions_left, valid_actions):
            agent.alive = False
            print(f'agent killed due to no move actions in chromList, but also out of arrows')

class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension):
        self.dimension = dimension
        self.n_agents = n_agents
        self.n_initChrom = n_initChrom
        self.cave = gridSetup(dimension, n_pits, n_golds, n_wumpus)
        self.agents = []
        self.agents = self.initialize_agents()
        self.cave.updateAgentCoordinates(self.agents, True)
        self.print_agent_init_chromList()
        self.graveyard = []
        self.bestIndividual = None

    def initialize_agents(self):    # init agents and add them to grid
        agents = []
        for i in range(self.n_agents):
            temp = agentobject(self.cave)
            agents.append(temp)
        return agents

    def print_agent_init_chromList(self):
        for i in range(self.n_agents):
            loc = self.agents[i].locatedAt
            print(f'agent {i} located at {loc} with chromosomes {self.agents[i].chromList}')
        print(self.cave.grid)

    def run_game(self):
        while(self.agents):
            for i in range(len(self.agents)):
                # print(f'agent {i} located at {agents[i].locatedAt}')
                action, direction = self.agents[i].act()
                perceive(self.agents[i], self.cave, i)
                print(f'agent {i}: {action} in direction {direction}')

                if action == 'move':
                    self.agents[i].move(direction, self.cave)
                    print(f'agent fatigue at {self.agents[i].fatigue}')
                if action == 'shoot':
                    if self.agents[i].arrow:
                        self.agents[i].arrow = False
                        targCoord = self.agents[i].shootTargetCoord(self.cave, direction)
                        print(f'agent {i} shot from {self.agents[i].locatedAt} to {targCoord}')
                        if targCoord in self.cave.wumpusCoordinates:
                            self.agents[i].killedWumpus = True
                            self.agents[i].fitness += 5
                            print(f'agent {i} killed wumpus at {targCoord}')
                        else:
                            print(f'Arrow missed')

                if action == 'pickup':
                    if self.agents[i].locatedAt in self.cave.goldCoordinate:
                        self.agents[i].gotGold = True
                        self.agents[i].wonGame = True
                        self.agents[i].fitness += 200
                        print(f'agent {i} found gold')
                updateStatus(self.agents[i], self.cave, i)
                # print(f'After move, agent {i} located at {self.agents[i].locatedAt}')
            print("\n")
            # print(f'agent length after removing dead guys {len(self.agents)}')
            self.removeDeadAgents()

            # print(self.cave.grid)
        # for i,agent in enumerate(self.agents):
        #     print(f'agent {i} has known phenomena: {agent.knownPhenomena}')
        for indiv in self.graveyard:
            print(f' overall: {indiv.fitness}, {indiv.chromList}')
        fitness_list = [indiv.fitness for indiv in self.graveyard]
        self.graveyard.sort(key=lambda element: element.fitness, reverse=True) # graveyard sorted (desc) by fitness
        self.bestIndividual = self.graveyard[0].chromList
        print(self.bestIndividual)


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

def listIntersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3