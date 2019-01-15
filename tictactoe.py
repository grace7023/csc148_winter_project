"""
Superclass Game
"""
from typing import Any, Union
from game import Game
from game_state import GameState


class TicTacToe(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        self.current_state = TicTacToeCS(p1_starts)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return "Player 1's mark is O and Player 2's mark is X. Players takes " \
               "turns placing their mark in a section of the grid (1, 2, 3 " \
               "are the top left, top center, top right, etc). First player " \
               "to get 3 of their marks in a row (horizontially, vertically, " \
               "diagonally) wins the game."

    def is_over(self, state: 'TicTacToeCS') -> bool:
        """
        Return whether or not this game is over at state.
        """
        return (all([x != ' ' for x in state.board]) or
                ['X', 'X', 'X'] in state.rows or
                ['O', 'O', 'O'] in state.rows or
                ['X', 'X', 'X'] in state.columns or
                ['O', 'O', 'O'] in state.columns or
                ['X', 'X', 'X'] in state.diag or
                ['O', 'O', 'O'] in state.diag)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        if not self.is_over(self.current_state):
            return False
        if (['O', 'O', 'O'] in self.current_state.rows or
            ['O', 'O', 'O'] in self.current_state.columns or
            ['O', 'O', 'O'] in self.current_state.diag) and player == 'p1':
            return True
        if (['X', 'X', 'X'] in self.current_state.rows or
            ['X', 'X', 'X'] in self.current_state.columns or
            ['X', 'X', 'X'] in self.current_state.diag) and player == 'p2':
            return True
        return False

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        return int(string)


def xd(s: Union[int, str]) -> str:
    """
    lol
    """
    if str(s) == 'X':
        return "\033[1;36m{0}\033[00m".format(s)
    elif str(s) == 'O':
        return "\033[01;31m{0}\033[00m".format(s)
    return s


class TicTacToeCS(GameState):
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    BOARD = """ {0[0]} | {0[1]} | {0[2]}
--- --- ---
 {0[3]} | {0[4]} | {0[5]}
--- --- ---
 {0[6]} | {0[7]} | {0[8]}
    """

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        super().__init__(is_p1_turn)
        self.board = [' ' for _ in range(9)]
        self.rows = [[self.board[i+j-1] for i in range(3)] for j in [1, 4, 7]]
        self.columns = [[self.board[j + 3 * i] for i in range(3)]
                        for j in range(3)]
        self.diag = [[self.board[0], self.board[4], self.board[8]],
                     [self.board[2], self.board[4], self.board[6]]]

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        lst = []
        for item in self.board:
            lst.append(xd(item))
        return self.BOARD.format(lst)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        if (['X', 'X', 'X'] in self.rows or
            ['O', 'O', 'O'] in self.rows or
            ['X', 'X', 'X'] in self.columns or
            ['O', 'O', 'O'] in self.columns or
            ['X', 'X', 'X'] in self.diag or
            ['O', 'O', 'O'] in self.diag):
            return []
        return [i+1 for i in range(9) if self.board[i] == ' ']

    def make_move(self, move: int) -> 'TicTacToeCS':
        """
        Return the GameState that results from applying move to this GameState.
        """
        symbol = 'X'
        if self.p1_turn:
            symbol = 'O'
        new_state = TicTacToeCS(not self.p1_turn)
        new_state.board = self.board[:]
        new_state.board[move - 1] = symbol
        new_state.rows = [[new_state.board[i+j-1] for i in range(3)]
                          for j in [1, 4, 7]]
        new_state.columns = [[new_state.board[j + 3 * i] for i in range(3)]
                             for j in range(3)]
        new_state.diag = [[new_state.board[0], new_state.board[4],
                           new_state.board[8]],
                          [new_state.board[2], new_state.board[4],
                           new_state.board[6]]]
        return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1 Turn: {}".format(self.p1_turn) + str(self)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        raise NotImplementedError
