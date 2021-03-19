# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from features import *

# TODO This is your code!
sys.path.insert(1, '../group01')
from testcharacter import TestCharacter

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, inBombExplosionRange, distanceToMonster, monsterToBomb, bomb_to_wall, distanceToWall, bombTimer]
weights = [136.05318909614874, -29.74172315089922, -3.3317683532687012, 4.451782608731871, 3.7562655432844676, 3.7773607267087024, 11.673651427137699]



qlearner = QLearner(weights, features)


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                 "S",              # avatar
                                 3, 9,             # position
                                1                 # detection range
	))

q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               False,
                               1)

#Uncomment this if you want the interactive character
g.add_character(q_character)

g.go(1)
