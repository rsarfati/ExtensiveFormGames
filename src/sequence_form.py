#! /usr/bin/python
import numpy as np
import traversals
from game import *
from tree import *
import queue
import itertools as it
from scipy.optimize import linprog
import lemkelcp as lcp

def extensive_to_strategic_form(game):
	''' 
	Input: Game tree
	Output: Matrices A,B necessary to compute equilibria
	 		(via your favorite algorithm for solving LPs)
	'''
	n_players = game.n_players
	bt = game.tree

	if (n_players != 2):
		raise IOError('This implementation is not going to work without 2 players.')

	root = bt.root()
	depth = bt.height()

	nodes = bt.getNodes()

	a_moves = {}
	b_moves = {}

	for node in nodes:
		if node.hasChildren():
			if (node.information_set[0] == 1):
				if node.information_set[1] not in a_moves.keys():
					a_moves[node.information_set[1]] = set(range(len(node.children())))
			elif (node.information_set[0] is not None):
				if node.information_set[1] not in b_moves.keys():
					b_moves[node.information_set[1]] = set(range(len(node.children())))

	a_strategies = list(it.product(*[list(a_moves[inf]) for inf in a_moves.keys()]))
	b_strategies = list(it.product(*[list(b_moves[inf]) for inf in b_moves.keys()]))

	A = np.zeros((len(a_strategies), len(b_strategies)))
	B = np.zeros((len(a_strategies), len(b_strategies)))

	for i in range(A.shape[0]):
		for j in range(B.shape[1]):
			
			# Establish path from the root
			cur_seq_a = a_strategies[i]
			cur_seq_b = b_strategies[j]

			path = [None]*(len(cur_seq_a) + len(cur_seq_b))
			
			if ((len(cur_seq_b) == 0) and (len(cur_seq_a) == 1)):
				path = cur_seq_a
			else:
				if not is_valid_path(cur_seq_a, cur_seq_b):
					path = []
				elif (len(cur_seq_a) == 1):
					path[0] = cur_seq_a[0]
					path[1] = cur_seq_b[0]
				else:
					path[::2] = cur_seq_a
					path[1::2] = cur_seq_b

			cur_node = root

			for bend in path:
				# If turn is valid, continue down path from root
				if bend < len(bt.children(cur_node)):
					cur_node = bt.children(cur_node)[bend]
				# If invalid, then path does not exist in tree; payoffs 0
				else:
					break

			# Payoffs are 0 if not at leaf, or node doesn't exist
			if (cur_node.payoffs == None):
				A[i][j] = 0
				B[i][j] = 0
			else:
				A[i][j] = cur_node.payoffs[0]
				B[i][j] = cur_node.payoffs[1]

	print(A)
	print(B)

	##### Correlated Equilibrium Coefficients ####
	return A, B

def solve_strategic_form(aMatrix, bMatrix):
	aH, aL = len(aMatrix), len(aMatrix[0])
	nvpp = aH * aL

	A_lb = []
	b_lb = []

	perms = list(it.permutations(list(range(aH)), 2))
	for perm in perms:
		row = nvpp * [0]

		ind = perm[0]
		jnd = perm[1]

		for i in range(aL):
			value = -(aMatrix[ind][i] - aMatrix[jnd][i])
			row[ind * aL + i] = value

		A_lb.append(row)
		b_lb.append(0)

	perms = list(it.permutations(list(range(aL)), 2))
	for perm in perms:
		row = nvpp * [0]

		ind = perm[0]
		jnd = perm[1]

		for i in range(aH):
			value = -(bMatrix[i][ind] - bMatrix[i][jnd])
			row[ind + i * aL] = value

		A_lb.append(row)
		b_lb.append(0)

	A_lb.append(nvpp * [1])
	b_lb.append(1)

	A_eq = [[1] * nvpp]
	b_eq = [1]

	# for row in A_lb:
	# 	print(row)
	# print(b_lb)

	onlyBound = (0, None)
	bounds = [onlyBound] * nvpp
	bounds = tuple(bounds)

	obj = [0] * nvpp
	for i in range(aH):
		for j in range(aL):
			aVal = -aMatrix[i][j]
			bVal = -bMatrix[i][j]
			
			obj[i * aL + j] = aVal + bVal

	#print(obj)

	result = linprog(obj, A_eq=A_eq, b_eq=b_eq, A_ub=A_lb, b_ub = b_lb, bounds=bounds, options={"disp": True})

	print(result)

def solve_sequence_form(A,B,E,F,e,f):
	# Solves for player 1
	v_len = F.shape[0]
	x_len = A.shape[0]

	# Pads zeros onto /columns/
	c = - np.pad(f.T, ((0,0),(0, x_len)), mode='constant').T
	add_to_one = np.concatenate([np.zeros(v_len), np.ones(x_len)], axis=0)
	A_eq = np.pad(E, ((0,0),(v_len, 0)), mode='constant')
	b_eq = e

	A_ub = (np.pad(F.T, ((0,0),(0, x_len)), mode='constant') - \
			np.pad(A.T, ((0,0),(v_len, 0)), mode='constant'))

	b_ub = np.zeros(A_ub.shape[0])

	vBound = (None, None)
	xBound = (0, None)
	bounds = [vBound] * v_len + [xBound] * x_len
	bounds = tuple(bounds)

	result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub = b_ub, bounds=bounds, method='interior-point',options={"disp": True})

	print("===== PLAYER 1 =====")
	print(result)

	
	#sol = lcp(E.T, np.dot(A,))

