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
    inf_to_ind = {}

    tup_len = 0
    print(inf_to_children.keys())
    for i in inf_to_children.keys():
        inf_to_ind[i] = copy(tup_len)
        tup_len += inf_to_children[i]

    print("Tup Len ")
    print(tup_len)

    print("Dict to ind")
    print(inf_to_ind)

    Q  = Queue()
    inf_to_prefix = {} # Maps information set to its prefix
    inf_list      = {} # Maps information set to node (to keep track of visited)

    last_player_inf = {}

    # Desired output:
    seq_weight_vectors = [[]]

    Q.put(gt.root())

    while not Q.empty():
        n = Q.get()
        print("(" + str(n.get_player()) + ", " + str(n.get_information_set()) + ")")
        # If player's inf set did not precede it, set to 0
        if n not in last_player_inf.keys():
            last_player_inf[n] = 0
            
        if n.get_player() == player:
            if n.get_information_set() not in inf_to_prefix.keys():
                
                print("Information set: " + str(n.get_information_set()))

                tup_new = [0]*tup_len

                if gt.is_root(n):
                    print("ROOOOT")
                    inf_to_prefix[n.get_information_set()] = deepcopy(tup_new)
                else:
                    print("Last player info set: " + str(last_player_inf[n]))

                    tup_new = [0]*tup_len if last_player_inf[n] == 0 else deepcopy(inf_to_prefix[last_player_inf[n]])

                    #print("Tuple init: " + str(tup_new))
                    print("Inf to ind: " + str(inf_to_prefix[last_player_inf[n]]))

                    tup_new[inf_to_ind[last_player_inf[n]] + n.n_id] = 1

                    inf_to_prefix[n.get_information_set()] = deepcopy(tup_new)
                    # W/in inf set, actions should be same; don't double-count
                    
                if n.is_leaf():
                    print("Appending: " + str(tup_new))
                    seq_weight_vectors.append(deepcopy(tup_new))

            last_player_inf[n] = n.get_information_set()

        print(inf_to_prefix)

        for child in n.get_children():
            last_player_inf[child] = deepcopy(last_player_inf[n])
            Q.put(child)

    return seq_weight_vectors[1:]


    actions   = gt.get_player_actions(player)
    info_sets = gt.get_player_info_sets(player)
    n_info    = len(info_sets)

    seq_weight_vectors = []

    for seq in sequences:
        swv = zeros((n_info,))


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
            
