# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

from StateCharacter1 import StateCharacter1

# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
q_character = StateCharacter1("me", # name
                               "C",  # avatar
                               0, 0,  # position
                                )

	#Uncomment this if you want the interactive character
g.add_character(q_character)


# Run!
g.go(1)

print(g.world.scores["me"])

