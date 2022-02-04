from Game.ga_game import ga_game
import sys
import os
from datetime import datetime


def main():
    cwd = os.getcwd()
    targetPath = os.path.join(cwd, "logs")
    while not os.path.exists(targetPath):
        os.mkdir(targetPath)
    timestr = datetime.now().strftime("%d%m%Y-%H%M%S")
    targetFile = os.path.join(targetPath, timestr)

    orig_stdout = sys.stdout
    f = open(targetFile, 'w')
    sys.stdout = f
    game1 = ga_game(10, 50, 0.9, 0.05)
    game1.run()
    sys.stdout = orig_stdout
    f.close()


if __name__ == '__main__':
    main()