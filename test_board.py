from isolation import Board
from test_players import RandomPlayer
import player_submission_tests as tests


# export
class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        """Score the current game state
        Evaluation function that outputs a score equal to how many
        moves are open for AI player on the board minus how many moves
        are open for Opponent's player on the board.

        Note:
            If you think of better evaluation function, do it in CustomEvalFn below.

            Args
                game (Board): The board and game state.
                my_player (Player object): This specifies which player you are.

            Returns:
                float: The current state's score. MyMoves-OppMoves.

            """

        # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
        if not my_player:
            my_player = game.__active_

        my_moves = game.get_player_moves(my_player)
        opp_moves = game.get_opponent_moves(my_player)

        return len(my_moves) - len(opp_moves)


######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
# tests.correctOpenEvalFn(OpenMoveEvalFn)


################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆

class CustomEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        Custom evaluation function that acts however you think it should. This
        is not required but highly encouraged if you want to build the best
        AI possible.

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
        if not my_player:
            my_player = game.get_active_player()

        my_moves = game.get_player_moves(my_player)
        opp_moves = game.get_opponent_moves(my_player)

        intersection_moves = [move for move in my_moves if move in opp_moves]

        return len(my_moves) - len(opp_moves) + len(set(intersection_moves))

# export
class CustomPlayer:
    # TODO: finish this class!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, search_depth=3, eval_fn=CustomEvalFn()):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Evaluation function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, time_left):
        """Called to determine one move by your agent

        Note:
            1. Do NOT change the name of this 'move' function. We are going to call
            this function directly.
            2. Call alphabeta instead of minimax once implemented.
        Args:
            game (Board): The board and game state.
            time_left (function): Used to determine time left before timeout

        Returns:
            tuple: (int,int): Your best move
        """
        best_move = None
        try:
            while time_left() > 0:
                best_move, utility = alphabeta(self, game, time_left, depth=self.search_depth)
                self.search_depth += 1
        except Exception:
            pass

        return best_move

    def utility(self, game, my_turn):
        """You can handle special cases here (e.g. endgame)"""

        return self.eval_fn.score(game, self)


###################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE CLASS! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
###### IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ###########͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
###################################################################
# export

def minimax(player, game, time_left, depth, my_turn=True):
    """Implementation of the minimax algorithm.
    Args:
        player (CustomPlayer): This is the instantiation of CustomPlayer()
            that represents your agent. It is used to call anything you
            need from the CustomPlayer class (the utility() method, for example,
            or any class variables that belong to CustomPlayer()).
        game (Board): A board and game state.
        time_left (function): Used to determine time left before timeout
        depth: Used to track how deep you are in the search tree
        my_turn (bool): True if you are computing scores during your turn.

    Returns:
        (tuple, int): best_move, val
    """

    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆

    time_limit = 10000

    if my_turn:
        best_move, val = max_move(player, game, time_left, depth, current_depth=0, my_turn=my_turn)
    else:
        best_move, val = min_move(player, game, time_left, depth, current_depth=0, my_turn=my_turn)

    return best_move, val


def max_move(player, game, time_left, depth, current_depth=0, my_turn=True):
    maxi_move = None
    max_val = float("-inf")

    valid_moves = game.get_player_moves(player)
    if current_depth == depth or len(valid_moves) == 0:
        max_val = player.utility(game, my_turn)
        return maxi_move, max_val

    current_depth += 1

    for move in valid_moves:
        game_copy, _, _ = game.forecast_move(move)

        next_move, next_val = min_move(player, game_copy, time_left, depth, current_depth, my_turn)

        # Evaluate
        if next_val > max_val:
            max_val = next_val
            maxi_move = move

    return maxi_move, max_val


