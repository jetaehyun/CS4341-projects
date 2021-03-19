# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

from StateCharacter1 import StateCharacter1

# Create the game
g = Game.fromfile('map.txt')
features = [distanceToExit, distanceToBomb, inBombExplosionRange, anyDroppedBombs]

weights = [114.69554463857256, -2.861841880284248,  -6.044985197169929, 8.175889714036572]

qlearner = QLearner(weights, features)
prev_wrld = None
# TODO Add your character
state_character = StateCharacter1("me", # name
                                  "C",  # avatar
                                  0, 0,
)

#Uncomment this if you want the interactive character
g.add_character(state_character)

# Run!
g.go(1)
