from time import sleep

from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject


def perceive(agent, grid, agent_id):
    loc = agent.locatedAt
    perc = grid.grid.get_perc(loc)
    if len(perc) > 0:
        if perc not in agent.knownPhenomena:
            agent.knownPhenomena.append(perc)
            # print(f'At {loc}, there is a {perc} perception for agent {agent_id}')


def updateStatus(agent, grid, agent_id):
    loc = agent.locatedAt
    # print(f'location {loc} p {grid.pitCoordinates} s {grid.stenchCoord}')
    if loc[0] in grid.goldCoordinate:
        print(f'agent {agent_id} found gold')
        return 0
    elif loc[0] in grid.wumpusCoordinates or loc[0] in grid.pitCoordinates:
        print(f'agent {agent_id} located at {agent.locatedAt} has died')
        agent.alive = False
        print("------------------")


def removeDeadAgents(agents):
    dead_agents = []
    for i in range(len(agents)):
        if not agents[i].alive:
            dead_agents.append(agents[i])
        else:
            continue
    # print(dead_agents)
    for i in range(len(dead_agents)):
        agents.remove(dead_agents[i])


class game():
    def __init__(self, n_wumpus, n_golds, n_pits, n_agents, n_initChrom, dimension):
        agents = []
        grid = gridSetup(dimension, n_pits, n_golds, n_wumpus)
        for i in range(n_agents):
            temp = agentobject(n_initChrom, grid, dimension)
            agents.append(temp)
        grid.updateAgentCoordinates(grid.grid.grid, agents)
        for i in range(n_agents):
            loc = agents[i].locatedAt
            print(f'agent {i} located at {loc}')
            print(f'agent has chromosome {agents[i].chromList}')
        print(grid.grid)
        for a in range(10):
            for i in range(len(agents)):
                # print(f'agent {i} located at {agents[i].locatedAt}')
                perceive(agents[i], grid, i)
                #########  here we need to put in the "PERFORM ACTION" routine which chooses move/pickup/shoot
                agents[i].move(grid)
                #####################################
                updateStatus(agents[i], grid, i)
                # print(f'After move, agent {i} located at {agents[i].locatedAt}')
            print("\n\n\n")
            # print(f'agent length after removing dead guys {len(agents)}')
            grid.updateAgentCoordinates(grid.grid.grid, agents)
            removeDeadAgents(agents)
            print(grid.grid)
        for i,agent in enumerate(agents):
            print(f'agent {i} has known phenomena: {agent.knownPhenomena}')

