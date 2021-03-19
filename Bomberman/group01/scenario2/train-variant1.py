# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster
from sensed_world import SensedWorld

# TODO This is your code!
sys.path.insert(1, '../group01')

# Uncomment this if you want the empty test character
from StateCharacter1 import StateCharacter1


numOfWins = 0
for i in range(0, 10):
	print('Iteration #', i)

	# Create the game
	g = Game.fromfile('map.txt')

	# TODO Add your character

	state_character = StateCharacter1("me", # name
                              "C",  # avatar
                              0, 0,
                  		)

	#Uncomment this if you want the interactive character
	g.add_character(state_character)

	g.go(1)
	print(g.world.scores["me"])
	wrld = SensedWorld.from_world(g.world)
	#q_character.updateCharacterWeights(wrld, False, True)
	score = g.world.scores["me"]
	if score > 400:
		numOfWins += 1
	print(f'WIN PERCENTAGE: {numOfWins / (i+1)}')



