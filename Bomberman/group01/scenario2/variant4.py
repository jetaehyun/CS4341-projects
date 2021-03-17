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

features = [inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, distanceToMonster, inRadius3]
weights = [-44.6520034043336, 1.6721923695682053, 2.41678308288769, 0.19562856322164715, -0.010541500133580444, 2.316504343037947, -9.051171383704874, -0.4823988871411091]


qlearner = QLearner(weights, features)
N = 10
numOfWins = 0
for i in range(0, N): 
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
	score = g.world.scores["me"]

	if score > 0:
		numOfWins += 1

	print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))
