# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from patrick_star import perform_aStar, _heuristic
from queue import PriorityQueue

from helpers import *


def distanceToExit(wrld, character):
	exit = findAll(wrld, 0)

	if len(exit) == 0: 
		return 0

	pos = (character.x, character.y)

	nearest_exit = findNearestEntity(wrld, pos, exit)

	distance = float(perform_a_star(wrld, pos, nearest_exit))

	return (1 / (distance + 1)) ** 2


def distanceToBomb(wrld, character):
	bombs = findAll(wrld, 1)

	if len(bombs) == 0: 
		return 0

	pos = (character.x, character.y)

	nearest_bomb = findNearestEntity(wrld, pos, bombs)

	distance = float(perform_a_star(wrld, pos, nearest_bomb))

	return (1 / (distance + 1)) ** 2


def distanceToMonster(wrld, character):
	monsters = findAll(wrld, 2)

	if len(monsters) == 0: 
		return 0

	pos = (character.x, character.y)

	nearest_monster = findNearestEntity(wrld, pos, monsters)
	
	distance = float(perform_a_star(wrld, pos, nearest_monster))


	return (1 / (distance + 1)) ** 2


def distanceToWall(wrld, character):
	walls = findAll(wrld, 3)

	if len(walls) == 0:
		return 0

	pos = (character.x, character.y)

	nearest_wall = findNearestEntity(wrld, pos, walls)

	distance = float(perform_a_star(wrld, pos, nearest_wall))

	return (1 / (distance + 1)) ** 2

	
def inBombExplosionRange(wrld, character):
   
	x, y = character.x, character.y
	'''
	for i in range(2):
		if wrld.explosion_at(x, y) is not None:
			return 1

		wrld, events = wrld.next()
	'''

	if wrld.me(character) is None:
		return 1

	if wrld.explosion_at(character.x, character.y) is not None:
		return 1

	wrld, events = wrld.next()

	if wrld.explosion_at(character.x, character.y) is not None:
		return 1


	return 0


def anyDroppedBombs(wrld, character):
	if len(findAll(wrld, 1)) > 0:
		return 1

	else:
		return 0


def distanceToSmartMonster(wrld, character):
	monsters = findAll(wrld, 2)

	if len(monsters) == 0: 
		return 0

	pos = (character.x, character.y)

	nearest_monster = findNearestEntity(wrld, pos, monsters)

	monstersEntity = wrld.monsters_at(nearest_monster[0], nearest_monster[1])[0]

	
	distance = float(perform_a_star(wrld, pos, nearest_monster)) + 1

	if monstersEntity.name == "selfpreserving" or monstersEntity.name == "stupid":
		if distance <= 2:
			return ((3 - distance) / 3)

	elif monstersEntity.name == "aggressive":
		if distance <= 3:
			return ((4 - distance) / 4)

	return 0


def total_number_of_walls(wrld,character):
	walls = findAll(wrld,3)

	return (1/(len(walls)+1))**2


def monsterFromExit(wrld, character):
	monsters = findAll(wrld, 2)
	exit = findAll(wrld, 0)

	if len(monsters) == 0 or len(exit) == 0:
		return 0

	pos = (exit[0][0], exit[0][1])

	nearest_monster = findNearestEntity(wrld, pos, monsters)

	distance = float(perform_a_star(wrld, pos, nearest_monster))

	return (1 / (distance + 1)) ** 2


def __inWorld(wrld, dx, dy):
	if dx < 0 or dx >= wrld.width():
		return False 

	if dy < 0 or dy >= wrld.height():
		return False

	return True 


def inRadius(wrld, character):
	radius = [i for i in range(-8, 9, 1)]

	for i in range(len(radius)):
		for j in range(len(radius)):
			dx = character.x + radius[i]
			dy = character.y + radius[j]

			if __inWorld(wrld, dx, dy) is True:
				if wrld.monsters_at(dx, dy):
					return 1

	return 0

