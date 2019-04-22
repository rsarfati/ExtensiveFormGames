import tree
import game
import importlib
import numpy as np
import sequence_form
importlib.reload(tree)
from tree import *
from game import *
from sequence_form import *
import pytest

def normal_form_test():
	g = {0 : {}, 1 : {}, 2 : {}, 3 : {}, 4 : {}, 5 : {}, 6 : {}, 7 : {} }
	a = np.zeros((7,4))
	b = np.zeros((7,4))

	g[0][0] = (0,0)
	g[0][1] = (0,0)
	g[0][2] = (0,0)
	g[0][3] = (0,0)

	g[1][0] = (1,-1)
	g[1][1] = (1,-1)
	g[1][2] = (1,-1)
	g[1][3] = (1,-1)

	g[2][0] = (1,-1)
	g[2][1] = (1,-1)
	g[2][2] = (1,-1)
	g[2][3] = (1,-1)

	g[3][0] = (1,-1)
	g[3][1] = (1,-1)
	g[3][2] = (1,-1)
	g[3][3] = (1,-1)

	g[4][0] = (0,0)
	g[4][1] = (2,-2)
	g[4][2] = (4,-4)
	g[4][3] = (0,0)

	g[5][0] = (0,0)
	g[5][1] = (3,-3)
	g[5][2] = (4,-4)
	g[5][3] = (0,0)

	g[6][0] = (0,0)
	g[6][1] = (0,0)
	g[6][2] = (4,-4)
	g[6][3] = (5,-5)

	for i in range(7):
		for j in range(4):
			a[i][j] = g[i][j][0]
			b[i][j] = g[i][j][1]

	print("A matrix, Normal Form: ")
	print(a)
	print("B matrix, Normal Form: ")
	print(b)

def strategic_form_test():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	
	curr2.set_payoffs([3,3])

	curr3 = bt.addChild(curr, 3)
	curr4 = bt.addChild(curr, 4)

	curr3.set_information_set(1,3)
	curr4.set_information_set(1,3)

	curr5 = bt.addChild(curr3, 5)

	curr5.set_payoffs([2,2])
	curr6 = bt.addChild(curr3, 6)
	curr6.set_payoffs([0,3])

	curr7 = bt.addChild(curr4, 7)

	curr7.set_payoffs([5,6])
	curr8 = bt.addChild(curr4, 8)
	curr8.set_payoffs([6,1])

	game = Game(2, bt)
	A, B = extensive_to_strategic_form(game)
	solve_strategic_form(A.tolist(), B.tolist())

def sequence_big_test():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 3)
	curr3 = bt.addChild(bt.root(), 3)

	curr3.set_payoffs([0.5,-0.5])

	curr4 = bt.addChild(curr, 4)
	curr5 = bt.addChild(curr, 5)

	curr4.set_information_set(1,4)
	curr5.set_information_set(1,4)

	curr6 = bt.addChild(curr4, 5)
	curr7 = bt.addChild(curr4, 5)
	curr6.set_payoffs([-4, 4])
	curr7.set_payoffs([2, -2])

	curr8 = bt.addChild(curr5, 8)
	curr9 = bt.addChild(curr5, 9)
	curr8.set_payoffs([4, -4])
	curr9.set_payoffs([-2, 2])

	curr10 = bt.addChild(curr2, 10)
	curr11 = bt.addChild(curr2, 11)
	curr12 = bt.addChild(curr2, 12)

	curr10.set_payoffs([-1, 1])
	curr11.set_payoffs([-1, 1])
	curr12.set_payoffs([-1, 1])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	return A, B, E, F, e, f 

def strategic_big_test():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 3)
	curr3 = bt.addChild(bt.root(), 3)

	curr3.set_payoffs([0.5,-0.5])

	curr4 = bt.addChild(curr, 4)
	curr5 = bt.addChild(curr, 5)

	curr4.set_information_set(1,4)
	curr5.set_information_set(1,4)

	curr6 = bt.addChild(curr4, 5)
	curr7 = bt.addChild(curr4, 5)
	curr6.set_payoffs([-4, 4])
	curr7.set_payoffs([2, -2])

	curr8 = bt.addChild(curr5, 8)
	curr9 = bt.addChild(curr5, 9)
	curr8.set_payoffs([4, -4])
	curr9.set_payoffs([-2, 2])

	curr10 = bt.addChild(curr2, 10)
	curr11 = bt.addChild(curr2, 11)
	curr12 = bt.addChild(curr2, 12)

	curr10.set_payoffs([-1, 1])
	curr11.set_payoffs([-1, 1])
	curr12.set_payoffs([-1, 1])

	game = Game(2, bt)
	A, B = extensive_to_strategic_form(game)
	solve_strategic_form(A.tolist(), B.tolist())

