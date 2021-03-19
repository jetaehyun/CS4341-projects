# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!

from QLearner import QLearner
from QCharacter import QCharacter

from features1 import *

features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]
weights = [173.17464200348178, -1.8397384409939697, -28.549911042490006, -22.392729217308883, 0.050295801861828845]
qlearner = QLearner(weights, features)
# Create the game
 # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')

g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
))

# TODO Add your character
q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               False,
                               1)

g.add_character(q_character)


# Run!
g.go(1)
