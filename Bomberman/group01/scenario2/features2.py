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

	nearest_exit = findNearestEntity(wrld, character, exit)

	pos = (character.x, character.y)
	distance = float(perform_a_star(wrld, pos, nearest_exit))

	return (1 / (distance + 1)) ** 2


def distanceToBomb(wrld, character):
	bombs = findAll(wrld, 1)

	if len(bombs) == 0: 
		return 0

	nearest_bomb = findNearestEntity(wrld, character, bombs)

	pos = (character.x, character.y)
	distance = float(perform_a_star(wrld, pos, nearest_bomb))

	return (1 / (distance + 1)) ** 2


def distanceToMonster(wrld, character):
	monsters = findAll(wrld, 2)

	if len(monsters) == 0: 
		return 0

	nearest_monster = findNearestEntity(wrld, character, monsters)

	pos = (character.x, character.y)
	distance = float(perform_a_star(wrld, pos, nearest_monster))

	return (1 / (distance + 1)) ** 2


	
def inBombExplosionRange(wrld, character):
   
	for i in range(3):
		if wrld.explosion_at(character.x, character.y) is not None:
			return 1

		wrld, events = wrld.next()

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

	nearest_monster = findNearestEntity(wrld, character, monsters)

	monstersEntity = wrld.monsters_at(nearest_monster[0], nearest_monster[1])[0]

	pos = (character.x, character.y)
	distance = float(perform_a_star(wrld, pos, nearest_monster)) + 1

	if monstersEntity.name == "selfpreserving":
		if distance <= 2:
			return ((3 - distance) / 3)

	elif monstersEntity.name == "aggressive":
		if distance <= 4:
			return ((5 - distance) / 5)

	return 0


def total_number_of_walls(wrld,character):
	walls = findAll(wrld,3)

	return (1/(len(walls)+1))**2


def bomb_to_wall(wrld,character):
	distance  = 0
	bombs = findAll(wrld, 1)
	walls = findAll(wrld, 3)

	if len(bombs) == 0 or len(walls) == 0:
		return 0

	nearest_bomb = findNearestEntity(wrld, character, bombs)
	nearest_wall = findNearestEntity(wrld, character, walls)

	pos = (nearest_bomb[0], nearest_bomb[1])
	distance = float(perform_a_star(wrld, pos, nearest_wall))

	return (1 / (distance + 1)) ** 2
