import game_rules, random

###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000
min_value_player = 'o'
max_value_player = 'x'


class Player(object):
    """ This is the player interface that is consumed by the GameManager. """

    def __init__(self, symbol): self.symbol = symbol  # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)

    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):

    # changed the __init__ in order to have access to the depth
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board):
        return 0, 0

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        # call the maximization function
        return self.maximize_value(board, self.depth, self.symbol)[1]

    def maximize_value(self, board, depth, symbol):
        # first step is to get the legal moves for the player
        legal_moves = game_rules.getLegalMoves(board, symbol)
        # check if the depth == 0 or if there are no other legal moves
        if depth == 0 or len(legal_moves) == 0:
            return self.h1(board, symbol), None
        # set the best value move to negative infinity as we are maximizing
        best_move = (NEG_INF, None)
        # run a for loop for all the available collected legal moves for the player
        for i in range(0, len(legal_moves)):
            # try and get the next moves based on the legal move of the loop
            next_moves = game_rules.makeMove(board, legal_moves[i])
            # check if we are maximizing for the max player "x"
            if symbol == max_value_player:
                next_move_value = self.minimize_value(next_moves, depth - 1, min_value_player)[0]
            else:
                next_move_value = self.minimize_value(next_moves, depth - 1, max_value_player)[0]
            # Check if the best move value we already have is less than the next move, if it is we pick it
            # and we also assign it the legal_move it should do and return it
            if best_move[0] < next_move_value:
                best_move = (next_move_value, legal_moves[i])
        return best_move

    # This is the minimization legal function for the player
    def minimize_value(self, board, depth, symbol):
        # first step is to get the legal moves for the player
        legalMoves = game_rules.getLegalMoves(board, symbol)
        # check if the depth == 0 or if there are no other legal moves
        if depth == 0 or len(legalMoves) == 0:
            return self.h1(board, symbol), None
        # set the best value m ove to positive infinity as we are minimizing
        best_move = (POS_INF, None)
        for i in range(len(legalMoves)):
            # try and get the next moves based on the legal move of the loop
            next_moves = game_rules.makeMove(board, legalMoves[i])
            if symbol == max_value_player:
                next_move_value = self.maximize_value(next_moves, depth - 1, min_value_player)[0]
            else:
                next_move_value = self.maximize_value(next_moves, depth - 1, max_value_player)[0]
            # Check if the best move value we already have is more than the next move, if it is we pick it
            # and we also assign it the legal_move it should do and return it
            if best_move[0] > next_move_value:
                best_move = (next_move_value, legalMoves[i])
        return best_move


# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    # again changed the __init__ in order to have access to the depth
    def __init__(self, symbol, depth):
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board):
        return 0, 0

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        return self.AlphaBetaSearch(board)[1]

    def AlphaBetaSearch(self, board):
        return self.maximize_value(board, NEG_INF, POS_INF, self.depth, self.symbol)

    def maximize_value(self, board, a, b, depth, symbol):
        # first step is to get the legal moves for the player
        legalMoves = game_rules.getLegalMoves(board, symbol)
        # check if the depth == 0 or if there are no other legal moves
        if len(legalMoves) == 0 or depth == 0:
            # just return the heuristic result
            return self.h1(board, symbol), None
        # set the best value move to negative infinity as we are maximizing
        best_move = (NEG_INF, None)
        for i in range(len(legalMoves)):
            # try and get the next moves based on the legal move of the loop
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == max_value_player:
                next_move_value = self.minimize_value(nextBoard, a, b, depth - 1, min_value_player)[0]
            else:
                next_move_value = self.minimize_value(nextBoard, a, b, depth - 1, max_value_player)[0]
            # Check if the best move value we already have is less than the next move, if it is we pick it as we are
            # attempting to maximize and we also assign it the legal_move it should do
            if best_move[0] < next_move_value:
                best_move = (next_move_value, legalMoves[i])
            # Now it is the time to check if the value if more or equal to a and if it is we return the move
            if best_move[0] >= b:
                return best_move
            # we check if the alpha value is higher than our current bet_move value, if it is we assign this value to
            # b and finally return
            if a < best_move[0]:
                a = best_move[0]
        return best_move

    # This is the minimization legal function for the player
    def minimize_value(self, board, a, b, depth, symbol):
        # first step is to get the legal moves for the player
        legalMoves = game_rules.getLegalMoves(board, symbol)
        # check if the depth == 0 or if there are no other legal moves
        if len(legalMoves) == 0 or depth == 0:
            return self.h1(board, symbol), None
        # set the best value m ove to positive infinity as we are minimizing
        best_move = (POS_INF, None)
        for i in range(len(legalMoves)):
            # try and get the next moves based on the legal move of the loop
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == max_value_player:
                next_move_value = self.maximize_value(nextBoard, a, b, depth - 1, min_value_player)[0]
            else:
                next_move_value = self.maximize_value(nextBoard, a, b, depth - 1, max_value_player)[0]

            # Check if the best move value we already have is more than the next move, if it is we pick it as we are
            # attempting to minimize and we also assign it the legal_move it should do
            if best_move[0] > next_move_value:
                best_move = (next_move_value, legalMoves[i])
            # Now it is the tume to check if the value if less or equal to a and if it is we return the move
            if best_move[0] <= a:
                return best_move
            # we check if the beta value is higher than our current bet_move value, if it is we assign this value to
            # b and finally return
            if b > best_move[0]:
                b = best_move[0]
        return best_move


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0:
            return random.choice(legalMoves)
        else:
            return None


class DeterministicPlayer(Player):
    def __init__(self, symbol):
        super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        return (0, 0)

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0:
            return legalMoves[0]
        else:
            return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)

    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')

    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')

    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=3):
    player = playerType[0].lower()
    if player == 'h':
        return HumanPlayer(symbol)
    elif player == 'r':
        return RandomPlayer(symbol)
    elif player == 'm':
        return MinimaxPlayer(symbol, depth)
    elif player == 'a':
        return AlphaBetaPlayer(symbol, depth)
    elif player == 'd':
        return DeterministicPlayer(symbol)
    else:
        raise NotImplementedException('Unrecognized player type {}'.format(playerType))


def callMoveFunction(player, board):
    if game_rules.isInitialMove(board):
        return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else:
        return player.getMove(board)
