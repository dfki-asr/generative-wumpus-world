import time

from Actions.actionMappings import tab_of_act
from Actions.directionMappings import directions
from Game.Game import game
from random import sample, randrange, random, choice
from Agent.agentObjet import agentobject
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mean
from Eval.Eval import evaluate

class ga_game:
    def __init__(self, n_agents, crossover_rate, mutation_rate):
        self.gameRun = game(n_wumpus=1, n_golds=1, n_pits=3, n_agents=n_agents, n_initChrom=4, dimension=10)
        # self.n_gens = n_generations
        self.crossover_rate = crossover_rate
        self.cross_count = 0
        self.mutation_rate = mutation_rate
        self.top_mates = 2
        self.flip_max = 2 # max number of chromosome elements that get flipped
                          # during flip mutation

    def run(self):
        agent_population = self.gameRun.agents
        best_fitness = []
        avg_fitness = []
        current_gen_sorted = []
        # how many brand new chromosomes, vs take over from prev gen gives cross_count
        self.cross_count = int(len(agent_population) * self.crossover_rate)
        self.cross_count = self.cross_count if self.cross_count % 2 == 0 else self.cross_count + 1
        i=0
        while True:
        # for i in range(self.n_gens):
            print(f'\nSTARTING NEW GENERATION {i}')
            # set agent list of gameobject
            self.gameRun.agents = agent_population
            self.printNewPopDetails(self.gameRun)
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
            for j in range(len(agent_population)):
                fitnessList.append(current_gen_sorted[j].fitness)
            avg_fitness.append(mean(fitnessList))
            # this gets new population

            ax = sns.heatmap(self.gameRun.cave.grid.heatmap, linewidth=0.5, annot=True, fmt="d", cmap="YlGnBu")
            gx, gy = self.gameRun.cave.goldCoordinate[0]
            orig = ax.texts[gy*10+gx].get_text()
            string = orig+'G'
            ax.texts[gy * 10 + gx].set_fontsize(20)
            ax.texts[gy*10+gx].set_text(string)
            for i in range(len(self.gameRun.cave.wumpusCoordinates)):
                wx, wy = self.gameRun.cave.wumpusCoordinates[i]
                orig = ax.texts[wy * 10 + wx].get_text()
                string = orig + 'W'
                ax.texts[wy * 10 + wx].set_fontsize(20)
                ax.texts[wy * 10 + wx].set_text(string)
            for i in range(len(self.gameRun.cave.pitCoordinates)):
                px, py = self.gameRun.cave.pitCoordinates[i]
                orig = ax.texts[py * 10 + px].get_text()
                string = orig + 'P'
                ax.texts[py * 10 + px].set_fontsize(20)
                ax.texts[py * 10 + px].set_text(string)
            i += 1
            print(f'Avg fitness is {avg_fitness[-1]}')
            plt.show()
            plt.close()
            self.reset_game(agent_population)

            if avg_fitness[-1]>140 or i>200:
                break
        plt.plot(best_fitness, label="best fitness")
        plt.plot(avg_fitness, label="avg fitness")
        plt.xlabel('Generation number')
        plt.ylabel('Highest fitness')
        plt.legend(loc="upper right")
        plt.title('Fitness progression over generations')
        plt.show()

        eval_run = evaluate(evolvedAgents=current_gen_sorted)


        # final_run = game(n_wumpus=1, n_golds=1, n_pits=3, n_agents=1, n_initChrom=4, dimension=10, agents=current_gen_sorted)
        # self.printNewPopDetails(final_run)
        # final_run.run_game()
        # final_gen_sorted:list = final_run.graveyard
        # j=0
        # final_avg = 0
        # for k in range(len(final_gen_sorted)):
        #     if final_gen_sorted[k].fitness>200:
        #         final_avg += final_gen_sorted[k].fitness
        #         j+=1
        # final_avg=final_avg/len(final_gen_sorted)
        # print(f'{j} agents won the game out of {len(final_gen_sorted)} with avg fitness of {final_avg}')



    def printNewPopDetails(self, game_object):
        for i in range(len(game_object.agents)):
            loc = game_object.agents[i].locatedAt
            facing = list(directions.keys())[list(directions.values()).index(game_object.agents[i].facing)]
            print(f'agent {game_object.agents[i].id} located at {loc}, facing {facing} with chromosomes {game_object.agents[i].chromList}')
        print(game_object.cave.grid)


    def reproduce(self, population, generation):
        mating_pool = self.selection(population)
        new_pop: list = self.crossover(mating_pool, generation)
        self.mutate(new_pop)
        for i in range(len(population) - self.cross_count):
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=population[i].chromList, phenomena=population[i].knownPhenomena, count=self.cross_count+i))
        return new_pop

    def selection(self, population):
        num = 5
        mating_pool = []

        for _ in range(self.cross_count):
            rand_sel = sample(population, num)
            rand_sel.sort(key=lambda pop: pop.fitness, reverse=True)
            winner = rand_sel[0]
            mating_pool.append(winner)
        return mating_pool

    def crossover(self, mating_pool, generation):
        new_pop = []
        # loop over for (cross_count/2) times, choosing two parents each time
        for i in range(0, self.cross_count, 2):
            while True:
                indv1 = mating_pool[randrange(self.cross_count)]
                indv2 = mating_pool[randrange(self.cross_count)]
                if indv1 != indv2 : break
            chrom1, chrom2 = self.onepointcrossover(indv1.chromList, indv2.chromList) ## use self.onepointcrossover_binned_actions for binned action chromosome model
            phenomena = list(set().union(indv1.knownPhenomena, indv2.knownPhenomena))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom1, phenomena=phenomena, count=i))
            new_pop.append(agentobject(grid=self.gameRun.cave, chromosome=chrom2, phenomena=phenomena, count=i+1))
        return new_pop

    def mutate(self, population):
        for indiv in population:
            mutate = random() < self.mutation_rate

            if mutate:
              self.swapmutation(indiv) ## use self.swap_binnedActions(indiv) for binned action list chromosome model
              self.flipmutation(indiv) ## use self.flip_binnedActions(indiv) fpr binned action list chromosome model

    def flipmutation(self, indiv):
        numFlipped = randrange(self.flip_max)
        size = len(indiv.chromList)
        for _ in range(numFlipped):
            index = randrange(size)
            (perc, react) = indiv.chromList[index]
            if (perc, react) != ('g','F') : # Agents should never forget that
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
        n1, n2 = randrange(1, len(indiv.chromList)) , randrange(1, len(indiv.chromList))
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
