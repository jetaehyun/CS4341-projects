# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from math import sqrt
from queue import PriorityQueue
from patrick_star import _aStar, get_exit_location, perform_aStar

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
    # def get_exit_location(self, wrld):
        # for w in range(wrld.width()):
            # for h in range(wrld.height()):
                # if wrld.exit_at(w, h):
                    # return (w, h)


    def do(self, wrld):

        if self.state == "aStar":
            if self.seek_path(wrld) == None:
                print("None")
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
        search = perform_aStar(wrld, (self.x, self.y), False)

        if search == None:
            return
        self.move(search[0], search[1])

    # # --------------------------------------------------------------------------
    # ##
    # # @Brief calculate the distance from current to goal
    # #
    # # @Param goal where we want to go
    # # @Param current where we are
    # #
    # # @Returns distance
    # # --------------------------------------------------------------------------
    # def _heuristic(self, goal, current):
        # return sqrt((goal[0] - current[0])**2 + (goal[1] - current[1])**2)


    # # --------------------------------------------------------------------------
    # ##
    # # @Brief A* algorithm
    # #
    # # @Param wrld world object
    # # @Param x x position of character
    # # @Param y y position of character
    # #
    # # @Returns dictionary of where each (x,y) came from
    # # --------------------------------------------------------------------------
    # def _aStar(self, wrld, x, y):
        # frontier = PriorityQueue()
        # frontier.put((x,y), 0)
        # came_from = {}
        # cost_so_far = {}
        # came_from[(x,y)] = None
        # cost_so_far[(x,y)] = 0

        # goal = self.get_exit_location(wrld)

        # while not frontier.empty():
            # current = frontier.get()
            # if current == goal: # break once the exit has been found
                # break

            # # create a list of neighbors at current position
            # neighX, neighY = current
            # neighbors = [(neighX-1,neighY), (neighX+1,neighY), (neighX,neighY+1), (neighX,neighY-1), (neighX+1,neighY+1),
                    # (neighX+1,neighY-1), (neighX-1, neighY+1), (neighX-1,neighY-1)] # left, right, up, down

            # # check each neighbor
            # for i in neighbors:
                # x1,y1 = i

                # if x1 < 0 or x1 >= wrld.width() or y1 < 0 or y1 >= wrld.height(): # out of bounds
                    # continue
                
                # if wrld.wall_at(x1, y1) or wrld.monsters_at(x1, y1) != None: # wall or monster(s)
                    # continue

                # distStartToCur = sqrt((x1-x)**2 + (y1-y)**2)        # calculate the cost it took to get here from starting node
                # new_cost = cost_so_far[current] + distStartToCur    # add up the costs

                # if i not in cost_so_far or new_cost < cost_so_far[i]:
                    # cost_so_far[i] = new_cost 
                    # priority = new_cost + self._heuristic(goal, i) # f = g + h
                    # frontier.put(i, priority)
                    # came_from[i] = current

        # if not goal in came_from.keys():
            # return None

        # return came_from
