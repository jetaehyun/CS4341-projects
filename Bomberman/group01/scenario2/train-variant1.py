# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, distanceToBomb, inBombExplosionRange, anyDroppedBombs]

weights = [114.69554463857256, -2.861841880284248,  -6.044985197169929, 8.175889714036572]

qlearner = QLearner(weights, features)
prev_wrld = None
numOfWins = 0
for i in range(0, 10):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character



	q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
							   False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)
	score = g.world.scores["me"]
	if score > 400:
		numOfWins += 1
	print(f'WIN PERCENTAGE: {numOfWins / (i+1)}')



