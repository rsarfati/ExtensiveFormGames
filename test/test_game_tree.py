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

	print('- - - - - Leaves:')
	for l in leaves_list:
		print(l.get_sequences())

	print('- - - - - Player Sequences:')
	for p in [1]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_sequences(p))

	print('- - - - - Player Actions:')
	for p in [1]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_actions(p))

	print('- - - - - Player Inf. Sets:')
	for p in [1]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_info_sets(p))

	print(get_sequence_weight_vectors(g, 1))
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

	print('- - - - - Leaves:')
	for l in leaves_list:
		print(l.get_sequences())

	print('- - - - - Player Sequences:')
	for p in [1, 2]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_sequences(p))

	print('- - - - - Player Actions:')
	for p in [1, 2]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_actions(p))

	print('- - - - - Player Inf. Sets:')
	for p in [1, 2]:
		print('Player ' + str(p) + ':')
		print(gt.get_player_info_sets(p))

	print(get_sequence_weight_vectors(g, 1))
	print(get_sequence_weight_vectors(g, 2))


def get_tests():
    #return [von_stengel_test, test2, test3, test4, matching_pennies_sequence, dif1]
    return [simple_two_player_imp_info, one_player_2008]

# The mainline runs all of the test functions in the list returned by get_tests
if __name__ == '__main__' :
	print('Running game tree tests...')
	for test in get_tests():
		print('====== ' + str(test.__name__) + ' ======')
		test()
		
	print('All tests passed!')


