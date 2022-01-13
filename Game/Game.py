
from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject

class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension):
        agents = []
        grid = gridSetup(dimension, n_wumpus, n_golds, n_pits)
        for i in range(n_agents):
            temp = agentobject(n_initChrom, grid, dimension)
            agents.append(temp)
        for agent in agents:
            print(agent.chromList)
            print(agent.locatedAt)
        grid.updateAgentCoordinates(agents)

        print(grid.grid)

