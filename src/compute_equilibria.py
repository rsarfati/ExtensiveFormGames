from numpy import unique, zeros, eye
from queue import Queue
from copy import *

def compute_equilibrium(game, players, type):
    """
    Inputs: game::GameTree, players::List{Int}, type::String

    Computes one equilibrium concept.
    """
    if game is None:
        raise InvalidInputException("Input is None")
    if game.tree.isEmpty():
        return []
	r = game.tree.root()

