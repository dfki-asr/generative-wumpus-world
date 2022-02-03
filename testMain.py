from Game.Game import game
from Environment.gridSetup import gridSetup
from Agent.agentObjet import agentobject
from Game.ga_game import ga_game

def main():
    game1 = ga_game(5, 5, 0.8, 0.3)
    game1.run()

if __name__ == '__main__':
    main()