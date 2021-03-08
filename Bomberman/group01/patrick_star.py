from math import sqrt
from queue import PriorityQueue


def get_exit_location(wrld):
    for w in range(wrld.width()):
        for h in range(wrld.height()):
            if wrld.exit_at(w, h):
                return (w, h)

    # --------------------------------------------------------------------------
    ##
    # @Brief performs the a star search to the the exit
    #
    # @Param wrld world object
    #
    # @Returns None
    # --------------------------------------------------------------------------  	
def perform_aStar(wrld, position, getFullPath):

    x,y = position
    searchResults = _aStar(wrld, x, y)

    if searchResults == None:
        return None

    # unravel path from A*
    path = []
    current = get_exit_location(wrld)
    path.append(current)
    while(True): 
        came_from = searchResults[current] # find out where this path came from
        if came_from == None:              # we found the exit
            break
        path.append(current)
        current = came_from                # set next search

    pathRev = path[::-1]                   # reverse the list to get the correct direction

    if getFullPath:
        return pathRev

    # calculate the direction to go to
    dx = pathRev[0][0] - x   
    dy = pathRev[0][1] - y
    #print("Going: " + str(dx) + " " + str(dy))

    return (dx, dy)
    # self.move(dx, dy)



    # --------------------------------------------------------------------------
    ##
    # @Brief calculate the distance from current to goal
    #
    # @Param goal where we want to go
    # @Param current where we are
    #
    # @Returns distance
    # --------------------------------------------------------------------------
def _heuristic(goal, current):
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
def _aStar(wrld, x, y):
    frontier = PriorityQueue()
    frontier.put((x,y), 0)
    came_from = {}
    cost_so_far = {}
    came_from[(x,y)] = None
    cost_so_far[(x,y)] = 0

    goal = get_exit_location(wrld)

    while not frontier.empty():
        current = frontier.get()
        if current == goal: # break once the exit has been found
            break

            # create a list of neighbors at current position
        neighX, neighY = current
        neighbors = [(neighX-1,neighY), (neighX+1,neighY), (neighX,neighY+1), (neighX,neighY-1), (neighX+1,neighY+1),
                (neighX+1,neighY-1), (neighX-1, neighY+1), (neighX-1,neighY-1)] # left, right, up, down

            # check each neighbor
        for i in neighbors:
            x1,y1 = i

            if x1 < 0 or x1 >= wrld.width() or y1 < 0 or y1 >= wrld.height(): # out of bounds
                continue
                
            if wrld.wall_at(x1, y1) or wrld.monsters_at(x1, y1) != None: # wall or monster(s)
                continue

            distStartToCur = sqrt((x1-x)**2 + (y1-y)**2)        # calculate the cost it took to get here from starting node
            new_cost = cost_so_far[current] + distStartToCur    # add up the costs

            if i not in cost_so_far or new_cost < cost_so_far[i]:
                cost_so_far[i] = new_cost 
                priority = new_cost + _heuristic(goal, i) # f = g + h
                frontier.put(i, priority)
                came_from[i] = current

    if not goal in came_from.keys():
        return None

    return came_from
