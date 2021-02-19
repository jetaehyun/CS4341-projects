import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth


    def inBoard(self, brd, w, h):
    	if h >= 0 and h < brd.h:
    		if w >= 0 and w < brd.w:
    			return True 

    	return False

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""

        best_move_score = 0
        # best_state = (board, token)
        best_state = (None, None)

        for i in range(0, self.max_depth, 1):
        	(board, move_score) = self.__min_value(brd, i, float("-inf"), float("inf"))

        	if move_score > best_move_score:
        		best_move_score = move_score
        		best_state = board 

        	else:
        		best_state = board 

        return best_state[1] #if best_state is not None else random.choice(brd.free_cols)

    # Find the board state that has the maximum value 
    #
    # PARAM [board.Board] successor_states: the successor board 
    # PARAM [int] my_depth: the current depth where this function is called
    # PARAM [int] alpha: the current alpha value
    # PARAM [int] beta: the current beta value
    def __max_value(self, brd, depth, alpha, beta):
    	max_move_score = float("-inf")
    	max_board = None 

    	if self.__terminal_test(depth):
    		return None, self.__heuristic(brd)
    		
    	for state in self.get_successors(brd):
    		(board, move_score) = self.__min_value(state[0], depth-1, alpha, beta)

    		if move_score > max_move_score:
    			max_board, max_move_score = state, move_score

    		if move_score >= beta:
    			break

    		if move_score >= alpha:
    			alpha = move_score

    	return (max_board, max_move_score)

    # Find the board state that has the minimum value 
    #
    # PARAM [board.Board] successor_states: the successor board 
    # PARAM [int] my_depth: the current depth where this function is called
    # PARAM [int] alpha: the current alpha value
    # PARAM [int] beta: the current beta value
    def __min_value(self, brd, depth, alpha, beta):
    	min_move_score = float("inf")
    	min_board = None 

    	if self.__terminal_test(depth):
            return None, self.__heuristic(brd)

    	for state in self.get_successors(brd):
    		(board, move_score) = self.__max_value(state[0], depth-1, alpha, beta)

    		if move_score < min_move_score:
    			min_board, min_move_score = state, move_score

    		if move_score <= alpha:
    			break

    		if move_score <= beta:
    			beta = move_score

    	return (min_board, min_move_score)


    def __terminal_test(self, depth):
    	if depth == 0:
    		return True

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    # TODO: 
    # 1) Check if there is a block
    # 2) Subtract value on a block (e.g. is there a player? Is there a hole in a sequence?)
    # 3) Add value if there is a hole
    # 4) Find best heuristic equation to use

    # ---------------------------------------------------------------------------------
    ##
    # @Brief calculates the heuristic value of the board
    #
    # @Param brd board to be checked
    #
    # @return value of board
    # ---------------------------------------------------------------------------------

    def __heuristic(self, brd):
        
        # linear: 2n  -> 1: 2 | 2: 4 
        # Square: n^2 -> 1: 1 | 2: 4

        valuePlayer, valueEnemy = 0, 0

        for height in range(brd.h):
            for width in range(brd.w):
                
                value = 0
                token = brd.board[height][width]
                # check correct player
                diagNeg = self.__calcTokens(brd, token, width, height, 1, -1)
                diagPos = self.__calcTokens(brd, token, width, height, 1, 1)
                vert = self.__calcTokens(brd, token, width, height, 0, 1)
                hor = self.__calcTokens(brd, token, width, height, 1, 0)


                value += diagNeg + diagPos + vert +  hor

                if token == 0 or token == brd.player:
                    valuePlayer += value
                else:
                    valueEnemy += value
                    
        #print(valuePlayer - valueEnemy)
        print("PV: " + str(valuePlayer))
        print("EV" + str(valueEnemy))
        return valuePlayer - valueEnemy

    def __calcTokens(self, brd, playerPersp, width, height, dh, dw):
        points, duplicates = 0, 1
        player = brd.player

        for direction in range(brd.n):
            wPos = width + (direction * dw)
            hPos = height + (direction * dh)

            if self.inBoard(brd, wPos, hPos) is False:
                return points

            token = brd.board[hPos][wPos]

            if player == playerPersp: # gather points for the player we want to win
                if token == player or token == 0:
                    if token == player:
                        points += 2 ** duplicates
                        duplicates += 1

                else:
                    return 0 # not possible to win
            else: # gather points for enemy player
                if token != player or token == 0:
                    if token!= player and token !=0:
                        points += 2 ** duplicates
                        duplicates += 1
                        if(duplicates == brd.n):
                            points = points + 10000000
                else:
                    return 0


        return points




