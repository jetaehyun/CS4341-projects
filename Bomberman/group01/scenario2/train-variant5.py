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
from StateCharacter4 import StateCharacter4
from features import *

features = [monsterInLineOfSight, stuckInCorner, monsterPastWall,inBombExplosionRange, bombTimer, distanceToSmartMonster]

weights = [1.4831881831911438, 0.8931840360913579, 0.6964219975329767, -50.60325121251399, 0.6892064736831113, 0.2416027170828847]
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

	q_character = StateCharacter4("me", # name
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