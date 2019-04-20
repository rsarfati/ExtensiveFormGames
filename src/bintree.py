#!/usr/bin/python
# bintree.py
""" Binary Tree module

Implement a node-and-link based Binary Tree structure

"""
from queue import *
import string
from io import StringIO
import io

class EmptyBinTreeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidInputException(Exception): 
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Node:

    def __init__(self, parent, value) :
        """
        Input: Node (implicit argument), parent: Node, value: anything
        Output: a Node with a parent node and a value
        Purpose: constructor for a Node
        """
        self.n_parent = parent
        self.n_value = value
        self.payoffs = None
        self.information_set = (None,None)
        self.sequence_a = []
        self.sequence_b = []
        
        self.n_left = None
        self.n_right = None

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

    def left(self):
        """
        Input: Node (implicit argument)
        Output: Node
        Purpose: get the left child of this node (if possible)
        """
        if self.hasLeft():
            return self.n_left
        return None

    def right(self):
        """
        Input: Node (implicit argument)
        Output: Node
        Purpose: get the right child of this node (if possible)
        """
        if self.hasRight():
            return self.n_right
        return None

    def addLeft(self, value) :
        """
        Input: Node (implicit argument), value: anything
        Output: Node (the left child)
        Purpose: add a left child to this node with the given value if there isn't one already and return it.
                If there is one already, just return it
        """
        if not self.hasLeft():
            self.n_left = Node(self, value)
        return self.n_left

    def addRight(self, value) :
        """
        Input: Node (implicit argument), value: anything
        Output: Node (the right child)
        Purpose: add a right child to this node with the given value if there isn't one already and return it.
                 If there is one already, just return it
        """
        if not self.hasRight():
            self.n_right = Node(self, value)
        return self.n_right
    
    def hasLeft(self):
        """
        Input: Node (implicit argument)
        Output: boolean
        Purpose: return whether this node has a left child
        """
        if self.n_left is not None:
            return True
        return False
    
    def hasRight(self):
        """
        Input: Node (implicit argument)
        Output: boolean
        Purpose: return whether the node has a right child
        """
        if self.n_right is not None:
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
        output += "; L: "
        if self.hasLeft():
            output += str(self.left())
        else:
            output += "<nothing>"
        output += "; R: "
        if self.hasRight():
            output += str(self.right())
        else:
            output += "<nothing>"
        output += ")"
        return output

