# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff

from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
from QLearner import QLearner
from StateCharacter import StateCharacter
from features import *
# TODO This is your code!
features = [distanceToStupidMonster, diagonalOfBomb, monsterToNearestWall]
weights = [-439.56405095613394, -81.88835388811911, 33.243918944294634]
qlearner = QLearner(weights, features)


# Create the game
# TODO Change this if you want different random choices
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

# TODO Add your character
q_character = StateCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                            	False,
                               1)

	#Uncomment this if you want the interactive character
g.add_character(q_character)

# Run!
g.go(1)

print(g.world.scores["me"])
