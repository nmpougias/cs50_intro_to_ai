"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialize counters.
    counter_x = 0
    counter_o = 0

    # Counting Xs and Os.
    for row in board:
        counter_x += row.count(X)
        counter_o += row.count(O)

    # Checking if there is a possible move. If amove is possible,
    # since X plays first, everytime berore X's turn: Xs = Os.
    if (counter_x + counter_o) == 9:
        # print("No player can make a move")
        return None
    elif counter_x == counter_o:
        # print("It is X player's move")
        return X
    else:
        # print("It is O player's move")
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initializing the set.
    action_set = set()
    # Checking if a place on the board is EMPTY, if so add it to the set.
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                action_set.add((i, j))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Creating new board as a deepcopy so that the original board does not change.
    new_board = copy.deepcopy(board)

    # Getting indexes.
    i, j = action

    # Raising an exception if the action chosen cannot fit in the board.
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise Exception("The selected move coordinates are not correct.")

    # Saving active player's move, only if the spot is EMPTY.
    # If not EMPTY, an exception is raised.
    if not board[i][j]:
        new_board[i][j] = player(board)
        return new_board
    else:
        raise Exception("This spot is not available!")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Initializing sets to chech if the rows or the columns or the diagonals contain the same value.
    row = set()
    column = set()
    diagonal = set()
    anti_diagonal = set()

    for i in range(3):
        # Clearing each set of row and column before checking.
        row.clear()
        column.clear()

        # Filling the set with the elements of the diagonal and the anti-diagonal.
        diagonal.add(board[i][i])
        anti_diagonal.add(board[i][-(i + 1)])

        # Filling the set with the elements of the row and the column.
        for j in range(3):
            row.add(board[i][j])
            column.add(board[j][i])

        # Checking if a win condition is met in any row, any column, the diagonal or the anti-diagonal.
        # If a set has a length of 1, then all the elements of the row (or column or diagonal) are equal (and not EMPTY).
        if len(row) == 1 and board[i][j]:
            return list(row)[0]
        elif len(column) == 1 and board[j][i]:
            return list(column)[0]

    if (len(diagonal) == 1 or len(anti_diagonal) == 1) and board[1][1]:
        return board[1][1]

    # If there is no winner, then return NONE.
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not player(board):
        # print("The game has ended! Thanks for playing.")
        return True
    else:
        # print("The game is still in progress.")
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None

    # Finding the best available action.
    match player(board):
        case "X":
            best_action = max_value(board)[1]
        case "O":
            best_action = min_value(board)[1]

    return best_action


def max_value(board, start_value=10):
    """
    Returns the max value for the given state of the board.
    """
    # Initializing temporary value, best_action and action_set.
    value = -10
    best_action = None
    action_set = actions(board)

    # Checking if current state is a terminal state.
    if terminal(board):
        return (utility(board), None)

    # If not search for current state's estimated value.
    while len(action_set) > 0:
        # Choosing a random action from the set, then removing it.
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # This the implementation of A-B Pruning.
        if value >= start_value:
            break

        # Calculating max manually in order to return the best action.
        min_player = min_value(result(board, action), value)
        if min_player[0] > value:
            best_action = action
            value = min_player[0]

    return (value, best_action)


def min_value(board, start_value=-10):
    """
    Returns the min value for the given state of the board.
    """
    # Initializing temporary value, best_action and action_set.
    value = 10
    best_action = None
    action_set = actions(board)

    # Checking if current state is a terminal state.
    if terminal(board):
        return (utility(board), None)

    # If not search for current state's estimated value.
    while len(action_set) > 0:
        # Choosing a random action from the set, then removing it.
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # This the implementation of A-B Pruning.
        if value <= start_value:
            break

        # Calculating min manually in order to return the best action.
        max_player = max_value(result(board, action), value)
        if max_player[0] < value:
            best_action = action
            value = max_player[0]

    return (value, best_action)
