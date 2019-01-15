"""
stonehenge game
"""
from typing import Any, Dict, List, Union
from game import Game
from game_state import GameState
from stonehenge_constants import (generate_leylines, LETTERS_ROW, GRIDS)


class Stonehenge(Game):
    """
    Abstract class for a game to be played with two players.

    side_length - side length of the Stonehenge game
    current_state - current_state of Stonehenge game
    """

    side_length: int
    current_state: 'StonehengeCS'

    INSTR = 'Players take turns claiming cells. When a player captures at \
least half of the cells in a ley-line , then the player captures that \
ley-line. A ley-line, once claimed, cannot be taken by the other player. \
The first player to capture at least half of the ley-lines is the winner.'

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        n = input('Enter a number between 1 and 5, inclusive: ')
        # x.isnumeric() checks that x is type int and is non-negative.
        while not n.isnumeric() or not 1 <= int(n) <= 5:
            n = input('Input is not valid. Try again: ')
        self.side_length = int(n)
        self.current_state = StonehengeCS(p1_starts, self.side_length)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return self.INSTR

    def is_over(self, state: 'StonehengeCS') -> bool:
        """
        Return whether or not this game is over at state.
        """
        count_1 = 0
        count_2 = 0
        for key in state.leylines:
            count_1 += state.leylines[key].count(1)
            count_2 += state.leylines[key].count(2)
        if (count_1 >= (state.side_length + 1) * 3 / 2 or
                count_2 >= (state.side_length + 1) * 3 / 2):
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        if not self.is_over(self.current_state):
            return False
        player_int = int(player[1])
        count = 0
        for key in self.current_state.leylines:
            count += self.current_state.leylines[key].count(player_int)
        if count >= (self.current_state.side_length + 1) * 3 / 2:
            return True
        return False

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if string not in self.current_state.get_possible_moves():
            return '-1'
        return string


class StonehengeCS(GameState):
    """
    The state of a game at a certain point in time.

    p1_turn - whether it is p1's turn
    side_length - side length of the Stonehenge game
    leylines_letters - all groups of letters that form leylines
    leylines - leyline key that responds to each leyline
    letters - letters at each node
    """
    side_length: int
    leylines_letters: Dict[str, List[List[Union[int, str]]]]
    leylines: Dict[str, List[Union[int, str]]]
    letters: List[Union[str, int]]

    def __init__(self, is_p1_turn: bool, n: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> x = StonehengeCS(True, 2)
        >>> x.side_length == 2
        True
        """
        super().__init__(is_p1_turn)
        self.side_length = n
        ley = generate_leylines(n)
        self.leylines_letters = ley[0]
        self.leylines = ley[1]
        self.letters = [x for x in LETTERS_ROW[:(n + 1) * (n + 2) // 2 - 1 + n]]

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        return GRIDS[self.side_length - 1].format(self.leylines, self.letters)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to self.

        >>> StonehengeCS(True, 1).get_possible_moves()
        ['A', 'B', 'C']
        """
        count_1 = 0
        count_2 = 0
        for key in self.leylines:
            count_1 += self.leylines[key].count(1)
            count_2 += self.leylines[key].count(2)
        if (count_1 >= (self.side_length + 1) * 3 / 2 or
                count_2 >= (self.side_length + 1) * 3 / 2):
            return []
        return [x for x in self.letters if str(x).isalpha()]

    def make_move(self, move: str) -> 'StonehengeCS':
        """
        Return a new GameState that results from applying move to self.

        >>> x = StonehengeCS(True, 1)
        >>> y = x.make_move('A')
        >>> y.leylines
        {'r': [1, '@'], 't': ['@', 1], 'b': [1, '@']}
        """
        current_player = self.get_current_player_name()
        # make new state and change current player
        new_state = StonehengeCS(not self.p1_turn, self.side_length)
        # change state.letters
        new_state.letters = self.letters[:]
        new_state.letters[new_state.letters.index(move)] = \
            int(current_player[1])

        # make a copy of self.leylines_letters
        for key in self.leylines_letters:
            new_state.leylines_letters[key] = list([list(x) for x in
                                                    self.leylines_letters[key]])
            new_state.leylines[key] = list(self.leylines[key])

        # change state.leylines_letters
            for elem in new_state.leylines_letters[key]:
                for i in range(len(elem)):
                    elem[i] = int(current_player[1]) if elem[i] == move \
                        else elem[i]

        # check if more than half a leyline is claimed by a player to change
        # state.leyline
            for i in range(len(new_state.leylines_letters[key])):
                n = len(new_state.leylines_letters[key][i]) / 2
                count_player = int(current_player[1])
                if (new_state.leylines_letters[key][i].count(count_player) >= n
                        and new_state.leylines[key][i] == '@'):
                    new_state.leylines[key][i] = count_player
        return new_state

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1's Turn: {}\n".format(self.p1_turn) + str(self)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> x = StonehengeCS(True, 1)
        >>> x.rough_outcome()
        1
        """
        if any([(not self.make_move(x).get_possible_moves())
                for x in self.get_possible_moves()]):
            return self.WIN
        else:
            f_move = [self.make_move(x) for x in self.get_possible_moves()]
            s_move = [x.make_move(y) for x in f_move
                      for y in x.get_possible_moves()]
            if all([(not x.get_possible_moves()) for x in s_move]):
                return self.LOSE
            return self.DRAW
