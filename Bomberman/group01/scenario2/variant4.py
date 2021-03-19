# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!

from StateCharacter4 import StateCharacter4
from features import *

# Create the game
g = Game.fromfile('map.txt')

g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
	))

state_character = StateCharacter4("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              )

# TODO Add your character
g.add_character(state_character)

g.go(1)