def decorate_sequences(bt):
    """ decorate_sequences: tree -> list[Node]
    Purpose:  	Runs a breadth first search on a binary tree
    Consumes: 	Binary tree object
    Produces: 	List of Nodes in breadth first search order, 
    			with all nodes decorated with sequence of nodes
    			on path from root to themselves (defined as '0' if 
    			descend to left right child, '1' o/w)

    Example: 
	                    A 
	    breadthfirst(  / \  ) -> [A, B, C, D, E]
	                  B   C 
	                 / \
	                D   E
        Where A.node_sequence_a = [], B.node_sequence_a = [0], 
        c.node_sequence_a = [1], d.node_sequence_b = [0,0], 
        E.node_sequence_b = [0,1].

    If tree is empty, should return an empty list. If the tree
    is null, throws InvalidInputException. 
    """
    if bt is None:
        raise InvalidInputException("Input is None")
    if bt.isEmpty():
        return []

    Q = queue.Queue()
    qlist = []
    qlist.append(bt.root())
    Q.put(bt.root())

    while not Q.empty():
        node = Q.get()
        
        if (node.depth() == 1):
        	node.sequence_a.append(bt.children(bt.parent(node)).index(node))
        elif (node.depth() > 1):
        	if (node.depth() % 2 == 1):
	        	node.sequence_a = [turn for turn in bt.parent(node).sequence_a]
	        	node.sequence_a.append(bt.children(bt.parent(node)).index(node))
	        	node.sequence_b = [turn for turn in bt.parent(node).sequence_b]
	        else:
	        	node.sequence_b = [turn for turn in bt.parent(node).sequence_b]
	        	node.sequence_b.append(bt.children(bt.parent(node)).index(node))
	        	node.sequence_a = [turn for turn in bt.parent(node).sequence_a]
	        	
        if bt.hasChildren(node):
            for child in bt.children(node):
            	Q.put(child)
            	qlist.append(child)

    return qlist

def is_valid_path(seq_a, seq_b):
	''' 
	Input: Player A and Player B's proposed sequences
	Output: Returns false if path isn't possible
	'''
	if (len(seq_a) > len(seq_b) + 1):
		return False
	
	if (len(seq_b) > len(seq_a)):
		return False

	return True

def node_successors(i, list_sequences):
	''' 
	Input: Index and list of player's sequences
	Output: List of indices of direct successors in sequence (or empty list if none)
	'''
	if (i >= len(list_sequences) - 1):
		return []
	cur_seq = list_sequences[i]

	return [k for k in range(i+1, len(list_sequences)) \
			if ((cur_seq == list_sequences[k][:len(cur_seq)]) and \
				(len(list_sequences[k]) == len(cur_seq) + 1))]

def extensive_to_sequence_form(game):
	''' 
	Input: Game tree
	Output: Matrices A,B,E,e,F,f necessary to compute equilibria
	 		(via your favorite algorithm for solving LPs)
	'''
	n_players = game.n_players
	bt = game.tree

	if (n_players != 2):
		raise IOError('This implementation is not going to work without 2 players.')

	root = bt.root()
	depth = bt.height()

	nodes = decorate_sequences(bt)

	A_sequences = np.array(sorted(np.unique(np.array([node.sequence_a for node in nodes])), key=len))
	B_sequences = np.array(sorted(np.unique(np.array([node.sequence_b for node in nodes])), key=len))

	A = np.zeros((A_sequences.size, B_sequences.size))
	B = np.zeros((A_sequences.size, B_sequences.size))

	for i in range(A.shape[0]):
		for j in range(B.shape[1]):
			
			# Establish path from the root
			cur_seq_a = A_sequences[i]
			cur_seq_b = B_sequences[j]

			path = [None]*(len(cur_seq_a) + len(cur_seq_b))
			
			if ((len(cur_seq_b) == 0) and (len(cur_seq_a) == 1)):
				path = cur_seq_a
			else:
				if not is_valid_path(cur_seq_a, cur_seq_b):
					path = []
				elif (len(cur_seq_a) == 1):
					path[0] = cur_seq_a[0]
					path[1] = cur_seq_b[0]
				else:
					path[::2] = cur_seq_a
					path[1::2] = cur_seq_b

			cur_node = root

			for bend in path:
				# If turn is valid, continue down path from root
				if bend < len(bt.children(cur_node)):
					cur_node = bt.children(cur_node)[bend]
				# If invalid, then path does not exist in tree; payoffs 0
				else:
					cur_node = None
					break

			# Payoffs are 0 if not at leaf, or node doesn't exist
			if (cur_node == None or cur_node.payoffs == None):
				A[i][j] = 0
				B[i][j] = 0
			else:
				A[i][j] = cur_node.payoffs[0]
				B[i][j] = cur_node.payoffs[1]

	##### Now solving for E, e, F, f #########
	U_1 = np.unique(np.array([node.information_set \
			for node in nodes if node.information_set[0]==1]))
	U_2 = np.unique(np.array([node.information_set \
			for node in nodes if node.information_set[0]==2]))

	E = np.zeros((U_1.shape[0] + 1, A_sequences.size))
	F = np.zeros((U_2.shape[0] + 1, B_sequences.size))
	
	E[0][0], F[0][0] = 1, 1

	# Populate E
	for i in range(1, E.shape[0]):
		k = i-1
		col_seq = A_sequences[k]
		while not len(node_successors(k, A_sequences)):
			k += 1
		E[i][k] = -1
		for index in node_successors(k, A_sequences):
			E[i][index] = 1

	# Populate F
	for i in range(1, F.shape[0]):
		k = i-1
		col_seq = B_sequences[k]
		while not len(node_successors(k, B_sequences)):
			k += 1
		F[i][k] = -1
		for index in node_successors(k, B_sequences):
			F[i][index] = 1

	# Populate e, f
	e = np.zeros((U_1.shape[0]+1,1))
	f = np.zeros((U_2.shape[0]+1,1))
	e[0][0] = 1
	f[0][0] = 1
	
	return A,B,E,F,e,f
