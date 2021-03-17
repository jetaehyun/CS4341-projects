# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity
from sensed_world import SensedWorld
from real_world import RealWorld
from events import Event
import QLearner

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
			print('NOT SAFE')
			input()
			self.move(0, 0)

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


	def safeCondition(self, wrld):
		result = allMonstersTrapped(wrld)
		print('TRAPPED:', result)
		return allMonstersTrapped(wrld)

		



