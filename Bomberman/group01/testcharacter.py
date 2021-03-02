# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

	def __init__(self, name, avatar, x, y, variantFlag):
		CharacterEntity.__init__(self, name, avatar, x, y)

		self.variant = variantFlag

	###
	# Description: gets the coordinate of the exit location
	# PARAMS: wrld - world object
	# RETURN: (width, height) - tuple of the exit coordinate
	###
	def get_exit_location(self, wrld):
		for w in range(wrld.width()):
			for h in range(wrld.h()):
				if wrld.exit_at(w, h):
					return (w, h)


    def do(self, wrld):
        # need to know where the exit is - function 
        pass
