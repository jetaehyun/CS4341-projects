# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features1 import *

features = [distanceToExit, distanceToBomb, distanceToMonster, distanceToSmartMonster, inBombExplosionRange, anyDroppedBombs]

#weights = [0.07454250024312192, -1.3927287666669574, 0.5408097345211125, -42.307289465625345, -12.534558900002617]
#weights = [48.22191700745971, -3.960068253593247, -6.948051352419573, -7.29968753572757, 5.742455559360193]
#weights = [7.936803258605797, -0.16809098876621326, -2.487543588003159, 4.05296286434909, 5.68763111356333]
#weights = [151.8339062609312, -3.797528809195254, -18.788182544708963, -2.3597287470390147, -20.21465181426199, 2.616117293788106]

#weights = [158.2321605318441, -1.8480947526392106, -19.85272152516951, 0.47593996481356093, -20.806451798407036, 2.8326522788742654]
#weights = [-0.0014731353844448809, 0.63982395598296, -19.88923508228701, -22.022121698144286, -0.26396478487768343]

weights = None
qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 150):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	g.add_monster(SelfPreservingMonster("selfpreserving", # name
										"S",              # avatar
                                    	3, 9,             # position
                                    	1))                 # detection range

	q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               True,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)

	print('MY WEIGHTS')
	print(qlearner.weights)


