from patrick_star import perform_aStar, _heuristic
from queue import PriorityQueue

# --------------------------------------------------------------------------
##
# @Brief find the nearest entity to the character
#
# @Param wrld world object
# @Param character position of character (x,y)
# @Param entity desired entity to find
#
# @Returns None: nothing found, position tuple (x,y)
# --------------------------------------------------------------------------
def findNearestEntity(wrld, pos, entities):
	x, y = pos[0], pos[1]
	width, height = wrld.width(), wrld.height()
	
	nearest_entity = entities[0]

	for entity in entities:
		if _heuristic((x,y), entity) < _heuristic((x,y), nearest_entity):
			nearest_entity = entity

	return nearest_entity


def findAll(wrld, entityFlag):
	entities = []

	for w in range(wrld.width()):
		for h in range(wrld.height()):
			if entityFlag == 0:
				if wrld.exit_at(w, h):
					entities.append((w, h))

			elif entityFlag == 1:
				if wrld.bomb_at(w, h) is not None:
					entities.append((w, h))

			elif entityFlag == 2:
				if wrld.monsters_at(w, h):
					entities.append((w, h))

			elif entityFlag == 3:
				if wrld.wall_at(w, h):
					entities.append((w, h))

			elif entityFlag == 4:
				if wrld.explosion_at(w, h) is not None:
					entities.append((w, h))

	return entities


def perform_a_star(wrld, start, destination, includeWalls=True):
	frontier = PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0

	while not frontier.empty():
		current = frontier.get()
		if current == destination: # break once the exit has been found
			break

		# create a list of neighbors at current position
		neighX, neighY = current
		neighbors = [(neighX-1,neighY), (neighX+1,neighY), (neighX,neighY+1), (neighX,neighY-1), (neighX+1,neighY+1),
				(neighX+1,neighY-1), (neighX-1, neighY+1), (neighX-1,neighY-1)] # left, right, up, down

		# check each neighbor
		for next_cell in neighbors:
			x, y = next_cell

			if x < 0 or x >= wrld.width() or y < 0 or y >= wrld.height(): # out of bounds
				continue
			
			if includeWalls is True:
				if wrld.wall_at(x, y): # wall or monster(s)
					cost = 10

				else:
					cost = 1

			else:
				cost = 1

			new_cost = cost_so_far[current] + cost    			# add up the costs

			if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
				cost_so_far[next_cell] = new_cost 
				priority = new_cost + _heuristic(destination, next_cell) # f = g + h
				frontier.put(next_cell, priority)
				came_from[next_cell] = current

	current = destination
	my_path = []

	while current != start:
		my_path.append(current)
		current = came_from[current]

	my_path.append(start)
	my_path[::-1] 

	return cost_so_far[destination]

	