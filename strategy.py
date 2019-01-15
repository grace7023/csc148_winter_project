"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""

from typing import Any, List
from random import choice
from helper_classes import Tree, Stack
from game import Game
from game_state import GameState


def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Game) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_strategy(game: Game) -> Any:
    """
    Return a move for game that maximizes the chances of winning. This function
    is recursive.
    """
    current_state = game.current_state
    after_move = [current_state.make_move(x)
                  for x in current_state.get_possible_moves()]
    scores = [(-1) * max_move_score(game, x) for x in after_move]
    game.current_state = current_state
    return return_max_move(game.current_state.get_possible_moves(), scores)


def max_move_score(game: Game, state: GameState) -> int:
    """
    Return the score for the given state.
    """
    if game.is_over(state):
        game.current_state = state
        if game.is_winner(game.current_state.get_current_player_name()):
            return 1
        elif not game.is_winner(game.current_state.get_current_player_name()):
            return -1
        return 0
    states = [state.make_move(x) for x in state.get_possible_moves()]
    return max([(-1) * max_move_score(game, x) for x in states])


def iterative_strategy(game: Game) -> Any:
    """
    Return a move for game that maximizes the chances of winning. This function
    is iterative.
    """
    current_state = game.current_state
    after_move = [current_state.make_move(x)
                  for x in current_state.get_possible_moves()]
    scores = [(-1) * generate_states_score(game, x)
              for x in after_move]
    game.current_state = current_state
    return return_max_move(game.current_state.get_possible_moves(), scores)


def generate_states_score(game: Game, state: GameState) -> int:
    """
    Return the score for the given state.
    """
    s = Stack()
    t = Tree(state)
    s.add(t)
    while not s.is_empty():
        current_node = s.remove()
        current_state = current_node.value
        # assign score to states that are already over
        if game.is_over(current_state):
            game.current_state = current_state
            if game.is_winner(current_state.get_current_player_name()):
                current_node.score = 1
            elif not game.is_winner(current_state.get_current_player_name()):
                current_node.score = -1
            else:
                current_node.score = 0
        elif not current_node.children:
            # state not visited yet
            after_move = [Tree(current_state.make_move(x)) for x in
                          current_state.get_possible_moves()]
            current_node.children = after_move[:]
            s.add(current_node)
            for c in after_move:
                s.add(c)
        else:
            # state already visited, need to update score depending on children
            # and add to list_
            current_node.score = max([(-1) * x.score
                                      for x in current_node.children])
    return t.score


def return_max_move(moves: List[object], scores: List[int]) -> object:
    """ Return a move from moves where its corresponding score in scores
    is equal to max(scores).

    >>> return_max_move(['A', 'B', 'C'], [1, 1, -1]) in ['A', 'B']
    True
    """
    max_ = max(scores)
    return choice([moves[i] for i in range(len(moves)) if scores[i] == max_])