def matching_pennies():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 2)
	

	curr3 = bt.addChild(curr, 3)
	curr3.set_payoffs([1,-1])
	curr4 = bt.addChild(curr, 3)
	curr4.set_payoffs([-1,1])
	
	curr5 = bt.addChild(curr2, 3)
	curr5.set_payoffs([-1,1])
	curr6 = bt.addChild(curr2, 3)
	curr6.set_payoffs([1,-1])

	game = Game(2, bt)
	A, B = extensive_to_strategic_form(game)
	solve_strategic_form(A.tolist(), B.tolist())

def matching_pennies_sequence():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 2)
	

	curr3 = bt.addChild(curr, 3)
	curr3.set_payoffs([1,-1])
	curr4 = bt.addChild(curr, 3)
	curr4.set_payoffs([-1,1])
	
	curr5 = bt.addChild(curr2, 3)
	curr5.set_payoffs([-1,1])
	curr6 = bt.addChild(curr2, 3)
	curr6.set_payoffs([1,-1])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	return A, B, E, F, e, f

def test3_strategic():
	bt = Tree()

	# Depth 0
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	# Depth 1
	curr = bt.addChild(bt.root(), 1)
	curr2 = bt.addChild(bt.root(), 2)
	
	curr.set_information_set(2,2)
	curr2.set_information_set(2,2)

	# Depth 2
	curr3 = bt.addChild(curr, 3)
	curr4 = bt.addChild(curr, 4)
	curr5 = bt.addChild(curr2, 5)
	curr6 = bt.addChild(curr2, 6)

	curr3.set_information_set(1,2)
	curr4.set_information_set(1,2)
	curr5.set_information_set(1,3)
	curr6.set_information_set(1,3)

	# Depth 3
	curr7 = bt.addChild(curr3, 7)
	curr8 = bt.addChild(curr3, 8)
	curr9 = bt.addChild(curr4, 9)
	curr10 = bt.addChild(curr4, 10)
	curr11 = bt.addChild(curr5, 11)
	curr12 = bt.addChild(curr5, 12)
	curr13 = bt.addChild(curr6, 13)
	curr14 = bt.addChild(curr6, 14)

	# Set payoffs
	curr7.set_payoffs([1,-1])
	curr8.set_payoffs([2,-2])
	curr9.set_payoffs([3,-3])
	curr10.set_payoffs([4,-4])
	curr11.set_payoffs([5,-5])
	curr12.set_payoffs([6,-6])
	curr13.set_payoffs([7,-7])
	curr14.set_payoffs([8,-8])

	game = Game(2, bt)
	A, B = extensive_to_strategic_form(game)
	solve_strategic_form(A.tolist(), B.tolist())

def von_stengel_test():
	bt = Tree()
	bt.addRoot(0)
	
	curr = bt.addChild(bt.root(), 1)
	curr2 = bt.addChild(bt.root(), 2)
	
	curr2.set_payoffs([3,3])

	bt.root().set_information_set(1,1)

	curr3 = bt.addChild(curr, 3)
	curr4 = bt.addChild(curr, 4)

	curr3.set_information_set(2,2)
	curr4.set_information_set(2,2)

	curr5 = bt.addChild(curr3, 5)

	curr5.set_payoffs([2,2])
	curr6 = bt.addChild(curr3, 6)
	curr6.set_payoffs([0,3])

	curr5.set_information_set(1,3)
	curr6.set_information_set(1,3)

	curr7 = bt.addChild(curr4, 7)

	curr7.set_payoffs([5,6])
	curr8 = bt.addChild(curr4, 8)
	curr8.set_payoffs([6,1])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)

	# Test arrays are what they ought be
	np.testing.assert_array_equal(A,
		np.array([[0,0,0],[0,0,0],[3,0,0],[0,2,5],[0,0,6]]))
	np.testing.assert_array_equal(B,
		np.array([[0,0,0],[0,0,0],[3,0,0],[0,2,6],[0,3,1]]))
	np.testing.assert_array_equal(E,
		np.array([[1,0,0,0,0],[-1,1,1,0,0],[0,-1,0,1,1]]))
	np.testing.assert_array_equal(F,
		np.array([[1,0,0],[-1,1,1]]))
	np.testing.assert_array_equal(e,
		np.array([[1],[0],[0]]))
	np.testing.assert_array_equal(f,
		np.array([[1],[0]]))

	return A, B, E, F, e, f 

