from Game.Game import game
from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject


def main():
    game1 = game(n_wumpus=1, n_golds=1, n_pits=9, n_agents=5, n_initChrom=4, dimension=10)
    game1.run_game()


if __name__ == '__main__':
    main()