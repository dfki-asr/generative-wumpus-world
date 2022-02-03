from Actions.directionMappings import directions
from Game.Game import game
from random import sample, randrange, random, choice
from Agent.agentObjet import agentobject
import matplotlib.pyplot as plt

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
            for i in range(len(agent_population)):
                agent_population[i].initParameters(i)
            # this gets new population
            self.reset_game(agent_population)
        plt.plot(best_fitness)
        plt.xlabel('Generation number')
        plt.ylabel('Highest fitness')
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
            new_pop.append(population[i])

        return new_pop

    def selection(self, population):
        num = 3
        mating_pool = []
        for _ in range(self.cross_count):
            rand_sel = sample(population, num)  # randomly take "num" samples from population list
            rand_sel.sort(key=lambda pop: pop.fitness, reverse=True)  # sort the random selection (desc)
            winner = rand_sel[0]  # choose rand sel with highest fitness as the winner
            mating_pool.append(winner)  # add it to mating pool
        return mating_pool

    def crossover(self, mating_pool, generation):
        new_pop = []
        # loop over for (cross_count/2) times, choosing two parents each time
        for _ in range(0, self.cross_count, 2):
            indv1 = mating_pool[randrange(self.cross_count)]
            indv2 = mating_pool[randrange(self.cross_count)]
            chrom1, chrom2 = self.onepointcrossover(indv1.chromList, indv2.chromList)
            phenomena = list(set().union(indv1.knownPhenomena, indv2.knownPhenomena))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom1, phenomena=phenomena))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom2, phenomena=phenomena))
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
                indiv.chromList[index] = ( choice(indiv.knownPhenomena) , indiv.chromList[index][1])


    def swapmutation(self, indiv):
        size = len(indiv.chromList)
        n1, n2 = randrange(size), randrange(size)
        indiv.chromList = indiv.chromList[:n1] + [indiv.chromList[n2]] + indiv.chromList[n1 + 1:n2] + [
        indiv.chromList[n1]] + indiv.chromList[n2 + 1:]

    def onepointcrossover(self, seq1:list, seq2:list):
        p_seq1 = randrange(len(seq1))
        p_seq2 = randrange(len(seq2))

        seq12 = seq1[:p_seq1] + seq2[p_seq2:]
        seq21 = seq2[:p_seq2] + seq1[p_seq1:]

        return (seq12, seq21)

    def reset_game(self, agents):
        self.gameRun.removeDeadAgents()
        self.gameRun.graveyard = []
        self.gameRun.cave.resetGrid(agents, True)
