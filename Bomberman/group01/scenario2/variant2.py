# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from features import *

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs, bomb_to_wall, inRadius]
weights = [78.80623936169042, -2.405217606634862, -14.655308246771089, -7.328130461876308, 11.503787618791137, 3.421432340195113e-06, -0.5496048915549938]


qlearner = QLearner(weights, features)
N = 50
numOfWins = 0

for i in range(0, N):
	print('Iteration #', i)
	random.seed(random.randint(0, 1000))

	# Create the game
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
	score = g.world.scores["me"]
	print(score)

	if score > 400:
		numOfWins += 1

	print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))

print(f'WON: {numOfWins} out of {N}')
print(f'WIN PERCENTAGE: {numOfWins / N}')
