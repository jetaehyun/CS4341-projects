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
		self.count = 0
		self.iterations = 0
		self.pastMoves = []
		self.qLearning = False
		self.bomb = False


	def do(self, wrld):
		
		if self.safeCondition(wrld):
			self.qLearning = True
			if foundBomb(wrld):
				x, y = bomb_handler(wrld, (self.x, self.y), (0, 0))

				self.move(x, y)

			elif explosion_occurring(wrld) is True:
				x, y = explosion_handler(wrld, (1, -1))

				if explosion_will_occur(wrld, (self.x,self.y)) is True:
					self.move(0,0)
     
				else:
					self.move(x,y)
     
			elif wallInPath(wrld, (self.x, self.y), (0, 1)):
				self.place_bomb()
				x = random.choice([-1, 1])
				self.move(x, 1)

			elif allMonstersDead(wrld) or safePathToExitWithMonster(wrld, (self.x, self.y)):
				self.a_star(wrld)

			elif monsterPastCharacter(wrld, (self.x, self.y)) is True:
				goTo = perform_aStar(wrld, (self.x, self.y), lastWall(wrld, (self.x, self.y)), False)
				self.move(goTo[0], goTo[1])
    
			else:
				self.move(0, 1)

		else:
			self.qLearning = True
			self.perform_qLearning(wrld)
			'''
			if characterInWallRow(wrld, (self.x, self.y)):
				self.place_bomb()
				# directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
				# for i in directions:
				# 	if can_move(wrld, (self.x,self.y), i) and wrld.wall_at(self.x+i[0],self.y+i[1]) is None:
				# 		self.move(i[0], i[1])
				if can_move(wrld, (self.x, self.y), (1,1)) is True:
					self.move(1,1)
				elif can_move(wrld, (self.x,self.y), (-1,1)) is True:
					self.move(-1,1)
				# self.move(0, -1)

			else:
				self.qLearning = True
				self.perform_qLearning(wrld)
			'''


	def safeCondition(self, wrld):
		result = allMonstersTrapped(wrld)

		monsters = findAll(wrld, 2)

		if len(monsters) == 0:
			return True 

		pos = (self.x, self.y)

		nearest_monster_tuple = findNearestEntity(wrld, pos, monsters)

		distance = float(perform_a_star(wrld, pos, nearest_monster_tuple)) + 1


		if distance >= 15:
			return True

		return False
		'''
		if distance > 20 and result is False:
			return True

		if result is False:
      
			if monsterPastCharacter(wrld, (self.x, self.y)):
				return True
			
			monsters = findAll(wrld, 2)
			pos = (self.x, self.y)

			nearest_monster_tuple = findNearestEntity(wrld, pos, monsters)

			distance = len(perform_aStar(wrld, pos, nearest_monster_tuple, True))
	
			if distance == 0:
				return True
   
			nearest_monster = wrld.monsters_at(nearest_monster_tuple[0], nearest_monster_tuple[1])[0]

<<<<<<< HEAD
			if nearest_monster.name != "aggressive":
				if distance > 2:
					return True

			else:
				if distance >= 6:
					return True
=======
			if distance > 10:
				return True
				
>>>>>>> 876d9720fb054fbba1537ed06bbc8211ff66dac7

			return False 

		return True
		'''


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
	def a_star(self, wrld):
		search = perform_aStar(wrld, (self.x, self.y), self.get_exit_location(wrld), False)

		if len(search) == 0:
			self.move(0, 1)
			return

		self.move(search[0], search[1])


	def get_exit_location(self, wrld):
		for w in range(wrld.width()):
			for h in range(wrld.height()):
				if wrld.exit_at(w, h):
					return (w, h)




