# This is necessary to find the main code
import sys
import random



sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from QLearner import QLearner
from QCharacter import QCharacter
from features import *
from monsters.selfpreserving_monster import SelfPreservingMonster

features = [distanceToExit, inBombExplosionRange, distanceToMonster, monsterToBomb, bomb_to_wall, distanceToWall, bombTimer]

weights = None

qlearner = QLearner(weights, features)
prev_wrld = None
for i in range(0, 100):
    print('Iteration #', i)

    # Create the game
    #random.seed(random.randint(0, 1000))distanceToBomb, distanceToBomb, 
    g = Game.fromfile('map.txt')

    # TODO Add your character

    g.add_monster(SelfPreservingMonster("selfpreserving", # name
                            "S",      # avatar
                            3, 9,
                            1# position
    ))

    q_character = QCharacter("me", # name
                               "C",  # avatar
                               0, 0,  # position
                               qlearner,
                               True,
                               i)

    g.add_character(q_character)

    g.go(1)
    print(g.world.scores["me"])


    print('MY WEIGHTS')
    print(qlearner.weights)


