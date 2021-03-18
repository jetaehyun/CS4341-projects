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
from StateCharacter4 import StateCharacter4
from features import *

features = [distanceToExit, inBombExplosionRange, anyDroppedBombs, inRadius, monsterToBomb, bomb_to_wall, bombTimer, character_btw_monster_bomb, inMonsterRange]
weights = None

qlearner = QLearner(weights, features)
numOfWins = 0
for i in range(0, 10):
    print('Iteration #', i)

    # Create the game
    random.seed(random.randint(0, 1000))
    g = Game.fromfile('map.txt')

    # TODO Add your character

    g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
	))

    state_character = StateCharacter4("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              qlearner,
                              True,
                              i
    )

    g.add_character(state_character)

    g.go(1)
    score = g.world.scores["me"]

    if score > 0:
      numOfWins += 1


    print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))




