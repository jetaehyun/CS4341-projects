# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, distanceToBomb, distanceToSmartMonster, inBombExplosionRange, monsterToNearestWall,
            inRadius, bombDestroysWall, monsterToBomb, doesPathToExitExist, total_number_of_walls]
#[119.782373541981, -2.1134484212963316, -16.953064223583446, -27.914784559844453, -2.2661656438384576, 0.5422961638252195, -6.17895690936024, -0.999035661034831, 2.0710540230798875, 1.2311657254900958, -7.934999800105533]

# test this
#[88.75619516596633, -5.46920048853008, -9.9417931693591, -2.9892287300876355, 14.574786014483674, 0.3802116660555037, -2.0073190227696367, 3.5183743748331446, 1.3715697237187943, 9.211555562667932, -2.423505317476378, -13.737615575176452]
#[distanceToExit, distanceToBomb, distanceToSmartMonster, inBombExplosionRange, anyDroppedBombs,
            # monsterFromExit, inRadius, monsterToBomb, bombDestroysWall, bombTimer,
            # monsterToNearestWall, doesPathExist]

#[142.17363991567993, -0.25576190233991236, -12.341235487926118, -43.32853502499624, 2.6689969323660803, 0.7099511426653067, 0.8276171479932031, 2.4026530379802264, 0.9159628945926811, 0.5080277745632032, 1.531911468797813, 0.6147055954370205]
weights = None
qlearner = QLearner(weights, features)
prev_wrld = None
N = 100
numOfWins = 0
seeds = []

for i in range(0, N):
    seeds.append(random.seed(random.randint(0, 10000)))

for i in range(0, N):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	random.seed(seeds[i]) # TODO Change this if you want different random choices

	g = Game.fromfile('map.txt')
	g.add_monster(StupidMonster("stupid", # name
        	                    "S",      # avatar
    	                        3, 5,     # position
	))
	g.add_monster(SelfPreservingMonster("aggressive", # name
            	                        "A",          # avatar
        	                            3, 13,        # position
    	                                2             # detection range
	))

	q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                            	True,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	score = g.world.scores["me"]
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)

	print('MY WEIGHTS')
	print(qlearner.weights)

	if score > 400:
		numOfWins += 1

print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')