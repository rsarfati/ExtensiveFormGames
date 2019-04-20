#!/usr/bin/python
# tree.py

""" Tree module
Implement a node-and-link based Tree structure
"""
import queue
from queue import *
import string
from io import StringIO
import io

class EmptyTreeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidInputException(Exception): 
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TreeNode:

    def __init__(self, parent, value):
        """
        Input: Node (implicit argument), parent: Node, value: anything
        Output: a Node with a parent node and a value
        Purpose: constructor for a Node
        """
        self.n_parent = parent
        self.n_value = value
        self.payoffs = None
        
        # Store as "(player, infset)"
        self.information_set = (None,None)
        self.n_children = []
        self.sequence_a = []
        self.sequence_b = []

        if self.n_parent is None:
            self.n_depth = 0 
        else:
            self.n_depth = parent.depth() + 1

    def set_information_set(self, player, inf_set):
        self.information_set = (player,inf_set)

    def set_payoffs(self, new_payoffs):
        self.payoffs = new_payoffs
        
    def parent(self):
        """
        Input: Node (implicit argument)
        Output: Node
        Purpose: get the parent of this Node (if possible)
        """
        if self.n_parent is not None:
            return self.n_parent
        return None

    def children(self):
        """
        Input: Node (implicit argument)
        Output: Node
        Purpose: get list of children (if possible)
        """
        return self.n_children

    def addChild(self, value):
        """
        Input: Node (implicit argument), value: anything
        Output: Node
        Purpose: add a child to this node
        """
        child = TreeNode(self,value)
        self.n_children.append(child)
        return child
    
    def hasChildren(self):
        """
        Input: Node (implicit argument)
        Output: boolean
        Purpose: return whether this node has a left child
        """
        if self.n_children is not []:
            return True
        return False
    
    def value(self):
        """
        Input: Node (implicit argument)
        Output: anything
        Purpose: return the value stored at this Node
        """
        return self.n_value
    
    def depth(self):
        """
        Input: Node (implicit argument)
        Output: int
        Purpose: return the depth of this node in the tree in O(1)
        """
        return self.n_depth

    def __str__(self):
        """
        Input: Node (implicit argument)
        Output: String representation of the Node
        Purpose: printing
        """
        output = ""
        output += "(val: "
        output += repr(self.value())
        count = 0
        output += "; "+str(count)+": "
        if self.hasChildren():
            for i in self.n_children:
                output += "; "+str(i)+": "
                output += str(self.n_children[i])
        else:
            output += "<nothing>"
        output += ")"
        return output

class Tree:
    """ Generic Tree class

    Implement a node-and-link based Tree structure

    Author: rsarfati
    Date: 4 Mar 2018
    """

    def __init__(self):
        """
        Input: Tree (implicit argument)
        Output: Tree
        Purpose: Creates an empty tree
        """
        self.t_root = None
        self.t_size = 0
        self.t_height = 0
                
    def root(self): 
        """
        Input: Tree (implicit argument)
        Output: Node
        Purpose: return the root node 
        Throw a EmptyTreeException if the tree is empty
        """
        if self.isEmpty():
            raise EmptyTreeException("Tree is empty")

        return self.t_root
            
    def parent(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: Node
        Purpose: return the parent node
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        return node.n_parent
            
    def children(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: List of child nodes
        Purpose: returns a list of child nodes
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        return node.n_children

    def getNodes(self):
        """
        Input: Tree (implicit argument), node: Node
        Output: List of nodes
        Purpose: returns a list of all nodes
        """
        Q = queue.Queue()
        root = self.root()
        out = []
        out.append(root)
        Q.put(root)
        while not Q.empty():
            node = Q.get()
            if self.hasChildren(node):
                for child in self.children(node):
                    Q.put(child)
                    out.append(child)
        return out
    
    def isEmpty(self):
        """
        Input: Tree (implicit argument)
        Output: boolean
        Purpose: return true if the tree is empty, false otherwise in O(1)
        """
        if self.t_root is None:
            return True
        return False
    
    def size(self):
        """
        Input: Tree (implicit argument)
        Output: int
        Purpose: return the size of the tree in O(1)
        """
        return self.t_size

    def height(self):
        """
        Input: Tree (implicit argument)
        Output: int
        Purpose: return the height of the tree in O(1) time
        Exceptions: throw an EmptyTreeException if the height is undefined
        """
        if self.isEmpty():
            raise EmptyTreeException("Tree is empty, height undefined")

        return self.t_height

    def isInternal(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node is internal.
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is not None:
            if node.hasLeft() or node.hasRight():
                return True
        return False

    def isExternal(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node is external.
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is None:
            return True
        if not node.hasLeft() and not node.hasRight():
            return True
        return False

    def isRoot(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node is the root
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is None:
            return True
        return False

    def hasChildren(self, node):
        """
        Input: Tree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node has a right child
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        return node.n_children is not []

    def addRoot(self, e):
        """
        Input: Tree (implicit argument), e: anything
        Output: Node (the root node)
        Purpose: add a root to the tree only if there isn't one already and return it.
                 If there is one already, just return it
        """
        if self.t_root is None:
            self.t_root = TreeNode(None, e)
            self.t_size += 1
        return self.t_root

    def addChild(self, node, e):
        """
        Input: Tree (implicit argument), node: Node, e: anything
        Output: the right child of the node
        Purpose: add a right child to the node only if there isn't one already and return it.
                 If there is one already, return it
        Exceptions: throw an InvalidInputException if node input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")
        
        child = TreeNode(node,e)
        node.n_children.append(child)

        self.t_size += 1
        if child.n_depth > self.t_height:
            self.t_height = child.n_depth
        
        return child
        
    def __str__(self):
        """
        Input: Tree (implicit argument)
        Output: String representation of Tree
        Purpose: printing
        """
        toReturn = 'Size: ' + str(self.size()) + '\n'
        toReturn += 'Height: ' + str(self.height()) + '\n'
        toReturn += str(self.root()) 
        return toReturn

