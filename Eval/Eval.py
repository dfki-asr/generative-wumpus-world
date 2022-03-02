from Game.Game import game
from Agent.agentObjet import agentobject
from Environment.gridSetup import gridSetup
import matplotlib.pyplot as plt
from statistics import mean
class evaluate():
    def __init__(self, evolvedAgents):
        print("\n\n\n EVALUATION PHASE \n\n\n")
        finalRun = game(n_wumpus=1, n_golds=1, n_pits=3, n_agents=1, n_initChrom=4, dimension=10, agents=evolvedAgents)
        evolvedAgents = finalRun.agents.copy()

        randomAgents = []
        best_fitness_evolved = []
        best_fitness_random = []
        fitnessList_evolved = []
        fitnessList_random = []
        avg_fitness_evolved = []
        avg_fitness_random = []

        # create a batch of random agents
        for i in range(len(evolvedAgents)):
            randomAgents.append(agentobject(finalRun.cave, count='r'+str(i)))

        n=10            # n variations of environment
        for i in range(n):
            print(f"\nEnvironment {i}")
            if not i == 0:
                finalRun.cave = gridSetup(10, 3, 1, 1) # on the first run, random environment already created
                                                        # by the call to game()
            finalRun.agents.clear()
            # finalRun.agents = evolvedAgents
            for k in range(len(evolvedAgents)):
                finalRun.agents.append(evolvedAgents[k])
                finalRun.agents[k].initParameters(count=finalRun.agents[k].id)

            finalRun.run_game()
            best_fitness_evolved.append(finalRun.graveyard[0].fitness)
            for j in range(len(evolvedAgents)):
                fitnessList_evolved.append(finalRun.graveyard[j].fitness)
            avg_fitness_evolved.append(mean(fitnessList_evolved))
            fitnessList_evolved.clear()
            reset_game(finalRun)
            print(f"\n\n Evolved perf done {i}")
            #### Performance metrics
            finalRun.agents.clear()
            # finalRun.agents = randomAgents.copy()
            for j in range(len(randomAgents)):
                finalRun.agents.append(randomAgents[j])
                finalRun.agents[j].initParameters(count=finalRun.agents[j].id)
            finalRun.run_game()
            best_fitness_random.append(finalRun.graveyard[0].fitness)
            for k in range(len(evolvedAgents)):
                fitnessList_random.append(finalRun.graveyard[k].fitness)
            avg_fitness_random.append(mean(fitnessList_random))
            fitnessList_random.clear()
            print(f"\n\n Random perf done {i}")
            reset_game(finalRun)
        plt.plot(best_fitness_evolved, label="best fitness evolved")
        plt.plot(best_fitness_random, label="best fitness random")
        plt.plot(avg_fitness_evolved, linestyle='dashed',label="avg fitness evolved")
        plt.plot(avg_fitness_random, linestyle='dashed',label="avg fitness random")
        plt.xlabel('Environment number')
        plt.ylabel('Highest fitness')
        plt.legend(loc="upper right")
        plt.title('Fitness progression over environments')
        plt.show()
        # 1. run the entire evolved agents
        # 2. run random agents on the same grid
        # 3. Plot performance comparison
        # 4. For all evolved agents, reinitialize parameters
        # 5. Start from 1, but with brand new grid, repeat n times



        # finalRun = game(n_wumpus=1, n_golds=1, n_pits=3, n_agents=1, n_initChrom=4, dimension=10)
        # for i in range(len(evolvedAgents)):

def reset_game(gameObject):
    gameObject.removeDeadAgents()
    gameObject.graveyard = []
    gameObject.cave.resetGrid(gameObject.agents, True)


    def run(self):
        pass