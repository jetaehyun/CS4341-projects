# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

from sensed_world import SensedWorld
from events import Event

ALPHA = 0.2
GAMMA = 0.8

###
# Class Description: defining blueprint for an object to perform Q-Learning using Feature Representation
###
class QLearner:
	def __init__(self, weights, features):
		self.weights = weights
		self.features = features 

		if self.weights is None:
			self.weights = [0] * len(self.features)	# all weights start with 0

		# tuple - (x, y, placeBomb?)
		self.available_moves = [
			(0, 0, False), (0, 1, False), (0, -1, False),
			(0, 0, True), (0, 1, True), (0, -1, True),
			(1, 0, False), (1, 1, False), (1, -1, False),
			(-1, 0, True), (-1, 1, True), (-1, -1, True)
		]

	# --------------------------------------------------------------------------
	##
	# @Brief - performs all possible moves at the character's current state and
	#		   determining the best Q value and best action
	#
	# @Param - wrld: world object
	# @Param - character: charcter object
	#
	# @Returns (max q value, best action move)
	# -------------------------------------------------------------------------- 
	def getBestMove(self, wrld, character):
		maxQ = float('-inf')

		best_action = (0, 0, False)
		best_wrld = wrld 

		for move in self.available_moves:
			my_wrld = SensedWorld.from_world(wrld) # creates a copy of the current world state

			# check if character in the world right now
			if my_wrld.me(character) is None:
				continue

			x = move[0]
			y = move[1]
			place_bomb = move[2]

			my_wrld.me(character).move(x, y)

			if place_bomb is True:
				my_wrld.me(character).place_bomb()

			next_wrld, next_events = my_wrld.next()	# now see the results of the move taken

			curr_q = float('-inf')

			if next_wrld.me(character) is not None:
				curr_q = self.Q_Function(next_wrld, my_wrld.me(character))

			else:
				# either character just died or exited 
				for event in next_events:
					if event.tpe == Event.BOMB_HIT_CHARACTER or event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
						#print('CHARACTETR DIED')
						curr_q = float('-inf')


					elif event.tpe == Event.CHARACTER_FOUND_EXIT:
						curr_q = float('inf')

			if curr_q > maxQ:
				maxQ = curr_q
				best_action = move 
				best_wrld = next_wrld

		return (maxQ, best_action, best_wrld)

	# --------------------------------------------------------------------------
	##
	# @Brief - perfoms the Q-Function with Feature Representation
	#
	# @Param - wrld: world object
	#
	# @Returns totalSum - the total sum of the weights * feature (aka value of Q(s, a))
	# -------------------------------------------------------------------------- 
	def Q_Function(self, wrld, character):
		totalSum = 0

		for i in range(len(self.features)):
			w = self.weights[i]	# corresponding weight for the current feature

			totalSum += (w * self.features[i](wrld, character))
	
		return totalSum


	# --------------------------------------------------------------------------
	##
	# @Brief - updates the weights by following the algorithm for Approximate Q-Learning
	#
	# @Param - wrld: world object
	# @Param - prime_wrld: the next world object
	# @Param - r - the reward
	#
	# @Returns totalSum - the total sum of the weights * feature (aka value of Q(s, a))
	# -------------------------------------------------------------------------- 
	def updateWeights(self, character, wrld, r):

		delta = r - self.Q_Function(wrld, character)

		for i in range(len(self.features)):
			self.weights[i] += (ALPHA * delta * self.features[i](wrld, character))