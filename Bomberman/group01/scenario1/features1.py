from patrick_star import perform_aStar, _heuristic

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
def findNearestEntity(wrld, character, entity):
	x,y = character.x, character.y
	width,height = wrld.width(), wrld.height()
	
	distanceTo = 99999
	coord = None

	for w in range(width):
		for h in range(height):
			distanceToFound = 99999
			if entity == "monster":
				if wrld.monsters_at(w, h) is not None:
					distanceToFound = _heuristic((w,h), (x,y))

			elif entity == "bomb":
				if wrld.bomb_at(w,h) is not None:
					distanceToFound = _heuristic((w,h), (x,y))

			elif entity == "exit":
				if wrld.exit_at(w,h):
					return (w,h)

			if distanceToFound<distanceTo:
				distanceTo = distanceToFound
				coord = (w,h)

	return coord


def getListOfMonsters(wrld):

    monsterList = []
    width, height = wrld.width(), wrld.height()

    for w in range(width):
        for h in range(height):
            if wrld.monsters_at(w,h) is not None:
                monsterList.append((w,h))

    return monsterList

def getPathToClosestMonster(wrld, character):

    monsterList = getListOfMonsters(wrld)
    x,y = character.x, character.y

    if len(monsterList) == 0:
        return 0

    shortestPath = 99999
    coord = (0,0)

    for pos in monsterList:
        xPos, yPos = pos[0], pos[1]
        dist = _heuristic(pos, (xPos,yPos))

        if dist<shortestPath:
            shortestPath = dist
            coord = (xPos, yPos)
    pos = (character.x,character.y)
    path = perform_aStar(wrld, pos, coord, True)
    return (1 / (1+len(path))**2)
    
	
def distanceToExit(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "exit")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition, True)
	distance = float(len(path)) if path is not None else 0
	return 1-(1 / (1+distance)**2)


def distanceToBomb(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "bomb")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition, True)
	distance = float(len(path)) if path is not None else 0
	return 1-(1 / (1+distance)**2)



def distanceToMonster(wrld, character):
	entityPosition = findNearestEntity(wrld, character, "monster")

	if entityPosition == None:
		return 0

	pos = (character.x, character.y)
	path = perform_aStar(wrld, pos, entityPosition, True)
	distance = float(len(path)) if path is not None else 0
	return 1 / (1+distance)**2



def inBombExplosionRange(wrld, character):
   
	for i in range(3):
		if wrld.me(character) is None:
			return 1

		if wrld.explosion_at(character.x, character.y) is not None:
			return 1

		wlrd, events = wrld.next()

	return 0
