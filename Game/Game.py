from time import sleep

from Actions.actionMappings import tab_of_act
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


def getTarget(locatedAt, direction):
    pass


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
            # print(f'agent has chromosome {agents[i].chromList}')
        print(grid.grid)
        for a in range(1):
            for i in range(len(agents)):
                # print(f'agent {i} located at {agents[i].locatedAt}')
                perceive(agents[i], grid, i)
                action, direction = agents[i].act()
                print(f'agent {i}: {action} in direction {direction}')

                if action == 'move':
                    agents[i].move(direction, grid)
                if action == 'shoot':
                    if agents[i].arrow:
                        agents[i].arrow = False
                        targCoord = agents[i].shootTargetCoord(grid, direction)
                        print(f'agent {i} shot from {agents[i].locatedAt} to {targCoord}')
                        if targCoord in grid.wumpusCoordinates:
                            agents[i].killedWumpus = True
                            print(f'agent {i} killed wumpus at {targCoord}')
                        else:
                            print(f'Arrow missed')
                if action == 'pickup':
                    if agents[i].locatedAt in grid.goldCoordinate:
                        agents[i].gotGold = True
                        print(f'agent {i} found gold')

                updateStatus(agents[i], grid, i)
                # print(f'After move, agent {i} located at {agents[i].locatedAt}')
            print("\n\n\n")
            # print(f'agent length after removing dead guys {len(agents)}')
            grid.updateAgentCoordinates(grid.grid.grid, agents)
            removeDeadAgents(agents)
            print(grid.grid)
        # for i,agent in enumerate(agents):
        #     print(f'agent {i} has known phenomena: {agent.knownPhenomena}')

