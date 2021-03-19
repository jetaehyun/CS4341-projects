# This is necessary to find the main code
import sys, random
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


features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, monsterFromExit, inBombExplosionRange, anyDroppedBombs, inRadius1, monsterToBomb]

weights = None
qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 150):
	print('Iteration #', i)
	random.seed(random.randint(0, 1000))
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
                               True,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)

	print('MY WEIGHTS')
	print(qlearner.weights)


