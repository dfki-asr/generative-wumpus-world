from Game.Game import game
from gridSetup import gridSetup
from Agent.agentObjet import agentobject


def main():
    game1 = game(n_wumpus=1, n_golds=1, n_pits=5, n_agents=10, n_initChrom=2, dimension=10)


if __name__ == '__main__':
    main()