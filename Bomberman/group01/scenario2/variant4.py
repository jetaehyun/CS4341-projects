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

features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, distanceToMonster]
weights = [0.026307211952499653, -49.703088641849014, 3.8945078776391067, -1.3830224890124843, -0.20801889428318396, 0.008660961882211698, 0.27812312272866896, -4.494002911481876]



qlearner = QLearner(weights, features)
N = 10
numOfWins = 0
for i in range(0, N): 
	random.seed(random.randint(0, 100))
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
