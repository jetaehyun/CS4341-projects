# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity
from sensed_world import SensedWorld
from real_world import RealWorld
from events import Event
import QLearner
from features import *
from patrick_star import _aStar, perform_aStar

class QCharacter(CharacterEntity):

	def __init__(self, name, avatar, x, y, q_learner, train, iteration, stateMachine=False):
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
		self.identity = "A-Star"
		self.stateMachine = stateMachine


	def do(self, wrld):

		self.prev_wrld = SensedWorld.from_world(wrld)
		self.identity = "A-Star"

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
				exploringFlag = False
				maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

				x, y, place_bomb = best_action

				self.move(x, y)

				if place_bomb is True:
					self.place_bomb()
			

			
		else:
			# use the converged values 

			if self.stateMachine is True:
				if self.anyMonstersInLineOfSight(wrld, self.x, self.y) is True:
					if self.identity == "A-Star":
						self.identity = "Q-Learning"

				if self.identity == "A-Star":
					self.seek_path(wrld)
					return


			maxQ, best_action, best_wrld = self.q_learner.getBestMove(wrld, self)

			x, y, place_bomb = best_action
			if self.iterations == 20:
				self.pastMoves = []
				self.count = 0
				self.iterations = 0


			dx = self.x + x 
			dy = self.y + y 

			if (dx, dy) in self.pastMoves:
				self.count += 1

			else:
				self.pastMoves.append((dx, dy))


			if self.count == 10:
				self.count = 0
				self.pastMoves = []
				y = 1

				x, y = self.bomb_handler(wrld, x, y)
				x, y = self.explosion_handler(wrld, x, y)

			self.move(x, y)
			self.iterations += 1



			if place_bomb is True:
				self.place_bomb()

	# --------------------------------------------------------------------------
	##
	# @Brief performs the a star search to the the exit
	#
	# @Param wrld world object
	#
	# @Returns None
	# --------------------------------------------------------------------------  	
	def seek_path(self, wrld):
		search = perform_aStar(wrld, (self.x, self.y), self.get_exit_location(wrld), False)

		if search == None:
			return

		self.move(search[0], search[1])


	def get_exit_location(self, wrld):
		for w in range(wrld.width()):
			for h in range(wrld.height()):
				if wrld.exit_at(w, h):
					return (w, h)


	def anyMonstersInLineOfSight(self, wrld, x, y):
		monsters = findAll(wrld, 2)

		if len(monsters) == 0: 
			return False

		pos = (x, y)

		nearest_monster = findNearestEntity(wrld, pos, monsters)

		distance = float(perform_a_star(wrld, pos, nearest_monster))

		if distance <= 20:
			return True

		return False

	def updateCharacterWeights(self, wrld, win, lose):
		reward = 0

		if self.train is True:	
			if win is True:
				reward = 100

			elif lose is True:
				reward = -50

			else:
				pos = (self.x, self.y)
				reward = (((distanceToExit(wrld, self)** 0.1) * 10) - ((distanceToMonster(wrld, self)** 0.1) * 5)) - ((self.world_timer(wrld) ** 0.1))

			self.q_learner.updateWeights(self, self.prev_wrld, wrld, reward)


	def world_timer(self, wrld):

		world_timer = wrld.time + 1

		return (1 / world_timer) ** 2


	def can_move(self, wrld, x, y):
		dx = self.x + x 
		dy = self.y + y
		if dx < 0 or dx >= wrld.width():
			return False 

		if dy < 0 or dy >= wrld.height():
			return False 

		if wrld.wall_at(dx, dy) is True:
			return False

		return True



	def find_all_bombs(self, wrld):
		bombs = []

		for x in range(wrld.width()):
			for y in range(wrld.height()):
				if wrld.bomb_at(x, y) is not None:
					bombs.append((x,y))

		return bombs


	def bomb_handler(self, wrld, x, y):
		for bomb in self.find_all_bombs(wrld):
			#print('FOUND BOMB')
			dx = self.x + x 
			dy = self.y + y

			#print(f'BX: {bomb[0]}, BY: {bomb[1]}')
			#print(f'DX: {dx}, DY: {dy}')
			escape_directions = [-1, 1] 

			if dx == bomb[0]:
				#print('DX:', dx)
				#print('BOMB_X:', bomb[0])
				#print("FOUND IN COLUMN\n")
				'''
				if abs(bomb[1] - dy) > 4:
					pass
				'''
				x = escape_directions[random.randint(0, 1)] if x == 0 else (x * -1)

				#print(f'RANDOM X: {x}')
				if self.can_move(self.prev_wrld, x, y) is False:
					x = 0

			if dy == bomb[1]:
				#print('DY:', dy)
				#print('BOMB_Y:', bomb[1])
				#print("FOUND IN ROW\n")
				'''
				if abs(bomb[1] - dy) > 4:
					continue 
				'''

				y = escape_directions[random.randint(0, 1)] if y == 0 else (y * -1)
				#print(f'RANDOM y: {y}')
				if self.can_move(self.prev_wrld, x, y) is False:
					y = 0

		return x, y

	def explosion_occurring(self, wrld):
		for x in range(wrld.width()):
			for y in range(wrld.height()):
				if wrld.explosion_at(x, y) is not None:
					return True 

		return False

	def explosion_handler(self, wrld, x, y):
		if self.explosion_occurring(wrld) is True:
			return (0, 0)

		return x, y

			



