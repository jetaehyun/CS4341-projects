# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

import SensedWorld

###
# Class Description: defining blueprint for an object to perform Q-Learning using Feature Representation
###
class QLearner:
	def __init__(self, weights):
		self.weights = weights

		if self.weights is None:
			self.weights = [0] # depending on num of features, all weights start at 0

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

		best_action = None

		for move in self.available_moves:
			my_wrld = SensedWorld.from_world(wrld) # creates a copy of the current world state

			# check if character in the world right now
			if my_wrld.me(character) is None:
				break

			x = move[0]
			y = move[1]
			place_bomb = move[2]

			my_wrld.me(character).move(x, y)

			if place_bomb is True:
				my_wrld.me(character).place_bomb()

			next_wrld, next_events = my_wrld.next()	# now see the results of the move taken

			if my_wrld.me(character) is not None:
				# TODO: calculate the Q value
				q = 0

			else:
				# either character just died or exited 
				# TODO: set q value to proper value depending on situation
				q = 0

			# TODO: check if found a better q value


		return (maxQ, best_action)


	def Q_Function(self):
		totalSum = 0

		# totalSum = (w1 * fcn(s, a)) + (w2 * fcn(s, a)) + ...

		return totalSum