def inRadius1(wrld, character):
	radius = [-1, 0, 1]

	for i in range(len(radius)):
		for j in range(len(radius)):
			dx = character.x + radius[i]
			dy = character.y + radius[j]

			if __inWorld(wrld, dx, dy) is True:
				if wrld.monsters_at(dx, dy):
					return 1

	return 0

def inRadius3(wrld, character):
	radius = [-3, 0, 3]

	for i in range(len(radius)):
		for j in range(len(radius)):
			dx = character.x + radius[i]
			dy = character.y + radius[j]

			if __inWorld(wrld, dx, dy) is True:
				if wrld.monsters_at(dx, dy):
					return 1

	return 0

def monsterToBomb(wrld, character):
	monsters = findAll(wrld, 2)
	bombs = findAll(wrld, 1)

	if len(monsters) == 0 or len(bombs) == 0:
		return 0

	# assumes only one bomb at a time
	pos = (bombs[0][0], bombs[0][1])

	nearest_monster = findNearestEntity(wrld, pos, monsters)

	distance = float(perform_a_star(wrld, pos, nearest_monster))

	return (1 / (distance + 1)) ** 2
	

def monsterToNearestWall(wrld, character):
	monsters = findAll(wrld, 2)
	walls = findAll(wrld, 3)
	 
	if len(monsters) == 0 or len(walls) == 0:
		return 0

	nearest_wall = findNearestEntity(wrld, (character.x, character.y), walls)
	pos = (nearest_wall[0], nearest_wall[1]) 	
 
	distance = float(perform_a_star(wrld, pos, nearest_wall))
	return (1 / (distance + 1)) ** 2


def bomb_to_wall(wrld,character):
	bombs = findAll(wrld, 1)
	walls = findAll(wrld, 3)

	if len(walls) == 0:
		return 0

	if len(bombs) == 0:
		return 0

	pos = (bombs[0][0], bombs[0][1])

	nearest_wall = findNearestEntity(wrld, pos, walls)
	
	distance = float(perform_a_star(wrld, pos, nearest_wall))

	return (1 / (distance + 1)) ** 2



def anyMonsters(wrld, character):
	monsters = findAll(wrld, 2)
	
	if len(monsters) < 2:
		return 1
	
	return 0


def distanceToWall(wrld, character):
	walls = findAll(wrld, 3)
	
	if len(walls) == 0:
		return 0

	for i in walls:
		xPos, yPos = i[0], i[1]
  
		if character.y - yPos < 0:
			walls.remove(i)
 
	pos = (character.x, character.y)
	nearest_wall = findNearestEntity(wrld, pos, walls)
	distance = float(perform_a_star(wrld, pos, nearest_wall))

	return (1 / (distance + 1))

def distanceBetweenMonsters(wrld, character):
    monsters = findAll(wrld, 2)
    
    if len(monsters) < 2:
        return 0
    
    monster1 = monsters[0][0]
    monster2 = monsters[0][1]
    
    distance = float(perform_a_star(wrld, monster1, monster2))
    
    return (1 / (distance+1)) ** 2

def bombTimer(wrld, character):
	bombs = findAll(wrld, 1)

	if len(bombs) == 0:
		return 0

	pos = (character.x, character.y)
	nearest_bomb = findNearestEntity(wrld, pos, bombs)

	bombEntity = wrld.bomb_at(nearest_bomb[0], nearest_bomb[1])

	return (1 / float(bombEntity.timer + 1)) ** 2


def bombDestroysWall(wrld, character):
	explosions = findAll(wrld, 4)
	walls = findAll(wrld, 3)

	if len(explosions) == 0:
		return 0

	for explosion in explosions:
		x, y = explosion[0], explosion[0]

		if wrld.wall_at(x, y):
			return 1

	return 0

def allWall(wrld, character):
	walls = findAll(wrld, 3)

	if len(walls) == 0:
		return 0

	pos = (character.x, character.y)

	nearest_wall = findNearestEntity(wrld, pos, walls)

	row = nearest_wall[1]
	count = 0

	for x in range(wrld.width()):
		if wrld.wall_at(x, row):
			count += 1

	return (count / 8)



