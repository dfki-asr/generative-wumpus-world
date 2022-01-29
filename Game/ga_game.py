from Game.Game import game
from random import sample, randrange, random
from Agent.agentObjet import agentobject


class ga_game:
    def __init__(self, n_generations, crossover_rate, mutation_rate):
        self.gameRun = game(n_wumpus=1, n_golds=1, n_pits=9, n_agents=5, n_initChrom=4, dimension=10)
        self.n_gens = n_generations
        self.crossover_rate = crossover_rate
        self.cross_count = 0
        self.mutation_rate = mutation_rate

    def run(self):
        agent_population = self.gameRun.agents
        # how many brand new chromosomes, vs take over from prev gen gives cross_count
        self.cross_count = int(len(agent_population) * self.crossover_rate)
        self.cross_count = self.cross_count if self.cross_count % 2 == 0 else self.cross_count + 1
        for i in range(self.n_gens):
            # set agent list of gameobject
            self.gameRun.agents = agent_population
            # reset graveyard
            # run game for this population
            self.gameRun.run_game()
            # get sorted graveyard and best chromList
            current_gen_sorted = self.gameRun.graveyard  # current population sorted by fitness (desc)
            # reproduce, select, crossover, mutate
            agent_population = self.reproduce(current_gen_sorted, i)
            # this gets new population
            self.reset_game(agent_population)

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
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom1))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom2))
        return new_pop

    def mutate(self, population):
        for indiv in population:
            mutate = random() < self.mutation_rate

            if mutate:
                # indiv.chromosome = indiv.randomChromosome()
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
        self.gameRun.graveyard = []
        self.gameRun.cave.updateAgentCoordinates(agents)
