# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter

from QLearner import QLearner
from QCharacter import QCharacter
from StateCharacter import StateCharacter
from features import *

# Create the game

features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, character_btw_monster_bomb, inMonsterRange]
#features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, character_btw_monster_bomb]
#features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bombTimer, distanceToMonster]
#weights = [0.026307211952499653, -49.703088641849014, 3.8945078776391067, -1.3830224890124843, -0.20801889428318396, 0.008660961882211698, 0.27812312272866896, -4.494002911481876]
#weights = [-0.0005935473941769263, -51.53515022709986, 2.8895370919029624, -0.44692496045791696, -0.6979767153618994, 0.0008609613710392164, -0.22707770231690316, -0.2002370088844276]
#weights = [-0.0007493784122923247, -47.68173268176715, 2.9594309600069386, -1.0123472221417058, -3.9581312942455154, 0.01796024811608957, -0.03020824786931328, -9.065725116700494]
weights = [69.96678357549504, -26.868991042094397, 0.290781397860215, 1.5748226757557369, -7.379904200489241, -0.32749223287906565, 0.045787593356713265, -3.5003960368499674, -23.738590781189437]



qlearner = QLearner(weights, features)
N = 10
numOfWins = 0
for i in range(0, N): 
	random.seed(random.randint(0, 100))
	g = Game.fromfile('map.txt')
	g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
	))

	state_character = StateCharacter("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              qlearner,
                              False,
                              0
	)

	# TODO Add your character
	g.add_character(state_character)

	g.go(1)
	score = g.world.scores["me"]

	if score > 0:
		numOfWins += 1

	print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))
