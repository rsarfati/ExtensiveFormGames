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

def get_sequence_weight_vectors(game, player):
    gt = game.tree

    inf_to_children = gt.info_set_to_num_children(player)
    
    inf_to_prefix = {} # Maps information set to its prefix
    inf_list      = {} # Maps information set to node (to keep track of visited)
    inf_to_ind    = {} # Maps information set to index in sq weight vec

    # Need to keep track of these when skipping over opponent's information sets
    last_player_inf  = {}
    last_player_move = {}

    # Determine the tuple length and the starting indices for information sets
    tup_len = 0
    for i in inf_to_children.keys():
        inf_to_ind[i] = copy(tup_len)
        tup_len += inf_to_children[i]

    # Desired output:
    seq_weight_vectors = [[]]

    Q  = Queue()
    Q.put(gt.root())

    # Breadth-first search through tree
    while not Q.empty():
        n = Q.get()

        # If player's inf set did not precede node, set to 0
        if n not in last_player_inf.keys():
            last_player_inf[n] = 0
            
        if n.get_player() == player or n.is_leaf():

            if last_player_inf[n] == 0:
                inf_to_prefix[n.get_information_set()] = [0] * tup_len
                
            else:
                tup_new = deepcopy(inf_to_prefix[last_player_inf[n]])

                tup_new[inf_to_ind[last_player_inf[n]] + last_player_move[n]] = 1

                inf_to_prefix[n.get_information_set()] = deepcopy(tup_new)
             
            if n.get_player() == player:
                last_player_inf[n] = n.get_information_set()

            if n.is_leaf():
                seq_weight_vectors.append(deepcopy(tup_new))

        for child in n.get_children():

            last_player_inf[child] = deepcopy(last_player_inf[n])
            
            if n.get_player() == player:
                last_player_move[child] = deepcopy(child.n_id)
            
            elif last_player_inf[n] is not 0:
                last_player_move[child] = deepcopy(last_player_move[n])
            
            else: 
                last_player_move[child] = 0

            Q.put(child)

    return [list(x) for x in set(tuple(i) for i in seq_weight_vectors[1:])]


def build_regret_matrices_seq_to_seq(game, player):
    # sequences = [[1, 0, 0, 0], [0, 1, 1, 0], [0, 1, 0, 1]]
    # info_sets = [1, 2, 3, 4]
    gt        = game.tree
    sequences = gt.get_player_sequences(player)
    info_sets = gt.get_player_info_sets(player)
    n_info    = len(info_sets)

    # To output: list of regret matrices
    phi_list  = [] 
    
    print(sequences)

    for seq_from in sequences:
        for seq_to in sequences:

            # Want to construct a matrix *per* pure strategy sequence 
            phi = zeros((n_info, n_info))
            
            # Find the index you start from, put probability in that cell
            ind = find_first_divergence(seq_to, seq_from)
            
            # If sequences don't diverge, you return the identity!
            if ind == -1:
                phi_list.append(eye(n_info, n_info))
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
            
