from time import sleep

from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject

class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension):
        agents = []
        grid = gridSetup(dimension, n_pits, n_golds, n_wumpus)
        for i in range(n_agents):
            temp = agentobject(n_initChrom, grid, dimension)
            agents.append(temp)
        grid.updateAgentCoordinates(grid.grid.grid, agents)

        print(grid.grid)
        for a in range(10):
            for i in range(n_agents):
                # print(f'agent {i} located at {agents[i].locatedAt}')
                agents[i].move(grid)
                # print(f'After move, agent {i} located at {agents[i].locatedAt}')
            print("\n\n\n")
            grid.updateAgentCoordinates(grid.grid.grid, agents)
            print(grid.grid)

