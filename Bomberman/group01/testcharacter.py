# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from math import sqrt
from queue import PriorityQueue

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
            for h in range(wrld.height()):
                if wrld.exit_at(w, h):
                    return (w, h)


    def do(self, wrld):
        # need to know where the exit is - function 
        searchResults = self._aStar(wrld, self.x, self.y)

        # unravel path from A*
        path = []
        current = self.get_exit_location(wrld)
        path.append(current)
        while(True): 
            came_from = searchResults[current] # find out where this path came from
            if came_from == None: # we found the exit
                break
            path.append(current)
            current = came_from # set next search

        pathRev = path[::-1][0] # reverse the list to get the correct direction

        # calculate the direction to go to
        dx = pathRev[0] - self.x   
        dy = pathRev[1] - self.y
        #print("Going: " + str(dx) + " " + str(dy))
        self.move(dx, dy)

    # --------------------------------------------------------------------------
    ##
    # @Brief calculate the distance from current to goal
    #
    # @Param goal where we want to go
    # @Param current where we are
    #
    # @Returns distance
    # --------------------------------------------------------------------------
    def _heuristic(self, goal, current):
        return sqrt((goal[0] - current[0])**2 + (goal[1] - current[1])**2)


    # --------------------------------------------------------------------------
    ##
    # @Brief A* algorithm
    #
    # @Param wrld world object
    # @Param x x position of character
    # @Param y y position of character
    #
    # @Returns dictionary of where each (x,y) came from
    # --------------------------------------------------------------------------
    def _aStar(self, wrld, x, y):
        frontier = PriorityQueue()
        frontier.put((x,y), 0)
        came_from = {}
        cost_so_far = {}
        came_from[(x,y)] = None
        cost_so_far[(x,y)] = 0

        goal = self.get_exit_location(wrld)

        while not frontier.empty():
            current = frontier.get()
            if current == goal: # break once the exit has been found
                break

            # create a list of neighbors at current position
            neighX, neighY = current
            neighbors = [(neighX-1,neighY), (neighX+1,neighY), (neighX,neighY+1), (neighX,neighY-1)] # left, right, up, down

            # check each neighbor
            for i in neighbors:
                x1,y1 = i

                if x1 < 0 or x1 >= wrld.width() or y1 < 0 or y1 >= wrld.height(): # out of bounds
                    continue
                
                if wrld.wall_at(x1, y1): # wall
                    continue

                distStartToCur = sqrt((x1-x)**2 + (y1-y)**2)        # calculate the cost it took to get here from starting node
                new_cost = cost_so_far[current] + distStartToCur    # add up the costs

                if i not in cost_so_far or new_cost < cost_so_far[i]:
                    cost_so_far[i] = new_cost 
                    priority = new_cost + self._heuristic(goal, i) # f = g + h
                    frontier.put(i, priority)
                    came_from[i] = current


        return came_from
                    


