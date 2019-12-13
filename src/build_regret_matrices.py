# This file contains methods enabling the replication of Gordon and Greenwald (2008)
from numpy import unique, zeros

def get_player_sequences(game):
    """
    Input: game tree
    Output: unique player sequences (list of information sets)
    """
    sequences = [[]]
    return sequences

def get_info_sets(game):
    """
    Input: game tree
    Output: unique player information sets
    """
    info_sets = []
    return info_sets

def build_regret_matrices(game):
    sequences = get_player_sequences(game)
    info_sets = get_info_sets(game)
    info_dict = {} # want this to map info sets to their order
    n_info    = length(info_sets)
    phi_list  = []
    for seq_from in sequences:
        for seq_to in sequences:
            # Want to construct a matrix per pure strategy sequence (will prune for 
            # uniqueness, later)
            phi = zeros(info_sets, info_sets)
            # Here, we want to (1) find the index you start from, put probability
            # in that cell



            phi_list.append(phi)
            
    return phi_list
            
