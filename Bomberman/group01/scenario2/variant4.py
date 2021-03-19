# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter

from QLearner import QLearner
from QCharacter import QCharacter
from StateCharacter import StateCharacter
from features import *

# Create the game

features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, character_btw_monster_bomb, inMonsterRange]

weights = [69.96678357549504, -26.868991042094397, 0.290781397860215, 1.5748226757557369, -7.379904200489241, -0.32749223287906565, 0.045787593356713265, -3.5003960368499674, -23.738590781189437]

qlearner = QLearner(weights, features)


g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
	))

state_character = StateCharacter("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              qlearner,
                              False,
                              0
	)

# TODO Add your character
g.add_character(state_character)

g.go(1)