from Game.ga_game import ga_game
import sys
import os
from datetime import datetime


def main(print_file):
    if print_file:
        cwd = os.getcwd()
        targetPath = os.path.join(cwd, "logs")
        while not os.path.exists(targetPath):
            os.mkdir(targetPath)
        timestr = datetime.now().strftime("%d%m%Y-%H%M%S")
        targetFile = os.path.join(targetPath, f'{timestr}.txt')
        orig_stdout = sys.stdout
        f = open(targetFile, 'w')
        sys.stdout = f

    game1 = ga_game(50,20, 0.8, 0.25)
    game1.run()

    if print_file:
        sys.stdout = orig_stdout
        f.close()


if __name__ == '__main__':
    main(print_file=False)