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


class StateCharacter4(CharacterEntity):

	def __init__(self, name, avatar, x, y, q_learner, train, iteration):
		CharacterEntity.__init__(self, name, avatar, x, y)

		self.q_learner = q_learner
		self.train = train
		self.iteration = iteration 

		self.epsilon = 1 / (self.iteration + 1) ** 0.5
		self.prev_wrld = None
		self.best_wrld = None
		self.count = 0
		self.iterations = 0
		self.pastMoves = []
		self.qLearning = False
		self.bomb = False

		self.goal = (0, 2, True)
		self.state11 = False

		self.state1 = False 		# blow first wall in first wall row
		self.state1_1 = False
		self.state2 = False 		# blow wall in second wall row 
		self.state3 = False 		# blow wall in third wall row 
		self.state4 = False			# waiting for monster
		self.state5 = False			# place bomb
		self.state6 = False
  
		self.state = "go"
		self.hasMoved = False
		self.dxdy = (-1, -1)
		self.bomb_locations = [(0, 2, True), (7, 2, True), (7, 6, True), (7, 10, True), (4, 9, False), (7, 12, True), (7, 18, False)]
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
				if self.location_index - 1 == 5:
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
    
     
			

		# if self.state1 is False:
		# 	self.perform_state_1(wrld)

		# elif self.state1_1 is False:
		# 	self.perform_state_1_1(wrld)

		# elif self.state2 is False:
		# 	self.perform_state_2(wrld)

		# elif self.state3 is False:
		# 	self.perform_state_3(wrld)

		# else: 
		# 	self.move(0, 0)

	def atGoal(self):
		if self.x == self.goal[0] and self.y == self.goal[1]:
			return True

		return False


	def perform_state_1(self, wrld):

		if self.atGoal() is True:

			if foundBomb(wrld):
				self.move(0, 0)
				return 

			self.place_bomb()
			self.goal = (7, 2, True)
			self.state1 = True

		else:
			dest = (self.goal[0], self.goal[1])
			self.a_star(wrld, dest)


	def perform_state_1_1(self, wrld):
		if self.atGoal() is True:

			if foundBomb(wrld):
				self.move(0, 0)
				return 

			self.place_bomb()
			self.move(-1, -1)
			self.goal = (7, 6, True)
			self.state1_1 = True

		else:
			dest = (self.goal[0], self.goal[1])
			self.a_star(wrld, dest)

			
	def perform_state_2(self, wrld):
		if self.atGoal() is True:

			if foundBomb(wrld):
				self.move(0, 0)
				return 

			self.place_bomb()
			self.move(-1, -1)
			self.goal = (7, 10, True)
			self.state2 = True

		else:
			dest = (self.goal[0], self.goal[1])
			self.a_star(wrld, dest)


	def perform_state_3(self, wrld):
		if self.atGoal() is True:

			if foundBomb(wrld):
				self.move(0, 0)
				return 

			self.place_bomb()
			self.goal = (4, 9, False)
			self.state3 = True

		else:
			dest = (self.goal[0], self.goal[1])
			self.a_star(wrld, dest)



	def updateCharacterWeights(self, wrld, win, lose):
		reward = 0

		if self.train is True and self.qLearning is True:	
			if win is True:
				reward = 100

			elif lose is True:
				reward = -50

			else:
				pos = (self.x, self.y)
				reward = (((distanceToExit(wrld, self)** 0.1) * 10) - ((distanceToMonster(wrld, self)** 0.1) * 5)) #- ((self.world_timer(wrld) ** 0.1))

			self.q_learner.updateWeights(self, self.prev_wrld, wrld, reward)


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




