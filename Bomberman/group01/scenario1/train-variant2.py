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
from features1 import *

features = [distToMonster, distToExit, distToBomb, distToWall, inBombExplosionRange]
#[-19.3896499238949, -48.4741248097407, -87.25342465753285, -29.08447488584545, -96.9482496194814]

weights = [-24.477947236340455, -1.2238973618170195, -48.95589447268091, -24.477947236340455, -55.35263663944667]

#weights = None
qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 15):
	print('Iteration #', i)

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
                               True,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go()
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	q_character.updateCharacterWeights(wrld, False, True)

	print('MY WEIGHTS')
	print(qlearner.weights)


