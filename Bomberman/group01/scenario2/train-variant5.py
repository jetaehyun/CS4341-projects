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
from StateCharacter import StateCharacter
from features import *

# best one
#[88.75619516596633, -5.46920048853008, -9.9417931693591, -2.9892287300876355, 14.574786014483674, 0.3802116660555037, -2.0073190227696367, 3.5183743748331446, 1.3715697237187943, 9.211555562667932, -2.423505317476378, -13.737615575176452]
# features = [distanceToExit, distanceToBomb, distanceToSmartMonster, inBombExplosionRange, anyDroppedBombs,
#             monsterFromExit, inRadius, monsterToBomb, bombDestroysWall, bombTimer,
#             monsterToNearestWall, doesPathToExitExist]
# weights = [88.75619516596633, -5.46920048853008, -9.9417931693591, -2.9892287300876355, 14.574786014483674, 0.3802116660555037, -2.0073190227696367, 3.5183743748331446, 1.3715697237187943, 9.211555562667932, -2.423505317476378, -13.737615575176452]


features = [distanceToExit, inBombExplosionRange,distanceToStupidMonster, distanceToSmartMonster, anyDroppedBombs, inRadius, bombTimer, total_number_of_walls]
#[-52.78006702872462, 0.5148877100366913, 2.11238592786106, 0.13990307547126168, -0.03447161086977752]
# weights = [-47.90193974134428, -2.623272706735263, 2.833456615840688, -0.9204928157561079, 0.03698300081441763]
weights = None
qlearner = QLearner(weights, features)
prev_wrld = None
N = 200
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

	q_character = StateCharacter("me", # name
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