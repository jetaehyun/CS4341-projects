# This is necessary to find the main code
import sys, random
sys.path.insert(0, '../bomberman')

class QCharacter(CharacterEntity):

	def __init__(self, name, avatar, x, y, q_learner, train, iteration, max_iteration):
        CharacterEntity.__init__(self, name, avatar, x, y)

        self.q_learner = q_learner
        self.train = train
        self.iteration = iteration 
        self.max_iteration = max_iteration

        self.epsilon = (1 / (iteration + 1)) ** 0.1


    def do(self, wrld):

    	if self.train is True:
    		if random.random() < self.epsilon:
    			# choose random move
    			allowed_direction = [-1, 0, 1]
    			bomb_actions = [False, True]

    			direction_x = allowed_direction[random.randint(0, 2)]
    			direction_y = allowed_direction[random.randint(0, 2)]
    			place_bomb = bombactions[random.randint(0, 1)]

    			x = direction_x
    			y = direction_y if x == 0 else 0

    			if place_bomb is True:
    				self.place_bomb()

    			self.move(x, y)

    		else:
    			maxQ, best_action = self.q_learner.getBestMove(wrld, self)

    			x, y, bomb = best_action

    			if bomb is True:
    				self.place_bomb()

    			self.move(x, y)

    	else:
    		# use the converged values 
    		
    		maxQ, best_action = self.q_learner.getBestMove(wrld, self)

    		x, y, bomb = best_action

    		if bomb is True:
    			self.place_bomb()

    		self.move(x, y)


