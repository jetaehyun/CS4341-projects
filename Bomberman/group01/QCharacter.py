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

		self.epsilon = (1 / (iteration + 1)) ** 0.5
		self.prev_wrld = None


	def do(self, wrld):
		self.prev_wrld = SensedWorld.from_world(wrld)

		if self.train is True:
			if random.random() < 0.2:
				# choose random move
				allowed_direction = [-1, 0, 1]
				bomb_actions = [False, True]

				direction_x = allowed_direction[random.randint(0, 2)]
				direction_y = allowed_direction[random.randint(0, 2)]
				place_bomb = bomb_actions[random.randint(0, 1)]

				x = direction_x
				y = direction_y

				for bomb in self.find_all_bombs(self.prev_wrld):
					dx = self.x + x 
					dy = self.y + y

					escape_directions = [-1, 1] 

					print(f'X: {dx}, Y: {dy}')
					print(f'BOMB: X: {bomb[0]}, Y: {bomb[1]}')

					if dx == bomb[0]:
						y = escape_directions[random.randint(0, 1)]

						if self.in_world(self.prev_wrld, x, y) is False:
							y *= -1

					if dy == bomb[1]:
						x = escape_directions[random.randint(0, 1)]

						if self.in_world(self.prev_wrld, x, y) is False:
							x *= -1

				print(f'\nMY MOVE: X:{x}, Y:{y}\n')

				self.move(x, y)

				if place_bomb is True:
					self.place_bomb()

			else:
				maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

				x, y, place_bomb = best_action

				for bomb in self.find_all_bombs(self.prev_wrld):
					dx = self.x + x 
					dy = self.y + y

					escape_directions = [-1, 1] 

					print(f'X: {dx}, Y: {dy}')
					print(f'BOMB: X: {bomb[0]}, Y: {bomb[1]}')

					if dx == bomb[0]:
						y = escape_directions[random.randint(0, 1)]

						if self.in_world(self.prev_wrld, x, y) is False:
							y *= -1

					if dy == bomb[1]:
						x = escape_directions[random.randint(0, 1)]

						if self.in_world(self.prev_wrld, x, y) is False:
							x *= -1

				print(f'\nMY MOVE: X:{x}, Y:{y}\n')

				self.move(x, y)

				if place_bomb is True:
					self.place_bomb()

				self.updateCharacterWeights(best_wrld, False, False)

		else:
			# use the converged values 
			
			maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

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
				reward = -10

			else:
				reward = 5

			self.q_learner.updateWeights(self, self.prev_wrld, wrld, reward)

	def in_world(self, wrld, x, y):
		if x >= 0 and x < wrld.width():
			if y >= 0 and y < wrld.height():
				return True 

		return False 

	def find_all_bombs(self, wrld):
		bombs = []

		for x in range(wrld.width()):
			for y in range(wrld.height()):
				if wrld.bomb_at(x, y) is not None:
					bombs.append((x,y))

		return bombs
			



