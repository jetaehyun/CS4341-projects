# This is necessary to find the main code
import sys
import random

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features2 import *

numOfWins =0
features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]
weights = [151.3165613674901, -2.5215911378156255, -23.430249878167054, -0.1671006070009438, 3.6843296791750113]

qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 10):
	print('Iteration #', i)

	# Create the game
	random.seed(random.randint(0,290344))
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
                               False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)
	score = g.world.scores["me"]
	if score > 400:
		numOfWins += 1
	print(f'WON: {numOfWins} out of 10')
	print(f'WIN PERCENTAGE: {numOfWins / 10}')

	print('MY WEIGHTS')
	print(qlearner.weights)


