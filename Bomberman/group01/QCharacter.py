# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity
from sensed_world import SensedWorld
import QLearner

class QCharacter(CharacterEntity):

	def __init__(self, name, avatar, x, y, q_learner, train, iteration):
		CharacterEntity.__init__(self, name, avatar, x, y)

		self.q_learner = q_learner
		self.train = train
		self.iteration = iteration 

		self.epsilon = (1 / (iteration + 1)) ** 0.1
		self.prev_wrld = None


	def do(self, wrld):
		self.prev_wrld = wrld

		if self.train is True:
			if random.random() < self.epsilon:
				# choose random move
				allowed_direction = [-1, 0, 1]
				bomb_actions = [False, True]

				direction_x = allowed_direction[random.randint(0, 2)]
				direction_y = allowed_direction[random.randint(0, 2)]
				place_bomb = bomb_actions[random.randint(0, 1)]

				x = direction_x
				y = direction_y

				if place_bomb is True:
					self.place_bomb()

				self.move(x, y)

			else:
				maxQ, best_action = self.q_learner.getBestMove(wrld, self)

				x, y, place_bomb = best_action

				if place_bomb is True:
					self.place_bomb()

				self.move(x, y)

		else:
			# use the converged values 
			
			maxQ, best_action = self.q_learner.getBestMove(wrld, self)

			x, y, place_bomb = best_action

			if place_bomb is True:
				self.place_bomb()

			self.move(x, y)


	def updateCharacterWeights(self, wrld, won, lost):
		reward = 0

		if self.train is True:
			if won is True:
				reward = 100

			elif lost is True:
				reward = -50

			else:
				reward = 5

			self.q_learner.updateWeights(self.prev_wrld, wrld, reward)
			



