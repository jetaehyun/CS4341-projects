from patrick_star import perform_aStar, _heuristic

# --------------------------------------------------------------------------
##
# @Brief find the nearest entity to the character
#
# @Param wrld world object
# @Param character position of character (x,y)
# @Param entity desired entity to find
#
# @Returns None: nothing found, list(): of positions
# --------------------------------------------------------------------------
def findNearestEntity(wrld, character, entity):
	x,y = character.x, character.y
	width,height = wrld.width(), wrld.height()
	
	distanceTo = 99999
	coord = None

	for w in range(width):
		for h in range(height):
			distanceToFound = 99999
			if entity == "monster":
				if wrld.monsters_at(w, h) != None:
					distanceToFound = _heuristic((w,h), (x,y))

			elif entity == "bomb":
				if wrld.bomb_at(w,h) != None:
					distanceToFound = _heuristic((w,h), (x,y))

			elif entity == "exit":
				if wrld.exit_at(w,h):
					return (w,h)

			if distanceToFound<distanceTo:
				distanceTo = distanceToFound
				coord = (w,h)

	return coord


	
def distanceToExit(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "exit")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition)
	distance = float(len(path))
	return 1 / (1+distance)**2


def distanceToBomb(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "bomb")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition)
	distance = float(len(path))
	return 1 / (1+distance)**2



def distanceToMonster(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "exit")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition)
	distance = float(len(path))
	return 1 / (1+distance)**2



def inBombExplosionRange(wrld, character):
   
	for i in range(3):
		if wrld.me(character) is None:
			return 1

		if wrld.explosion_at(character.x, character.y) is not None:
			return 1

		wlrd, events = wrld.next()

	return 0
