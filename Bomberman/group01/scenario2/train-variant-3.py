# This is necessary to find the main code
import sys
import random



sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features2 import *
from monsters.selfpreserving_monster import SelfPreservingMonster

numOfWins =0
features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]
weights = [99.01502595145853, -3.024368630487915, -24.227424565497664, -4.647379985530353, -1.0585944409653059]

qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 10):
	print('Iteration #', i)

	# Create the game
	random.seed(random.randint(0,290344))
	g = Game.fromfile('map.txt')

	# TODO Add your character

	g.add_monster(SelfPreservingMonster("selfpreserving", # name
                            "S",      # avatar
                            3, 9,
                            1# position
	))

	q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)
	score = g.world.scores["me"]

	print('MY WEIGHTS')
	print(qlearner.weights)


