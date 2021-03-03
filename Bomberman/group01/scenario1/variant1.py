# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from testcharacter import TestCharacter

# Uncomment this if you want the interactive character
# from interactivecharacter import InteractiveCharacter

# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

# Uncomment this if you want the test character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              0
))

# Uncomment this if you want the interactive character
<<<<<<< HEAD
# g.add_character(InteractiveCharacter("me", # name
#                                      "C",  # avatar
#                                      0, 0  # position
# ))
=======
g.add_character(InteractiveCharacter("me", 		# name
                                     "C",  		# avatar
                                     0, 0,  	# position
                                     1			# variant
))
>>>>>>> 69de55f45e4fa4c552a349fecad8014ac1a7e147

# Run!

# Use this if you want to press ENTER to continue at each step
#g.go(0)

# Use this if you want to proceed automatically
g.go(1)
