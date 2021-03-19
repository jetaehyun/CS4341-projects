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
# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *

features = [distanceToExit, distanceToBomb, distanceToMonster, inBombExplosionRange, anyDroppedBombs, bomb_to_wall]
weights = [139.78076720937227, 1.4224294781714875, -8.095538475997134, -42.5108559198316, 0.43457010740038093, 0.2378080895637052]



qlearner = QLearner(weights, features)



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
                               1)

#Uncomment this if you want the interactive character
g.add_character(q_character)

g.go(1)

print(g.world.scores["me"])
