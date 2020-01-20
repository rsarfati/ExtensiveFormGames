#!/usr/bin/python3

# Useful: https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes
import sys
import copy
sys.path.insert(1, '../src')
import numpy as np
import pytest
from game import *
from build_regret_matrices import *

def one_player_2008():
	# Want to test the following tree:
	#
	#      (1, 1)
	#     /      \
	#  (1, 2)    (1, 3)
	#            /    \
	#        (1, 4)   (1, 5)
	#                 /     \
	#              (1, 6)    (1, 7)

	gt = GameTree()
	g  = Game(1, gt)

	r    = gt.add_root(1, 1)
	inf2 = r.add_child(1, 2)
	inf3 = r.add_child(1, 3)

	inf4 = inf3.add_child(1, 4)
	inf5 = inf3.add_child(1, 5)

	inf5.add_child(1, 6)
	inf5.add_child(1, 7)

	leaves_list = gt.leaves()

	# Leaves:
	leaves_true = [{1: [0]}, {1: [1, 0]}, {1: [1, 1, 0]}, {1: [1, 1, 1]}]
	for (i, l) in list(enumerate(leaves_list)):
		assert l.get_sequences() == leaves_true[i]

	# Player Sequences:
	assert gt.get_player_sequences(1) == [[1, 1, 0], [1, 0], [0], [1, 1, 1]]

	# Player Actions:
	assert gt.get_player_actions(1) == [0, 1, 0, 1, 0, 1]

	# Player Inf. Sets:
	assert gt.get_player_info_sets(1) == [1, 3, 5]

	# Sequence weight vectors:
	assert get_sequence_weight_vectors(g, 1) == [[1, 0, 0, 0, 0, 0], 
												 [0, 1, 0, 1, 1, 0], 
												 [0, 1, 0, 1, 0, 1], 
												 [0, 1, 1, 0, 0, 0]]
	#build_regret_matrices_seq_to_seq(g, 1)

def simple_two_player_imp_info():
	# Want to test the following tree:
	#
	#                  (1, 1)
	#                 /      \
	#           (2, 2)........(2, 2)
	#          /      \       /     \
	#     (1, 3)...(1, 3)   (1, 4)...(1, 4)
	#    /    /    |    |   |    |    \    \
	# |3|    |2|  |2|  |0| |0|  |2|   |1|  |3|
	# |3|    |0|  |2|  |0| |4|  |2|   |1|  |3|

	gt = GameTree()
	g  = Game(2, gt)

	r = gt.add_root(1, 1)
	inf2_1 = r.add_child(2, 2)
	inf2_2 = r.add_child(2, 2)

	inf3_1 = inf2_1.add_child(1, 3)
	inf3_2 = inf2_1.add_child(1, 3)

	inf4_1 = inf2_2.add_child(1, 4)
	inf4_2 = inf2_2.add_child(1, 4)

	inf3_1.add_child(2, 5).set_payoffs([3, 3])
	inf3_1.add_child(2, 6).set_payoffs([2, 0])

	inf3_2.add_child(2, 7).set_payoffs([2, 2])
	inf3_2.add_child(2, 8).set_payoffs([0, 0])

	inf4_1.add_child(2, 9).set_payoffs([0, 4])
	inf4_1.add_child(2, 10).set_payoffs([2, 2])

	inf4_2.add_child(2, 11).set_payoffs([1, 1])
	inf4_2.add_child(2, 12).set_payoffs([3, 3])

	leaves_list = gt.leaves()

	# Leaves:
	leaves_true = [ {1: [0, 0], 2: [0]}, {1: [0, 1], 2: [0]}, {1: [0, 0], 2: [1]},
					{1: [0, 1], 2: [1]}, {1: [1, 0], 2: [0]}, {1: [1, 1], 2: [0]},
					{1: [1, 0], 2: [1]}, {1: [1, 1], 2: [1]}]
	for (i, l) in list(enumerate(leaves_list)):
		assert l.get_sequences() == leaves_true[i]

	# Player Sequences:
	assert gt.get_player_sequences(1) == [[0, 1], [1, 0], [0, 0], [1, 1]]
	assert gt.get_player_sequences(2) == [[0], [1]]

	# Player Actions:
	assert gt.get_player_actions(1) == [0, 1, 0, 1, 0, 1]
	assert gt.get_player_actions(2) == [0, 1]

	# Player Inf. Sets:
	assert gt.get_player_info_sets(1) == [1, 3, 4]
	assert gt.get_player_info_sets(2) == [2]

	assert get_sequence_weight_vectors(g, 1) == [[1, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0], [1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1]]
	assert get_sequence_weight_vectors(g, 2) == [[0, 1], [1, 0]]

def get_tests():
    return [simple_two_player_imp_info, one_player_2008]

# The mainline runs all of the test functions in the list returned by get_tests
if __name__ == '__main__' :
	print('Running game tree tests...')
	for test in get_tests():
		print('* ' + str(test.__name__))
		test()
		
	print('All tests passed!')


