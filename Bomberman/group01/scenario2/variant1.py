# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

from QLearner import QLearner
from QCharacter import QCharacter
from features import *

# Create the game
g = Game.fromfile('map.txt')
features = [distanceToExit, distanceToBomb, inBombExplosionRange, anyDroppedBombs]

weights = [114.69554463857256, -2.861841880284248,  -6.044985197169929, 8.175889714036572]

qlearner = QLearner(weights, features)
prev_wrld = None
# TODO Add your character
q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
							   False,
                               1)

	#Uncomment this if you want the interactive character
g.add_character(q_character)

# Run!
g.go(1)
