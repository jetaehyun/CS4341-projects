# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
import random
# TODO This is your code!
sys.path.insert(1, '../group01')

from sensed_world import SensedWorld
from events import Event

from helpers import *
from patrick_star import perform_aStar, _heuristic

def foundBomb(wrld):
	bombs = findAll(wrld, 1)

	return False if len(bombs) == 0 else True 

def can_move(wrld, pos, delta):
	dx = pos[0] + delta[0] 
	dy = pos[1] + delta[1]

	if inGrid(wrld, pos, delta) is False:
		return False 

	if wrld.wall_at(dx, dy) is True:
		return False

	return True


def bomb_handler(wrld, pos, delta):
	x, y = delta[0], delta[1]
	bombs = findAll(wrld, 1)
	# monsters = findAll(wrld, 2)
	# monstToChara = False
 
	# if len(monsters) > 0:
	# 	nearest_monster = findNearestEntity(wrld, pos, monsters)
	# 	pathToMonst = len(perform_aStar(wrld, pos, nearest_monster, True))
	
	# 	if pathToMonst != 0 and pathToMonst > 8:
	# 		monstToChara = True
	

	for bomb in bombs:
		dx = pos[0] + x 
		dy = pos[1] + y

		escape_directions = [-1, 1] 
  
		# if monstToChara is True:
		# 	# distX = pos[0] - nearest_monster[0]
		# 	distY = pos[1] - nearest_monster[1]
   
		# 	if distY < 0:
		# 		x = 1
		# 		y = 1
				
		# 		if can_move(wrld, pos, (x, y)) is False:
		# 			y *= -1
	 
		# 	return (x,y)

		if dx == bomb[0]:
			x = escape_directions[random.randint(0, 1)] if x == 0 else (x * -1)

			if can_move(wrld, pos, (x, y)) is False:
				x *= -1

		if dy == bomb[1]:
			y = escape_directions[random.randint(0, 1)] if y == 0 else (y * -1)

			# if can_move(wrld, pos, (x, y)) is False:
			# 	y *= -1

	return (x, y)

def explosion_occurring(wrld):
	for x in range(wrld.width()):
		for y in range(wrld.height()):
			if wrld.explosion_at(x, y) is not None:
				return True 

	return False

def explosion_handler(wrld, pos):
	x, y = pos[0], pos[1]
	if explosion_occurring(wrld) is True:
		return (0, 0)

	return x, y 

def explosion_handler2(wrld, pos, delta):
	x, y = delta[0], delta[1]
	bombs = findAll(wrld, 1)

	for bomb in bombs:
		dx = pos[0] + x 
		dy = pos[1] + y

		escape_directions = [-1, 1] 

		if dx == bomb[0]:
			x = escape_directions[random.randint(0, 1)] if x == 0 else (x * -1)

			if can_move(wrld, pos, (x, y)) is False:
				x *= -1

		if dy == bomb[1]:
			y = escape_directions[random.randint(0, 1)] if y == 0 else (y * -1)

			if can_move(wrld, pos, (x, y)) is False:
				y *= -1

	return (x, y)

def wallInPath(wrld, pos, delta):
	currX, currY = pos[0], pos[1]

	newX, newY = currX + delta[0], currY + delta[1]

	if inGrid(wrld, pos, delta):
		if wrld.wall_at(newX, newY):
			return True 

	return False 

def inGrid(wrld, pos, delta):
	dx = pos[0] + delta[0] 
	dy = pos[1] + delta[1]

	if dx < 0 or dx >= wrld.width():
		return False 

	if dy < 0 or dy >= wrld.height():
		return False 

	return True


def completeRowOfWalls(wrld, pos):
	currX, currY = pos[0], pos[1]

	for x in range(0, wrld.width()):
		if wrld.wall_at(x, currY) is False:
			return False 

	return True 


def topWall(wrld, pos):
	currX, currY = pos[0], pos[1]

	for y in range(-3, 0, 1):
		dy = currY + y

		pos = (currX, dy)

		if completeRowOfWalls(wrld, pos) is True:
			return True 

	return False 


def bottomWall(wrld, pos):
	currX, currY = pos[0], pos[1]

	for y in range(1, 4, 1):
		dy = currY + y

		pos = (currX, dy)

		if completeRowOfWalls(wrld, pos) is True:
			return True 


	return False

def surroundedByWalls(wrld, pos):
	
	if topWall(wrld, pos) and bottomWall(wrld, pos):
		return True

	return False


def allMonstersTrapped(wrld):

	monsters = findAll(wrld, 2)

	for monster in monsters:
		monsterPos = (monster[0], monster[1])

		if surroundedByWalls(wrld, monsterPos) is False:
			return False 

	return True

def allMonstersDead(wrld):
	monsters = findAll(wrld, 2)

	return True if len(monsters) == 0 else False 


def characterInWallRow(wrld, pos):
	walls = findAll(wrld, 3)

	nearest_wall = findNearestEntity(wrld, pos, walls)

	wall_row = nearest_wall[1]

	return pos[1] == wall_row


def safePathToExitWithMonster(wrld, pos):
	monsters = findAll(wrld, 2)
	exit = findAll(wrld, 0)
	
	charToExit = float(perform_a_star(wrld, pos, exit[0], True))
	
	if charToExit == 0:
		return False
	
	nearest_monster = findNearestEntity(wrld, pos, monsters)
	monstToExit = float(perform_a_star(wrld, nearest_monster, exit[0], True))
	
	if monstToExit > charToExit:
		return True
	
	return False
	
	
	
	