class BinTree:
    """ Binary Tree class

    Implement a node-and-link based Binary Tree structure

    Author: rsarfati
    Date: 4 Mar 2016
    """

    def __init__(self) :
        """
        Input: BinTree (implicit argument)
        Output: BinTree
        Purpose: Creates an empty binary tree
        """
        self.t_root = None
        self.t_size = 0
        self.t_height = 0
                
    def root(self): 
        """
        Input: BinTree (implicit argument)
        Output: Node
        Purpose: return the root node 
        Throw a EmptyBinTreeException if the tree is empty
        """
        if self.isEmpty():
            raise EmptyBinTreeException("Tree is empty")

        return self.t_root
            
    def parent(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: Node
        Purpose: return the parent node
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        return node.parent()
            
    def children(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: List of child nodes
        Purpose: returns a list of child nodes
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        n_children = []
        if node.hasLeft():
            n_children.append(node.left())
        if node.hasRight():
            n_children.append(node.right())

        return n_children
    
    def isEmpty(self):
        """
        Input: BinTree (implicit argument)
        Output: boolean
        Purpose: return true if the tree is empty, false otherwise in O(1)
        """
        if self.t_root is None:
            return True
        return False
    
    def size(self):
        """
        Input: BinTree (implicit argument)
        Output: int
        Purpose: return the size of the tree in O(1)
        """
        return self.t_size

    def height(self):
        """
        Input: BinTree (implicit argument)
        Output: int
        Purpose: return the height of the tree in O(1) time
        Exceptions: throw an EmptyBinTreeException if the height is undefined
        """
        if self.isEmpty():
            raise EmptyBinTreeException("Tree is empty, height undefined")

        return self.t_height

    def isInternal(self, node):
        """
        Input: BinTree (implicit argument), node: Node
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
        Input: BinTree (implicit argument), node: Node
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
        Input: BinTree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node is the root
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is None:
            return True
        return False

    def left(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: Node
        Purpose: get the left child of the node (if possible)
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.hasLeft():
            return node.left()
        return None

    def right(self, node): 
        """
        Input: BinTree (implicit argument), node: Node
        Output: Node
        Purpose: get the right child of the node (if possible)
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.hasRight():
            return node.right()
        return None

    def isLeft(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: Node
        Purpose: get the right child of the node (if possible)
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if self.parent(node).hasLeft():
            if (self.left(self.parent(node)) == node):
                return 1
        return 0

    def isRight(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: Node
        Purpose: get the right child of the node (if possible)
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if self.parent(node).hasRight():
            if (self.right(self.parent(node)) == node):
                return 1
        return 0

    def hasLeft(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node has a left child
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.hasLeft():
            return True
        return False

    def hasRight(self, node):
        """
        Input: BinTree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node has a right child
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.hasRight():
            return True
        return False

    def addRoot(self, e):
        """
        Input: BinTree (implicit argument), e: anything
        Output: Node (the root node)
        Purpose: add a root to the tree only if there isn't one already and return it.
                 If there is one already, just return it
        """
        if self.t_root is None:
            self.t_root = Node(None, e)
            self.t_size += 1
        return self.t_root

    def addLeft(self, node, e):
        """
        Input: BinTree (implicit argument), node: Node, e: anything
        Output: the left child of the node
        Purpose: add a left child to the node only if there isn't one already and return it.
                 If there is one already, just return it
        Exceptions: throw an InvalidInputException if node input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.hasLeft():
            return node.left()
        
        node.addLeft(e)
        self.t_size += 1
        if node.left().depth() > self.t_height:
            self.t_height = node.left().depth()
        return node.left()

    def addRight(self, node, e):
        """
        Input: BinTree (implicit argument), node: Node, e: anything
        Output: the right child of the node
        Purpose: add a right child to the node only if there isn't one already and return it.
                 If there is one already, return it
        Exceptions: throw an InvalidInputException if node input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if self.hasRight(node):
            return node.right()
        
        node.addRight(e)

        self.t_size += 1
        if node.right().depth() > self.t_height:
            self.t_height = node.right().depth()
        
        return node.right()
        
    def __str__(self):
        """
        Input: BinTree (implicit argument)
        Output: String representation of BinTree
        Purpose: printing
        """
        toReturn = 'Size: ' + str(self.size()) + '\n'
        toReturn += 'Height: ' + str(self.height()) + '\n'
        toReturn += str(self.root()) 
        return toReturn

 
    def getheight(self, node):
        if not node:
            return 0
        else:
            return max(getheight(node.left), getheight(node.right)) + 1
     
    def add_padding(self, ipstr, pad_length):
        ipstr = ipstr.strip()
        padding = ' ' * (pad_length - len(ipstr))
        return ''.join([padding, ipstr])
     
    # def show(self, root):
    #     max_pretty_print_height = 7
    #     output = io.StringIO()
    #     keys = []
    #     if root:
    #         current_level = Queue()
    #         next_level = Queue()
    #         current_level.put(self.root)
    #         depth = 0
    #         while not current_level.empty():
    #             current_node = current_level.get()
    #             output.write('%s ' % current_node.value() if current_node else 'NUL ') 
    #             next_level.put(current_node.left if current_node else current_node)
    #             next_level.put(current_node.right if current_node else current_node)
     
    #             if current_level.empty():
    #                 if sum([i is not None for i in next_level.a]):
    #                     current_level, next_level = next_level, current_level
    #                     depth = depth + 1
    #                 output.write('\n')
     
    #     if getheight(root) == 0:
    #         skip_start = spaces * pad_length
    #         skip_mid = (2 * spaces - 1) * pad_length
     
    #         key_start_spacing = ' ' * skip_start
    #         key_mid_spacing = ' ' * skip_mid
     
    #         keys = output.readline().split(' ')
    #         padded_keys = (self.add_padding(key, pad_length) for key in keys)
     
    #         padded_str = key_mid_spacing.join(padded_keys)
    #         complete_str = ''.join([key_start_spacing, padded_str])
     
    #         pretty_output.write(complete_str)
    #         current_depth = spaces
    #         spaces = spaces // 2
     
    #         if spaces > 0:
    #             pretty_output.write('\n')
     
    #             cnt = 0
    #             while cnt < current_depth:
    #                 inter_symbol_spacing = ' ' * (pad_length + 2 * cnt)
    #                 symbol = ''.join(['/', inter_symbol_spacing, '\\'])
    #                 symbol_start_spacing = ' ' * (skip_start-cnt-1)
    #                 symbol_mid_spacing = ' ' * (skip_mid-2*(cnt+1))
    #                 pretty_output.write(''.join([symbol_start_spacing, symbol]))
    #                 for i in keys[1:-1]:
    #                     pretty_output.write(''.join([symbol_mid_spacing, symbol]))
    #                 pretty_output.write('\n')
    #                 cnt = cnt + 1
    #     return pretty_output


    """ Helper methods for tree visualization. 
    You DON'T need to touch these """  

    def graphic(self):
        """Returns a representation of this graph as a .dot file.

        In other words, if you pass the string returned by this method into
        the program DOT (or, better yet, NEATO), you can get an image file
        of the graph."""
        strs = ["graph\n{\n"]
        
        def annex_vertex(v):
            strs.append("\t" + str(v.value()) + ";\n")

        def annex_edge(v):
            if v.hasLeft():
                strs.append("\t" + str(v.value()) + "--" + str(v.left().value()) + ";\n")
            if v.hasRight():
                strs.append("\t" + str(v.value()) + "--" + str(v.right().value()) + ";\n")

        self.parseVerts(annex_vertex, annex_edge)
        strs.append("}\n")
        return ''.join(strs)

    def popup(self):
        """Opens a new window with this graph rendered by DOT.
        Sequential calls to this function will show the window
        once at a time. """
        import os
        tmp = open("./.tmpgraph", "w+")
        tmp.write(self.graphic())
        tmp.close()
        os.system("dot ./.tmpgraph | display")


    def parseVerts(self, f1, f2):
        Q = Queue()
        Q.put(self.root())
        while not Q.empty():
            v = Q.get()
            f1(v)
            f2(v)
            if v.hasLeft():
                Q.put(v.left())
            if v.hasRight():
                Q.put(v.right())

