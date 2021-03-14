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

features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, monsterFromExit, inBombExplosionRange, anyDroppedBombs, inRadius]

weights = None
#weights = [182.6988963919609, -0.06697338907055363, -25.595194698516, -22.38475360886873, -1.6742679285951199]
#weights = [178.6559472181669, -1.0851218606775932, -30.45498158628978, -22.38871482591737, -2.978455290846071]
qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 200):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	g.add_monster(SelfPreservingMonster("aggressive", # name
										"A",              # avatar
                                    	3, 13,             # position
                                    	2))                 # detection range

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


