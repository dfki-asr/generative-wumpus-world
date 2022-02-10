from Actions.actionMappings import tab_of_act
from Actions.directionMappings import directions
from Game.Game import game
from random import sample, randrange, random, choice
from Agent.agentObjet import agentobject
import matplotlib.pyplot as plt
from statistics import mean

class ga_game:
    def __init__(self, n_generations, n_agents, crossover_rate, mutation_rate):
        self.gameRun = game(n_wumpus=1, n_golds=1, n_pits=9, n_agents=n_agents, n_initChrom=4, dimension=10)
        self.n_gens = n_generations
        self.crossover_rate = crossover_rate
        self.cross_count = 0
        self.mutation_rate = mutation_rate
        self.flip_max = 5 # max number of chromosome elements that get flipped
                          # during flip mutation

    def run(self):
        agent_population = self.gameRun.agents
        best_fitness = []
        avg_fitness = []
        # how many brand new chromosomes, vs take over from prev gen gives cross_count
        self.cross_count = int(len(agent_population) * self.crossover_rate)
        self.cross_count = self.cross_count if self.cross_count % 2 == 0 else self.cross_count + 1
        for i in range(self.n_gens):
            print(f'\nSTARTING NEW GENERATION {i}')
            # set agent list of gameobject
            self.gameRun.agents = agent_population
            self.printNewPopDetails()
            # reset graveyard
            # run game for this population
            self.gameRun.run_game()
            # get sorted graveyard and best chromList
            current_gen_sorted = self.gameRun.graveyard  # current population sorted by fitness (desc)
            # store the best fitness of current generation
            best_fitness.append(current_gen_sorted[0].fitness)
            # reproduce, select, crossover, mutate
            agent_population = self.reproduce(current_gen_sorted, i)
            fitnessList = []
            for i in range(len(agent_population)):
                fitnessList.append(current_gen_sorted[i].fitness)
            avg_fitness.append(mean(fitnessList))
            # this gets new population
            self.reset_game(agent_population)
        plt.plot(best_fitness, label="best fitness")
        plt.plot(avg_fitness, label="avg fitness")
        plt.xlabel('Generation number')
        plt.ylabel('Highest fitness')
        plt.legend(loc="upper right")
        plt.title('Fitness progression over generations')
        plt.show()

    def printNewPopDetails(self):
        for i in range(len(self.gameRun.agents)):
            loc = self.gameRun.agents[i].locatedAt
            facing = list(directions.keys())[list(directions.values()).index(self.gameRun.agents[i].facing)]
            print(f'agent {i} located at {loc}, facing {facing} with chromosomes {self.gameRun.agents[i].chromList}')
        print(self.gameRun.cave.grid)


    def reproduce(self, population, generation):
        mating_pool = self.selection(population)
        new_pop: list = self.crossover(mating_pool, generation)
        self.mutate(new_pop)
        for i in range(len(population) - self.cross_count):
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=population[i].chromList, phenomena=population[i].knownPhenomena, count=self.cross_count+i))
        return new_pop

    def selection(self, population):
        mating_pool = []
        for _ in range(0, self.cross_count, 2):
            mating_pool.append(population[0])
            mating_pool.append(population[1])
        return mating_pool

    def crossover(self, mating_pool, generation):
        new_pop = []
        # loop over for (cross_count/2) times, choosing two parents each time
        for i in range(0, self.cross_count, 2):
            indv1 = mating_pool[randrange(self.cross_count)]
            indv2 = mating_pool[randrange(self.cross_count)]
            chrom1, chrom2 = self.onepointcrossover(indv1.chromList, indv2.chromList)
            phenomena = list(set().union(indv1.knownPhenomena, indv2.knownPhenomena))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom1, phenomena=phenomena, count=i))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom2, phenomena=phenomena, count=i+1))
        return new_pop

    def mutate(self, population):
        for indiv in population:
            mutate = random() < self.mutation_rate

            if mutate:
                self.swapmutation(indiv)
                self.flipmutation(indiv)

    def flipmutation(self, indiv):
        numFlipped = randrange(self.flip_max) + 1
        size = len(indiv.chromList)
        for _ in range(numFlipped):
            index = randrange(size)
            (perc, react) = indiv.chromList[index]
            if (perc, react) != ('g','P') : # Agents should never forget that
                indiv.chromList[index] = ( indiv.chromList[index][0] , choice(list(tab_of_act)))

    def flip_binnedActions(self, indiv):
        numFlipped = randrange(self.flip_max)
        if numFlipped == 0: return

        for _ in range(numFlipped):
            rule = choice(indiv.chromList)
            flipIndex = randrange(len(rule[1]))
            flipTo = choice(list(tab_of_act.keys()))
            rule[1][flipIndex] = flipTo

    def swapmutation(self, indiv):
        n1, n2 = randrange(len(indiv.chromList)) , randrange(len(indiv.chromList))
        indiv.chromList[n1] , indiv.chromList[n2] = indiv.chromList[n2] , indiv.chromList[n1]

    def swap_binnedActions(self, indiv):
        for i, c in enumerate(indiv.chromList) :
            actions = c[1]
            l = len(actions)
            n1 = 0
            n2 = 0
            while n1 == n2:
                n1 = randrange(l)
                n2 = randrange(l)
            actions[n1], actions[n2] = actions[n2], actions[n1]


    def onepointcrossover(self, seq1:list, seq2:list):
        p_seq1 = randrange(len(seq1))

        seq12 = seq1[:p_seq1] + seq2[p_seq1:]
        seq21 = seq2[:p_seq1] + seq1[p_seq1:]

        return (seq12, seq21)


    def onepointcrossover_binned_actions(self, seq1:list, seq2:list):
        seq12 = []
        seq12.append(seq1[0])
        seq12.append(seq2[1])
        seq12.append(seq1[2])

        seq21 = []
        seq21.append(seq2[0])
        seq21.append(seq1[1])
        seq21.append(seq2[2])

        return (seq12, seq21)

    def reset_game(self, agents):
        self.gameRun.removeDeadAgents()
        self.gameRun.graveyard = []
        self.gameRun.cave.resetGrid(agents, True)
