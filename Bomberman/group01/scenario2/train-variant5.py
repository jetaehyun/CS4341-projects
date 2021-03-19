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

# features = [distanceToMonster, distanceToWall, distanceToBomb, inMonsterRange]

features = [distanceToStupidMonster, diagonalOfBomb, monsterToNearestWall]
# features = [distanceToStupidMonster, inBombExplosionRange, monsterToNearestWall, anyDroppedBombs]
# weights = [-8.903161609374699, -22.003626294921453, -13.833462417203572, -3.5812684740503853]

weights = [-439.56405095613394, -81.88835388811911, 33.243918944294634]
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

	q_character = StateCharacter("me", # name
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