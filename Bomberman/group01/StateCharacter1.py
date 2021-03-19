# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity
from sensed_world import SensedWorld
from real_world import RealWorld
from events import Event
import QLearner

from features import *
from helpers import *
from stateHelpers import *
from patrick_star import _aStar, perform_aStar


class StateCharacter1(CharacterEntity):

	def __init__(self, name, avatar, x, y):
		CharacterEntity.__init__(self, name, avatar, x, y)
  
		self.state = "go"
		self.hasMoved = False
		self.dxdy = (-1, -1)
		self.bomb_locations = [(7, 2, True), (7, 6, True), (7, 10, True), (7, 12, True), (7, 18, False)]
		self.location_index = 0


	def do(self, wrld):
		#print(self.state)
		if self.state == "bomb":
			if self.bomb_locations[self.location_index - 1][2] is True:
				self.place_bomb()

				self.state = "dodge"

			elif wrld.monsters_at(7, 8):
				#print("FOUND")
				self.state = "go"


		elif self.state == "dodge":
			x, y = self.x, self.y

			if self.location_index <= len(self.bomb_locations):
				if self.bomb_locations[self.location_index - 1][2] is False:
					#self.location_index = 5
					self.state = "go"
					return 

			if can_move(wrld, (x,y), self.dxdy) is True:
				self.move(self.dxdy[0], self.dxdy[1])
			else:
				if self.location_index - 1 == 3:
					self.move(-1, 1)
				else:
					self.move(1, -1)

			self.state = "wait"
    
		elif self.state == "go":
			goal = self.bomb_locations[self.location_index]
			goal = (goal[0], goal[1])
			self.a_star(wrld, goal)
   
			if goal[0] == self.x and goal[1] == self.y:
				self.state = "bomb"
				self.location_index += 1
	
		else:

			if foundBomb(wrld) is not True:
				if foundExplosion(wrld) is not True:
					self.state = "go"

			

			else:
				self.move(0,0)
    
     
	def updateCharacterWeights(self, wrld, win, lose):

		return 0


	# --------------------------------------------------------------------------
	##
	# @Brief performs the a star search to the the exit
	#
	# @Param wrld world object
	#
	# @Returns None
	# --------------------------------------------------------------------------  	
	def a_star(self, wrld, dest=None):

		dest = dest if dest is not None else self.get_exit_location(wrld)
		search = perform_aStar(wrld, (self.x, self.y), dest, False)

		if len(search) == 0:
			self.move(0, 1)
			return

		self.move(search[0], search[1])


	def get_exit_location(self, wrld):
		for w in range(wrld.width()):
			for h in range(wrld.height()):
				if wrld.exit_at(w, h):
					return (w, h)




