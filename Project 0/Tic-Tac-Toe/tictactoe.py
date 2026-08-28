"""
Tic Tac Toe Player
"""

import math
import copy

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
    n=sum(x is None for row in board for x in row)

    if n%2==0:
        return O
    else: 
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions=set()

    for row in range(0,3):
        for column in range(0,3):
            if board[row][column]==EMPTY:
                actions.add((row, column))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result=copy.deepcopy(board)
    i, j = action

    if i<0 or i>2 or j<0 or j>2:
        raise ValueError

    if result[i][j] is not EMPTY:
        raise ValueError
    else:
        result[i][j]=player(board)
        return result
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X,O):
        # Check horitzontal rows
        for i in range(0,3):
            if board[i][0]==player and board[i][1]==player and board[i][2]==player:
                return player

        # Check vertical rows
        for i in range(0,3):
            if board[0][i]==player and board[1][i]==player and board[2][i]==player:
                return player

        # Check diagonals
        if board[0][0]==player and board[1][1]==player and board[2][2]==player:
            return player

        if board[0][2]==player and board[1][1]==player and board[2][0]==player:
                    return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if sum(x is not EMPTY for row in board for x in row)==9 or winner(board) is not None: 
        return True 
    else: 
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    
    if winner(board)==O:
        return -1

    if winner(board)==None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    act=None

    if terminal(board)==True:
        return None

    if player(board)==X: # X is the maximizing player
        value=-math.inf

        for action in actions(board):
            if value<minvalue(result(board,action)):
                value=minvalue(result(board,action))
                act=action

    if player(board)==O: # O is the minimizing player
        value=math.inf
    
        for action in actions(board):
            if value>maxvalue(result(board,action)):
                value=maxvalue(result(board,action))
                act=action

    return act

def maxvalue(board):
    if terminal(board)==True:
        return utility(board)

    v=-math.inf

    for action in actions(board):
        v=max(v,minvalue(result(board,action)))

    return v


def minvalue(board):
    if terminal(board)==True:
        return utility(board)
    
    v=math.inf
    
    for action in actions(board):
        v=min(v,maxvalue(result(board,action)))

    return v

    