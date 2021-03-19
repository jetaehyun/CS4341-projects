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


class StateCharacter(CharacterEntity):

	def __init__(self, name, avatar, x, y, q_learner, train, iteration):
		CharacterEntity.__init__(self, name, avatar, x, y)

		self.q_learner = q_learner
		self.train = train
		self.iteration = iteration 

		self.epsilon = 1 / (self.iteration + 1) ** 0.5
		self.prev_wrld = None
		self.best_wrld = None
		self.iterations = 0
		self.qLearning = False
		self.bomb = False
  
		self.state = "go"
		self.dxdy = (-1, -1)
		self.bomb_locations = [(0, 2, True), (0, 3, True),(1, 3, True), (2, 3,True), (3, 3, True),(4, 3, True),(5, 3, True), (7, 3, True), (7, 10, True), (4, 9, False), (7, 12, True), (7, 18, False)]
		self.location_index = 0


	def do(self, wrld):
     
		monsters = findAll(wrld, 2)
		distance = 0
		nearest_monster = "nothing"
  
		if len(monsters) > 0:
			monster = findNearestEntity(wrld, (self.x,self.y), monsters)
			distance = len(perform_aStar(wrld, (self.x,self.y), (monster[0], monster[1]), True))
			nearest_monster = wrld.monsters_at(monster[0], monster[1])[0]
   
			# print(distance)
			if distance <= 2 and distance > 0 and nearest_monster.name != "aggressive":
				self.state = "qlearn"
   
   
		# print(self.state)
		if self.state == "bomb":
			if self.bomb_locations[self.location_index - 1][2] is True:
				self.place_bomb()
				self.state = "dodge"

			elif wrld.monsters_at(7, 8) or len(monsters) == 0:
				self.location_index = len(self.bomb_locations) - 1       
				self.state = "go"


		elif self.state == "dodge":
			x, y = self.x, self.y

			if self.location_index <= len(self.bomb_locations):
				if self.bomb_locations[self.location_index - 1][2] is False:
					#self.location_index = 5
					self.state = "go"
					return 

			if can_move(wrld, (x,y), self.dxdy) is True:
				if self.x >= wrld.width() - 1:
					self.move(-1, -1)
				else:
					self.move(1, self.dxdy[1])
    
			else:
				
				if self.location_index - 1 == 10:
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
	
		elif self.state == "wait":
    
			if foundBomb(wrld) is not True:
				if foundExplosion(wrld) is not True:
					self.state = "go"
			else:
				self.move(0,0)
		else:
			if (distance > 3 or distance == 0) and self.qLearning is True:
				if self.location_index != 0:
					self.location_index -= 1
     
				self.state = "go"
				self.qLearning = False
				return

			self.qLearning = True
			self.perform_qLearning(wrld)
    
    
	def perform_qLearning(self, wrld):
		self.prev_wrld = SensedWorld.from_world(wrld)

		if self.train is True:
			exploringFlag = False
			best_wrld = None
			if random.random() < self.epsilon:
				exploringFlag = True
				# choose random move
				allowed_direction = [-1, 0, 1]
				bomb_actions = [False, True]

				x = random.choice(allowed_direction)
				y = random.choice(allowed_direction)
				place_bomb = random.choice(bomb_actions)

				x, y = bomb_handler(wrld, (self.x, self.y), (x, y))
				#x, y = explosion_handler2(wrld, (self.x, self.y), (x, y))

				self.move(x, y)

				if place_bomb is True:
					self.place_bomb()

				

			else:
				maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

				x, y, place_bomb = best_action

				self.move(x, y)

				if place_bomb is True:
					self.place_bomb()
			

			
		else:
			# use the converged values 

			maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

			x, y, place_bomb = best_action


			self.move(x, y)

			if place_bomb is True:
				self.place_bomb()

	def updateCharacterWeights(self, wrld, win, lose):
		reward = 0

		if self.train is True and self.qLearning is True:	
			if win is True:
				reward = 100

			elif lose is True:
				reward = -500

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
			if self.location_index != 0:
				self.location_index -= 1
			self.state = "go"
			return

		self.move(search[0], search[1])


	def get_exit_location(self, wrld):
		for w in range(wrld.width()):
			for h in range(wrld.height()):
				if wrld.exit_at(w, h):
					return (w, h)




