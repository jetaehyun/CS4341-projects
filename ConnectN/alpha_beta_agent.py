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

        possible_moves = self.get_successors(brd)
        max_node = float("-inf") # negative infinity 
        best_state = None
        dic = {}
        for state in possible_moves:
            #found_min_node = find_min_node()
            found_min_node = 1
            if found_min_node > max_node:
                max_node = found_min_node
                best_state = state

        next_move = best_state[1]
        return next_move

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

        player = brd.player

        for width in range(brd.w):
            for height in range(brd.h):
                
                token = brd.board[width][height]

                # if checking player
                if token == player:

                    for vertical in range(brd.n):

                    for horizontal in range(brd.n):

                    for diagonalPos in range(brd.n):

                    for diagonalNeg in range(brd.n):


    def __diagonalNeg(self, brd, x, y):
        
        points = 0
        duplicates = 1
        player = brd.player

        for diag in range(brd.n):
            
            xPos = x + diag
            yPos = y - diag

            if xPos >= brd.w - 1 and yPos < 0:
                break
            
            token = brd.board[xPos][yPos]
            if token == player:
                points += 2 * duplicates
                duplicates += 1

        return points


    def __diagonalPos(self, brd, x, y):
        
        points = 0
        duplicates = 1
        player = brd.player

        for diag in range(brd.n):

            xPos = x + diag
            yPos = y + diag

            if xPos >= brd.w - 1 and yPos >= brd.h - 1:
                break
            
            token = brd.board[x+diag][y+diag]
            if token == player:
                points += 2 * duplicates
                duplicates += 1

        return points

    def __countVertical(self, brd, x, y):
        
        points = 0
        duplicates = 1
        player = brd.player

        for vert in range(brd.n):
            if vert >= brd.h - 1:
                break
            
            token = brd.board[x][y+vert]
            if token == player:
                points += 2 * duplicates
                duplicates += 1

        return points

    def __countHorizontal(self, brd, x, y):
        points = 0
        duplicates = 1
        player = brd.player

        for hor in range(brd.n):
            if hor >= brd.w - 1:
                break
            
            token = brd.board[x+hori][y]
            if token == player:
                points += 2 * duplicates
                duplicates += 1

        return points





















