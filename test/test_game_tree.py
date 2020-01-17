#!/usr/bin/python3
import sys
import copy
sys.path.insert(1, '../src')
from game import *

print('============= Ex. 1 ==============')
# Want to test the following tree:
#                  (1, 1)
#                 /      \
#           (2, 2)........(2, 2)
#          /      \        /    \
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

print('======== Leaves:')
for l in leaves_list:
	print(l.get_sequences())

