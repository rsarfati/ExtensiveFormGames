import sys
sys.path.insert(1, '../src')
from game import *

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
g = Game(2, gt)

r = gt.add_root(1, 1)
inf2_1 = r.add_child(2, 2)
inf2_2 = r.add_child(2, 2)

inf3_1 = inf2_1.add_child(1, 3)
inf3_2 = inf2_1.add_child(1, 3)

inf4_1 = inf2_2.add_child(1, 4)
inf4_2 = inf2_2.add_child(1, 4)

set_payoffs(inf3_1.add_child(2, 5), [3, 3])
set_payoffs(inf3_1.add_child(2, 6), [2, 0])

set_payoffs(inf3_2.add_child(2, 7), [2, 2])
set_payoffs(inf3_2.add_child(2, 8), [0, 0])

set_payoffs(inf4_1.add_child(2, 9), [0, 4])
set_payoffs(inf4_1.add_child(2, 10),[2, 2])

set_payoffs(inf4_2.add_child(2, 11),[1, 1])
set_payoffs(inf4_2.add_child(2, 12),[3, 3])



