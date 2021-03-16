# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from features import *

# TODO This is your code!
sys.path.insert(1, '../group01')
from testcharacter import TestCharacter

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, inBombExplosionRange, distanceToMonster, monsterToBomb, bomb_to_wall, distanceToWall, bombTimer]
#weights = [126.67921041823182, -38.28477185533087, -10.134174411752989, 3.9822536932994526, 2.782746176674528, 2.6255364626346243, 10.75701131617684]
weights = [136.05318909614874, -29.74172315089922, -3.3317683532687012, 4.451782608731871, 3.7562655432844676, 3.7773607267087024, 11.673651427137699]



qlearner = QLearner(weights, features)
N = 50
numOfWins = 0

for i in range(0, N):
	print('Iteration #', i)
	random.seed(random.randint(0, 1000))

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                    "S",              # avatar
                                    3, 9,             # position
                                    1                 # detection range
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
	print(score)

	if score > 400:
		numOfWins += 1

	print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))

print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')
