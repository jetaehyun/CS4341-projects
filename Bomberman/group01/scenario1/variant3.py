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
weights = [82.61768802204456, -1.1871931369125877, -15.06091124995377, -4.13591204084948, -19.488652143280845, 1.3357752186026706]

numOfWins = 0
qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 10):
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
                               False,
                               i)

	#Uncomment this if you want the interactive character
	g.add_character(q_character)

	g.go(1)
	score = g.world.scores["me"]
	print(score)

	if score > 400:
		numOfWins += 1


print(f'WON: {numOfWins} out of 10')
print(f'WIN PERCENTAGE: {numOfWins / 10}')


