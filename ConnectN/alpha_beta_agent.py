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

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""

        best_move_score = 0
        best_state = (None, None)

        for i in range(0, self.max_depth, 1):
        	(board, move_score) = self.__min_value(brd, i, float("-inf"), float("inf"))

        	if move_score >= float('inf'):
        		return 1 

        	elif move_score <= float('-inf'):
        		return 1 


        	if move_score > best_move_score:
        		best_move_score = move_score
        		best_state = board 

        	else:
        		best_state = board 

        return best_state

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
    		return brd, 1
    		
    	for state in self.get_successors(brd):
    		(board, move_score) = self.__min_value(state[0], depth-1, alpha, beta)

    		if move_score < max_move_score:
    			max_move_score = move_score
    			max_board = state 

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
    		return brd, 1

    	for state in self.get_successors(brd):
    		(board, move_score) = self.__max_value(state[0], depth-1, alpha, beta)

    		if move_score < min_move_score:
    			min_move_score = move_score
    			min_board = state 

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
