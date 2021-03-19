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

features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, monsterFromExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb]

# WIN RATE: 76-80% 
weights = [142.83436052987622, 2.3935722386778173, -14.693930403334434, 0.0644259835747207, 1.5729782904616798, -7.999804831642161, 2.8070100445367734, -2.030695531139905, 3.82815842223105]


qlearner = QLearner(weights, features)
prev_wrld = None
N = 10
numOfWins = 0
for i in range(0, N):
	print('Iteration #', i)
	random.seed(random.randint(0, 1000))

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
                               False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	score = g.world.scores["me"]
	print(score)

	if score > 400:
		numOfWins += 1

	print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))

print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')


