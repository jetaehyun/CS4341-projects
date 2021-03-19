# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features1 import *

features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]

weights = [177.2277174308819, -0.7130756483715992, -33.2426918278861, -72.0519479201516, 4.856841495253258]


qlearner = QLearner(weights, features)
prev_wrld = None


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

g.add_monster(SelfPreservingMonster("selfpreserving", # name
									"S",              # avatar
                                    3, 9,             # position
                                    1))                 # detection range

q_character = QCharacter("me", # name
                             "C",  # avatar
                           0, 0,  # position
                            qlearner,
                             False,
                             1)

#Uncomment this if you want the interactive character
g.add_character(q_character)

g.go(1)






