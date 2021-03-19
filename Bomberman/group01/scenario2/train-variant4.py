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

from StateCharacter4 import StateCharacter4

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
    )

    g.add_character(state_character)

    g.go(1)
    score = g.world.scores["me"]

    if score > 0:
      numOfWins += 1


    print("{}, {:.2f}%".format(g.world.scores["me"], numOfWins/(i+1)*100))




