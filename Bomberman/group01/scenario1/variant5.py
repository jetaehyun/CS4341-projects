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
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, distanceToBomb, distanceToSmartMonster, inBombExplosionRange, anyDroppedBombs,
            monsterFromExit, inRadius, monsterToBomb, monsterToNearestWall]

weights = [84.97696334172039, -0.08781776652353387, -14.86882125034955, -2.8169998761614785, 4.728037089732384, -1.3839415969552675, -2.4985137898174625, -1.7450048143550225, 9.318307041174288]
qlearner = QLearner(weights, features)
prev_wrld = None

N = 10
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
	# random.seed(123) # TODO Change this if you want different random choices
	g = Game.fromfile('map.txt')
	g.add_monster(StupidMonster("selfpreserving", # name
        	                    "S",      # avatar
    	                        3, 5,     # position
	))
	g.add_monster(SelfPreservingMonster("stupid", # name
            	                        "A",          # avatar
        	                            3, 13,        # position
    	                                2             # detection range
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
	score = g.world.scores["me"]
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)

	print('MY WEIGHTS')
	print(qlearner.weights)

	if score > 400:
		numOfWins += 1

print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')