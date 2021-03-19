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


#features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]

#weights = [131.8721386644834, -2.241117133834206, -34.586094590111074, -33.52603583704115, -8.314934606824577]
#weights = [159.78738293256993, -0.6215573402097863, -18.636221001030794, -3.554655669452952, -1.3020421285039028, 2.9151051402250623]

features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, monsterFromExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb]
weights = [142.83436052987622, 2.3935722386778173, -14.693930403334434, 0.0644259835747207, 1.5729782904616798, -7.999804831642161, 2.8070100445367734, -2.030695531139905, 3.82815842223105]
#weights = [146.33681531239796, -0.25385244429328574, -13.847815323005145, -7.620411880705918, -1.7459395969606089, -32.39948325365655, -8.797012407353018, 2.669574645669025, 1.167698665216529]

numOfWins = 0
qlearner = QLearner(weights, features)
prev_wrld = None
N = 50
for i in range(0, N):
	print('Iteration #', i)
	#random.seed(random.randint(0, 1000))

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
                               False,
                               i, 
                               False)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	score = g.world.scores["me"]
	print(score)

	if score > 400:
		numOfWins += 1

	print(f'PERCENTAGE: {numOfWins / (i+1)}')


print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')


