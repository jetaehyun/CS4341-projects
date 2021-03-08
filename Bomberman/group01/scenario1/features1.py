

def distToMonster(wrld, character):
    return 0.4

def distToExit(wrld, character):
    return 0.02

def distToBomb(wrld, character):
    return 0.8

def distToWall(wlrd, character):
    return 0.4

def inBombExplosionRange(wrld, character):
   
    for i in range(3):
    	if wrld.me(character) is None:
    		return 1

    	if wrld.explosion_at(character.x, character.y) is not None:
    		return 1

    	wlrd, events = wrld.next()

    return 0
