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


class StateCharacter(CharacterEntity):

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


	def do(self, wrld):
		
		if self.safeCondition(wrld) is True:
			self.qLearning = False
			if foundBomb(wrld):
				x, y = bomb_handler(wrld, (self.x, self.y), (0, 0))

				self.move(x, y)

			elif explosion_occurring(wrld) is True:
				x, y = explosion_handler(wrld, (-1, 1))

				self.move(x, y)

			elif wallInPath(wrld, (self.x, self.y), (0, 1)):
				self.place_bomb()
				self.move(1, -1)

			else:
				self.move(0, 1)

		else:
			self.qLearning = True
			self.perform_qLearning(wrld)


	def safeCondition(self, wrld):
		result = allMonstersTrapped(wrld)
		return allMonstersTrapped(wrld)


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
				reward = -50

			else:
				pos = (self.x, self.y)
				reward = (((distanceToExit(wrld, self)** 0.1) * 10) - ((distanceToMonster(wrld, self)** 0.1) * 5)) #- ((self.world_timer(wrld) ** 0.1))

			self.q_learner.updateWeights(self, self.prev_wrld, wrld, reward)

		