def test2(): 
	t = Tree()
	t.addRoot(0)
	t.root().set_information_set(1,1)

	# Depth 1
	curr = t.addChild(t.root(),1)
	curr2 = t.addChild(t.root(),2)
	
	curr.set_information_set(2,2)
	curr2.set_information_set(2,2)

	# Depth 2
	curr3 = t.addChild(curr2, 3)
	curr4 = t.addChild(curr2, 4)
	curr5 = t.addChild(curr2, 5)
	
	curr3.set_information_set(1,2)
	curr5.set_information_set(1,2)

	# Depth 3
	curr6 = t.addChild(curr3, 6)
	curr7 = t.addChild(curr3, 7)
	curr8 = t.addChild(curr5, 8)
	
	# Set payoffs
	curr.set_payoffs([1,-1])
	curr6.set_payoffs([2,-2])
	curr7.set_payoffs([3,-3])
	curr4.set_payoffs([4,-4])
	curr8.set_payoffs([5,-5])

	game = Game(2, t)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	
	# Test arrays are what they ought be
	np.testing.assert_array_equal(A,
		np.array([[0,0,0,0],[1,0,0,0],[0,0,4,0],[0,2,0,5],[0,3,0,0]]))
	np.testing.assert_array_equal(B,
		np.array([[0,0,0,0],[-1,0,0,0],[0,0,-4,0],[0,-2,0,-5],[0,-3,0,0]]))
	np.testing.assert_array_equal(E,
		np.array([[1,0,0,0,0],[-1,1,1,0,0],[0,0,-1,1,1]]))
	np.testing.assert_array_equal(F,
		np.array([[1,0,0,0],[-1,1,1,1]]))
	np.testing.assert_array_equal(e,
		np.array([[1],[0],[0]]))
	np.testing.assert_array_equal(f,
		np.array([[1],[0]]))
	
	return A, B, E, F, e, f 

def test3():
	bt = Tree()

	# Depth 0
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	# Depth 1
	curr = bt.addChild(bt.root(), 1)
	curr2 = bt.addChild(bt.root(), 2)
	
	curr.set_information_set(2,2)
	curr2.set_information_set(2,2)

	# Depth 2
	curr3 = bt.addChild(curr, 3)
	curr4 = bt.addChild(curr, 4)
	curr5 = bt.addChild(curr2, 5)
	curr6 = bt.addChild(curr2, 6)

	curr3.set_information_set(1,2)
	curr4.set_information_set(1,2)
	curr5.set_information_set(1,3)
	curr6.set_information_set(1,3)

	# Depth 3
	curr7 = bt.addChild(curr3, 7)
	curr8 = bt.addChild(curr3, 8)
	curr9 = bt.addChild(curr4, 9)
	curr10 = bt.addChild(curr4, 10)
	curr11 = bt.addChild(curr5, 11)
	curr12 = bt.addChild(curr5, 12)
	curr13 = bt.addChild(curr6, 13)
	curr14 = bt.addChild(curr6, 14)

	# Set payoffs
	curr7.set_payoffs([1,-1])
	curr8.set_payoffs([2,-2])
	curr9.set_payoffs([3,-3])
	curr10.set_payoffs([4,-4])
	curr11.set_payoffs([5,-5])
	curr12.set_payoffs([6,-6])
	curr13.set_payoffs([7,-7])
	curr14.set_payoffs([8,-8])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	
	# Test arrays are what they ought be
	np.testing.assert_array_equal(A,
		np.array([[0, 0, 0],[0,0,0],[0,0,0],[0,1,3],[0,2,4],[0,5,7],[0,6,8]]))
	np.testing.assert_array_equal(B,
		np.array([[0, 0, 0],[0,0,0],[0,0,0],[0,-1,-3],[0,-2,-4],[0,-5,-7],[0,-6,-8]]))
	np.testing.assert_array_equal(E,
		np.array([[1,0,0,0,0,0,0],[-1,1,1,0,0,0,0],[0,-1,0,1,1,0,0],[0,0,-1,0,0,1,1]]))
	np.testing.assert_array_equal(F,
		np.array([[1,0,0],[-1,1,1]]))
	np.testing.assert_array_equal(e,
		np.array([[1],[0],[0],[0]]))
	np.testing.assert_array_equal(f,
		np.array([[1],[0]]))

	return A, B, E, F, e, f 

