# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features1 import *

features = [distToMonster, distToExit, distToBomb, distToWall, bombDropped]
weights = [-8.547008547008543, -4.273504273504272, -38.46153846153847, -12.820512820512818, -42.73504273504273]
qlearner = QLearner(weights, features)

for i in range(0, 10):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
	))

	q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               True,
                               i,
                               1000)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go()
	wrld = q_character.getWorld()
	print(g.world.scores["me"])
	q_character.updateCharacterWeights(wrld, False, True)

	print('MY WEIGHTS')
	print(qlearner.weights)


