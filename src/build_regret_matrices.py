# This file contains methods enabling the replication of Gordon and Greenwald (2008)
from numpy import unique, zeros, eye
from queue import Queue
from copy import *

def get_sequence_continuations(game, node):
    """
    Inputs: game::GameTree

    Want to put sequences on the information sets to which they correspond
    """
    if game is None:
        raise InvalidInputException("Input is None")
    if game.tree.isEmpty():
        return []

    t = game.tree
    root = t.root()

    # To output:
    sequences = [[]]

    Q     = Queue()
    qlist = []

    while not Q.isempty():
        node = Q.get()

def find_first_divergence(seq1, seq2):
    for i in range(min(len(seq1), len(seq2))):
        if seq1[i] != seq2[i]:
            return i
    return -1

def first_move_after_divergence(ind, seqfrom):
    for i in range(ind, len(seqfrom)):
        if seqfrom[i] == 1:
            print("in", i)
            return i
    print("out", i)
    return ind

def info_set_to_index(game, player):
    """
    Input: game::Game, player::Int
    Output: tup_len::Int, inf_to_ind::Dict
    Complexity: O(n), n = # nodes in GameTree

    Maps information set to index in sequence weight vector.
    """
    inf_to_children = game.tree.info_set_to_num_children(player)
    inf_to_ind      = {}
    
    tup_len          = 0
    for i in inf_to_children.keys():
        inf_to_ind[i] = copy(tup_len)
        tup_len      += inf_to_children[i]
    
    return tup_len, inf_to_ind

def get_sequence_weight_vectors(game, player):
    """
    Input: game::Game, player::Int
    Output: seq_weight_vectors::List{List}
    Complexity: O(n), n = # nodes in GameTree

    Retrieves all sequence weight vectors of player.
    """
    inf_to_prefix = {} # Maps information set to its prefix
    inf_list      = {} # Maps information set to node (to keep track of visited)

    # Need to keep track of these when skipping over opponent's information sets
    last_player_inf  = {}
    last_player_move = {}

    # Maps information set to index in sq weight vec
    tup_len, inf_to_ind = info_set_to_index(game, player)

    # Desired output:
    seq_weight_vectors = [[]]

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
    return [list(x) for x in set(tuple(i) for i in seq_weight_vectors[1:])]

def build_internal_regret_matrices_seq_to_seq(game, player):
    """
    Input: game::Game, player::Int
    Output: phi_list::List{Array}

    Returns internal (pair-wise mappings) phi-regret matrices.
    """
    # sequences = [[1, 0, 0, 0], [0, 1, 1, 0], [0, 1, 0, 1]]

    gt        = game.tree
    sequences = get_sequence_weight_vectors(game, player)
    phi_size  = len(sequences[1])

    # Maps information set to index in sq weight vec
    tup_len, inf_to_ind = info_set_to_index(game, player)

    # To output: list of regret matrices
    phi_list  = [] 

    for seq_from in sequences:
        for seq_to in sequences:

            # Want to construct a matrix *per* pure strategy sequence 
            phi = zeros((phi_size, phi_size))
            
            # Find the index you start from, put probability in that cell
            ind = find_first_divergence(seq_to, seq_from)
            
            # If sequences don't diverge, you return the identity!
            if ind == -1:
                phi_list.append(eye(phi_size, phi_size))
            else:
                # Everything preceding first divergence should be the same;
                # Ones on diagonal
                ind_l = first_move_after_divergence(ind, seq_from) if (seq_from[ind] < seq_to[ind]) else ind

                for i in range(ind_l):
                    phi[i,i] = 1

                # If they do diverge, we start at the first divergence
                # and insert a column of the new sequence, there
                #inf_div = info_dict[seq_from[ind]]
                print(ind)
                print("From: ", seq_from)
                print("To:   ", seq_to)


                
                print(ind)
                for i in range(ind, n_info):
                    phi[i,ind_l] = seq_to[i]
                
                print(phi)
                print()

                phi_list.append(phi)
            
    return phi_list

if __name__ == '__main__' :
    regret_mats = build_regret_matrices_seq_to_seq()
    #for mat in regret_mats:
        #print(mat)
        #print()
            
