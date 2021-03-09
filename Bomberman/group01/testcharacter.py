# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from math import sqrt
from queue import PriorityQueue
from patrick_star import _aStar, perform_aStar

class TestCharacter(CharacterEntity):

    state = None

    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.state = "aStar"

	###
	# Description: gets the coordinate of the exit location
	# PARAMS: wrld - world object
	# RETURN: (width, height) - tuple of the exit coordinate
	###
    def get_exit_location(self, wrld):
        for w in range(wrld.width()):
            for h in range(wrld.height()):
                if wrld.exit_at(w, h):
                    return (w, h)


    def do(self, wrld):

        if self.state == "aStar":
            self.seek_path(wrld)
        else:
            print("Default")

    # --------------------------------------------------------------------------
    ##
    # @Brief check to see if a monster is line of sight
    #
    # @Param wrld world object
    #
    # @Returns x, y, and direction of monster (x, y, direction)
    # --------------------------------------------------------------------------
    def _checkRadius(self, wrld):
        x, y = self.x, self.y
        whereIsMonster = ""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)] # left, right, down, up, diagonal up right, diagonal down right, diagonal up left, diagonal down left 

        for i in range(len(directions)):
            lineOfSight = directions[i]
            dx = lineOfSight[0]
            dy = lineOfSight[1]

            xAhead = x
            yAhead = y
            for j in range(2):
                xAhead += dx
                yAhead += dy

                if xAhead >= wrld.width() or xAhead < 0 or yAhead >= wrld.height() or yAhead < 0:
                    continue

                if wrld.monsters_at(xAhead, yAhead) != None:
                    if i == 0:
                        whereIsMonster = "left"
                    elif i == 1:
                        whereIsMonster = "right"
                    elif i == 2:
                        whereIsMonster = "up"
                    elif i == 3:
                        whereIsMonster = "down"
                    elif i == 4:
                        whereIsMonster = "DUR"
                    elif i == 5:
                        whereIsMonster = "DDR"
                    elif i == 6:
                        whereIsMonster = "DUL"
                    else:
                        whereIsMonster = "DDL"

                    return (xAhead, yAhead, whereIsMonster)
                    

        return (x, y, whereIsMonster)

    # --------------------------------------------------------------------------
    ##
    # @Brief performs the a star search to the the exit
    #
    # @Param wrld world object
    #
    # @Returns None
    # --------------------------------------------------------------------------  	
    def seek_path(self, wrld):
        search = perform_aStar(wrld, (self.x, self.y), self.get_exit_location(wrld), False)

        if search == None:
            return
        self.move(search[0], search[1])
