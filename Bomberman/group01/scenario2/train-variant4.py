# This is necessary to find the main code
import sys, random
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
from StateCharacter import StateCharacter
from features import *

features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, distanceToMonster]
weights = None

qlearner = QLearner(weights, features)

for i in range(0, 200):
    print('Iteration #', i)

    # Create the game
    #random.seed(random.randint(0, 1000))distanceToBomb, distanceToBomb, 
    g = Game.fromfile('map.txt')

    # TODO Add your character

    g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
	))

    state_character = StateCharacter("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              qlearner,
                              True,
                              i
    )

    g.add_character(state_character)

    g.go(1)
    print(g.world.scores["me"])


    print('MY WEIGHTS')
    print(qlearner.weights)




