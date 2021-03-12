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

features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs]

#weights = [0.07454250024312192, -1.3927287666669574, 0.5408097345211125, -42.307289465625345, -12.534558900002617]
#weights = [48.22191700745971, -3.960068253593247, -6.948051352419573, -7.29968753572757, 5.742455559360193]
#weights = [7.936803258605797, -0.16809098876621326, -2.487543588003159, 4.05296286434909, 5.68763111356333]
# [7.536734293235794, -0.9951780814978648, -6.316881082677425, 2.799043211342837, 3.494437161228158]

#weights = [173.95171287537622, -4.787791163711921, -12.269904472356515, -20.778013726358505, 3.8076070950701517]
weights = [173.17464200348178, -1.8397384409939697, -28.549911042490006, -22.392729217308883, 0.050295801861828845]

qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 100):
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
                               False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)

	print('MY WEIGHTS')
	print(qlearner.weights)