def min_move(player, game, time_left, depth, current_depth=0, my_turn=True):
    mini_move = None
    min_val = float("inf")

    valid_moves = game.get_player_moves(player)

    if current_depth >= depth or len(valid_moves) == 0:
        max_val = player.utility(game, my_turn)
        return max_move, max_val

    current_depth += 1

    opp_valid_moves = game.get_opponent_moves(player)

    for move in opp_valid_moves:
        game_copy, _, _ = game.forecast_move(move)

        next_move, next_val = max_move(player, game_copy, time_left, depth, current_depth, my_turn)

        if next_val < min_val:
            min_val = next_val
            mini_move = move

    return mini_move, min_val


######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆


################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆

# export
def alphabeta(player, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), my_turn=True):
    """Implementation of the alphabeta algorithm.

    Args:
        player (CustomPlayer): This is the instantiation of CustomPlayer()
            that represents your agent. It is used to call anything you need
            from the CustomPlayer class (the utility() method, for example,
            or any class variables that belong to CustomPlayer())
        game (Board): A board and game state.
        time_left (function): Used to determine time left before timeout
        depth: Used to track how deep you are in the search tree
        alpha (float): Alpha value for pruning
        beta (float): Beta value for pruning
        my_turn (bool): True if you are computing scores during your turn.

    Returns:
        (tuple, int): best_move, val
    """

    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
    if my_turn:
        best_move, val = alphabeta_max(player, game, time_left, depth, current_depth=0, alpha=float("-inf"),
                                       beta=float("inf"), my_turn=my_turn)
    else:
        best_move, val = alphabeta_min(player, game, time_left, depth, current_depth=0, alpha=float("-inf"),
                                       beta=float("inf"), my_turn=my_turn)

    return best_move, val


def alphabeta_max(player, game, time_left, depth, current_depth=0, alpha=float("-inf"), beta=float("inf"),
                  my_turn=True):
    maxi_move = None
    max_val = float("-inf")

    valid_moves = game.get_player_moves(player)
    if current_depth >= depth or len(valid_moves) == 0:
        max_val = player.utility(game, my_turn)
        return maxi_move, max_val

    # current depth increment
    current_depth += 1

    for move in valid_moves:
        game_copy, _, _ = game.forecast_move(move)

        next_move, next_val = alphabeta_min(player, game_copy, time_left, depth, current_depth, alpha, beta, my_turn)

        # compare max_val
        if next_val > max_val:
            max_val = next_val
            maxi_move = move
            alpha = max(alpha, max_val)

        if max_val >= beta:
            break

    return maxi_move, max_val


def alphabeta_min(player, game, time_left, depth, current_depth=0, alpha=float("-inf"), beta=float("inf"),
                  my_turn=True):
    mini_move = None
    min_val = float("inf")

    valid_moves = game.get_player_moves(player)
    if current_depth >= depth or len(valid_moves) == 0:
        min_val = player.utility(game, my_turn)
        return mini_move, min_val

    current_depth += 1

    opp_valid_moves = game.get_opponent_moves(player)

    for move in opp_valid_moves:
        game_copy, _, _ = game.forecast_move(move)

        next_move, next_val = alphabeta_max(player, game_copy, time_left, depth, current_depth, alpha, beta,
                                            my_turn=my_turn)

        # next_move, next_val = max_move(player, game_copy, time_left, depth, current_depth, my_turn)

        # Evaluate for max
        if next_val < min_val:
            min_val = next_val
            mini_move = move
            beta = min(beta, min_val)

        if min_val <= alpha:
            break

    return mini_move, min_val


######################################################################
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######## IF YOU WANT TO CALL OR TEST IT CREATE A NEW CELL ############͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
######################################################################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆
# tests.name_of_the_test #you can uncomment this line to run your test͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆

################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏󠄋͏󠄏͏󠄄͏󠄆

if __name__ == '__main__':
    #game = Board(RandomPlayer(), RandomPlayer())
    #winner, move_history, termination = game.play_isolation(time_limit=1000, print_moves=True)

    tests.beatRandom(CustomPlayer)
    tests.alphabetaTest(CustomPlayer, alphabeta)