from numpy import unique, zeros, eye
from queue import Queue
from copy import *

def recur_decorate(game, n, visited, p_ih, q_ih):
	visited[n] = True # Mark as visited

	# Do whatever it is you wanted to do
	p_ih[n] = 

	
	for child in n.get_children():
		if child not in visited.keys():
			visited = recur_decorate(game, child, visited)

	return visited

def initialize_tree(game):
	"""
	Inputs: game::Game

    Initializes probabilities of actions at all information sets to be 
    uniform, and correspondingly the probabilities of states within
    information sets to be uniform.
	"""
	q_ih = {} # Maps INFORMATION SETS to probabilities over states
	p_ih = {} # Maps INFORMATION SETS to probabilities over actions
	visited = {} # Maps NODES to boolean of whether yet initialized

	Q  = Queue()
    Q.put(game.tree.root())

    # Depth-first search through tree
    while not Q.empty():
        n = Q.get()

        # If player's inf set did not precede node, set to 0
        if n not in last_player_inf.keys():
            last_player_inf[n] = 0
            
        if n.get_player() == player or n.is_leaf():

            # Base case: inf. set has no prefix of past player's action
            if last_player_inf[n] == 0:
                inf_to_prefix[n.get_information_set()] = [0] * tup_len
                
            else:
                # Take prefix of actions getting to most recent inf. set of player
                tup_new = deepcopy(inf_to_prefix[last_player_inf[n]])

                # Put 1 in the position of past move getting to this inf. set
                tup_new[inf_to_ind[last_player_inf[n]] + last_player_move[n]] = 1

                # Set new prefix for this inf. set 
                inf_to_prefix[n.get_information_set()] = deepcopy(tup_new)
            
            # If player node, then future inf. sets should have this as "most recent"
            if n.get_player() == player:
                last_player_inf[n] = n.get_information_set()

            # Append the sequences terminating at leaves
            if n.is_leaf():
                seq_weight_vectors.append(deepcopy(tup_new))

        for child in n.get_children():

            # Inherit most recent player inf. set from parent
            last_player_inf[child] = deepcopy(last_player_inf[n])
            
            if n.get_player() == player:
                # If current node is in player inf. set, most recent move is child id
                last_player_move[child] = deepcopy(child.n_id)

            elif last_player_inf[n] is not 0:
                # If current node is not, inherit last player move from parent
                last_player_move[child] = deepcopy(last_player_move[n])

            else: 
                # Base case: player has not yet moved
                last_player_move[child] = 0

            Q.put(child)

    # This convoluted expression just ensures uniqueness of entries
    to_return = [list(x) for x in set(tuple(i) for i in seq_weight_vectors[1:])]
    
    if return_all:
        return to_return, inf_to_prefix, last_player_inf, last_player_move

    return to_return


def compute_equilibrium(game, players, type = "afce"):
    """
    Inputs: game::GameTree, players::List{Int}, type::String

    Computes one equilibrium concept.
    """
    if game is None:
        raise InvalidInputException("Input is None")
    if game.tree.isEmpty():
        return []
	
	n = game.tree.root()

	R_in = {} # Maps STATES to expected reward
	R_ih = {} # Maps INFORMATION SETS to expected reward
	q_ih = {} # Maps INFORMATION SETS to probabilities over states
	p_ih = {} # Maps INFORMATION SETS to probabilities over actions




	inf_to_prefix = {} # Maps information set to its prefix
    inf_list      = {} # Maps information set to node (to keep track of visited)

    # Need to keep track of these when skipping over opponent's information sets
    last_player_inf  = {}
    last_player_move = {}

    # Maps information set to index in sq weight vec
    tup_len, inf_to_ind = info_set_to_index(game, player)

    Q  = Queue()
    Q.put(game.tree.root())

    # Breadth-first search through tree
    while not Q.empty():
        n = Q.get()

        # If player's inf set did not precede node, set to 0
        if n not in last_player_inf.keys():
            last_player_inf[n] = 0
            
        if n.get_player() == player or n.is_leaf():

            # Base case: inf. set has no prefix of past player's action
            if last_player_inf[n] == 0:
                inf_to_prefix[n.get_information_set()] = [0] * tup_len
                
            else:
                # Take prefix of actions getting to most recent inf. set of player
                tup_new = deepcopy(inf_to_prefix[last_player_inf[n]])

                # Put 1 in the position of past move getting to this inf. set
                tup_new[inf_to_ind[last_player_inf[n]] + last_player_move[n]] = 1

                # Set new prefix for this inf. set 
                inf_to_prefix[n.get_information_set()] = deepcopy(tup_new)
            
            # If player node, then future inf. sets should have this as "most recent"
            if n.get_player() == player:
                last_player_inf[n] = n.get_information_set()

            # Append the sequences terminating at leaves
            if n.is_leaf():
                seq_weight_vectors.append(deepcopy(tup_new))

        for child in n.get_children():

            # Inherit most recent player inf. set from parent
            last_player_inf[child] = deepcopy(last_player_inf[n])
            
            if n.get_player() == player:
                # If current node is in player inf. set, most recent move is child id
                last_player_move[child] = deepcopy(child.n_id)

            elif last_player_inf[n] is not 0:
                # If current node is not, inherit last player move from parent
                last_player_move[child] = deepcopy(last_player_move[n])

            else: 
                # Base case: player has not yet moved
                last_player_move[child] = 0

            Q.put(child)

    # This convoluted expression just ensures uniqueness of entries
    to_return = [list(x) for x in set(tuple(i) for i in seq_weight_vectors[1:])]
    
    if return_all:
        return to_return, inf_to_prefix, last_player_inf, last_player_move

    return to_return