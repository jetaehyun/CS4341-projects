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
from features import *

#features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, inBombExplosionRange, anyDroppedBombs]
features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]
#weights = [159.78738293256993, -0.6215573402097863, -18.636221001030794, -3.554655669452952, -1.3020421285039028, 2.9151051402250623]
#weights = [191.98886121017304, 3.772476271735364, -18.457315008153348, -11.465459325834754, -87.36783961649446, -7.553717764697351]
weights = [177.2277174308819, -0.7130756483715992, -33.2426918278861, -72.0519479201516, 4.856841495253258]

numOfWins = 0
qlearner = QLearner(weights, features)
prev_wrld = None
N = 10
for i in range(0, N):
	print('Iteration #', i)

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
                               i)

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