def test4():
	bt = Tree()

	# Depth 0
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	# Depth 1
	curr = bt.addChild(bt.root(), 1)
	curr2 = bt.addChild(bt.root(), 2)
	
	curr.set_information_set(2,2)

	# Depth 2
	curr3 = bt.addChild(curr, 3)
	curr4 = bt.addChild(curr, 4)
	curr5 = bt.addChild(curr, 5)
	curr6 = bt.addChild(curr, 6)

	curr3.set_information_set(1,2)
	curr5.set_information_set(1,2)

	# Depth 3
	curr7 = bt.addChild(curr3, 7)
	curr8 = bt.addChild(curr3, 8)
	curr9 = bt.addChild(curr3, 9)
	curr10 = bt.addChild(curr5, 10)
	curr11 = bt.addChild(curr5, 11)
	
	curr9.set_information_set(2,3)
	curr10.set_information_set(2,4)

	# Depth 4
	curr12 = bt.addChild(curr9, 12)
	curr13 = bt.addChild(curr10, 13)
	curr14 = bt.addChild(curr10, 14)

	curr14.set_information_set(1,14)

	# Depth 5
	curr15 = bt.addChild(curr14, 15)
	curr16 = bt.addChild(curr14, 16)

	# Set payoffs
	curr7.set_payoffs([1,-1])
	curr8.set_payoffs([-1,1])
	curr12.set_payoffs([2,-2])
	curr4.set_payoffs([3,-3])
	curr13.set_payoffs([4,-4])
	curr15.set_payoffs([5,-5])
	curr16.set_payoffs([-5,5])
	curr11.set_payoffs([6,-6])
	curr6.set_payoffs([7,-7])
	curr2.set_payoffs([8,-8])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)

	# Test arrays are what they ought be
	np.testing.assert_array_equal(A,
		np.array([[0,0,0,0,0,0,0,0],[0,0,3,0,7,0,0,0],[8,0,0,0,0,0,0,0],[0,1,0,0,0,0,4,0],[0,-1,0,6,0,0,0,0],[0,0,0,0,0,2,0,0],[0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,-5]]))
	np.testing.assert_array_equal(B,-A)
	np.testing.assert_array_equal(E,
		np.array([[1,0,0,0,0,0,0,0],[-1,1,1,0,0,0,0,0],[0,-1,0,1,1,1,0,0],[0,0,0,-1,0,0,1,1]]))
	np.testing.assert_array_equal(F,
		np.array([[1,0,0,0,0,0,0,0],[-1,1,1,1,1,0,0,0],[0,-1,0,0,0,1,0,0],[0,0,0,-1,0,0,1,1]]))
	np.testing.assert_array_equal(e,
		np.array([[1],[0],[0],[0]]))
	np.testing.assert_array_equal(f,
		np.array([[1],[0],[0],[0]]))

	return A, B, E, F, e, f

############## Checking NE vs. SPE ###########
def dif1():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_payoffs([5,-5])
	#curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 2)
	curr3 = bt.addChild(curr2, 3)
	curr3.set_payoffs([3,-3])
	curr4 = bt.addChild(curr2, 4)
	curr4.set_payoffs([2,-2])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	return A, B, E, F, e, f 

def dif2():
	bt = Tree()
	bt.addRoot(0)
	bt.root().set_information_set(1,1)
	
	curr = bt.addChild(bt.root(), 1)
	curr.set_payoffs([5,-5])
	#curr.set_information_set(2, 2)
	curr2 = bt.addChild(bt.root(), 2)
	curr2.set_information_set(2, 2)
	curr3 = bt.addChild(curr2, 3)
	curr3.set_payoffs([3,-3])
	curr4 = bt.addChild(curr2, 4)
	curr4.set_payoffs([2,-2])

	game = Game(2, bt)
	A, B, E, F, e, f = extensive_to_sequence_form(game)
	return A, B, E, F, e, f 

def print_results(A, B, E, F, e, f):
	'''
	Input: Matrices of solved game tree
	Function: Prints matrices to console
	Output: None
	'''
	print('Player One Payoff Matrix (A):')
	print(A)
	print('Player Two Payoff Matrix (B):')
	print(B)
	print('Player One Constraints (E):')
	print(E)
	print('Player Two Constraints (F):')
	print(F)
	print('Player One Vector (e):')
	print(e)
	print('Player Two Vector (f):')
	print(f)

def get_sequence_tests():
    #return [von_stengel_test, test2, test3, test4, matching_pennies_sequence, dif1]
    return [matching_pennies_sequence, dif1]

def get_strategic_tests():
	return [strategic_form_test, strategic_big_test, matching_pennies]

# The mainline runs all of the test functions in the list returned by get_tests
if __name__ == '__main__' :
	print('Running sequence form tests...')
	for test in get_sequence_tests():
		print('====== ' + str(test.__name__) + ' ======')
		A, B, E, F, e, f = test()
		print_results(A, B, E, F, e, f)
		solve_sequence_form(A,B,E,F,e,f)
	print('All tests passed!')

	# print('Running strategic form tests...')
	# for test in get_strategic_tests():
	# 	print('====== ' + str(test.__name__) + ' ======')
	# 	test()
	# print('All tests passed!')