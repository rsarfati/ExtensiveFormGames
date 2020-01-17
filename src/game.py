import GameTree

class Game:

    def __init__(self, n_players, tree) :
        """
        Input: Node (implicit argument), parent: Node, value: anything
        Output: a Node with a parent node and a value
        Purpose: constructor for a Node
        """
        self.n_players = n_players
        self.tree = tree
    
    def size(self):
        """
        Input: Game (implicit)
        Output: int
        Purpose: return the size of this tree in the tree in O(1)
        """
        return self.tree.size()

    def depth(self):
        """
        Input: Game (implicit)
        Output: int
        Purpose: return the height of this tree in the tree in O(1)
        """
        return self.tree.height()

    def __str__(self):
        """
        Input: Game (implicit argument)
        Output: String representation of Game
        Purpose: printing
        """
        toReturn  = 'Num. Players: ' + str(self.n_players) + '\n'
        toReturn += 'Size: '         + str(self.size())    + '\n'
        toReturn += 'Height: '       + str(self.height())  + '\n'
        return toReturn

class Node:

    def __init__(self, parent, player, inf_set) :
        """
        Input:   Node (implicit argument), parent: Node, value: anything
        Output:  Node with a parent node and a value
        Purpose: Constructor for a Node
        """
        self.n_parent          = parent
        self.n_payoffs         = None
        self.n_player          = player
        self.n_information_set = inf_set
        self.n_children        = []

        if self.n_parent is None:
            # Vacuously first child
            self.n_id    = 1
            self.n_depth = 0 
            
            # Maps players to the sequences getting them to node
            self.n_sequences  = {} 
        else:
            self.n_id    = parent.num_children() + 1
            self.n_depth = parent.depth()        + 1
            
            # Maps players to the sequences getting them to node
            self.n_sequences = parent.n_sequences

            # The parent node's action got you here
            self.n_sequences[parent.n_player].append(self.n_id)

    def set_information_set(self, player, inf_set):
        self.information_set = (player, inf_set)

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

    def add_child(self, player, inf_set) :
        """
        Input: Node (implicit argument), value: anything
        Output: Node (the new child)
        Purpose: add a child to node with the given value if there isn't one already and return it.
                If there is one already, just return it
        """
        child = Node(self, player, inf_set)
        self.n_children.append(child)
        return child

    def get_children(self):
        return self.n_children

    def num_children(self):
        return length(self.n_children)
    
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
        output += "(Player: "
        output += repr(self.n_player)
        output += "; Information Set: "
        output += repr(self.n_information_set)

        for child in self.n_children
            output += "; " + child.n_id + ": "
            output += str(child)
        output += ")"
        return output

class GameTree:
    """ Game Tree Class

    A node-and-link based Game Tree structure.
    """

    def __init__(self) :
        """
        Input:  GameTree (implicit argument)
        Output: GameTree
        Purpose: Creates an empty binary tree
        """
        self.t_root   = None
        self.t_size   = 0
        self.t_height = 0
                
    def root(self): 
        """
        Input: GameTree (implicit argument)
        Output: Node
        Purpose: return the root node 
        Throw a EmptyGameTreeException if the tree is empty
        """
        if self.isEmpty():
            raise EmptyGameTreeException("Tree is empty")
        return self.t_root
            
    def parent(self, node):
        """
        Input: GameTree (implicit argument), node: Node
        Output: Node
        Purpose: return the parent node
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")
        return node.parent()
            
    def children(self, node):
        """
        Input: GameTree (implicit argument), node: Node
        Output: List of child nodes
        Purpose: returns a list of child nodes
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        return node.n_children
    
    def is_empty(self):
        """
        Input: GameTree (implicit argument)
        Output: boolean
        Purpose: return true if the tree is empty, false otherwise in O(1)
        """
        if self.t_root is None:
            return True
        return False
    
    def size(self):
        """
        Input: GameTree (implicit argument)
        Output: int
        Purpose: return the size of the tree in O(1)
        """
        return self.t_size

    def height(self):
        """
        Input: GameTree (implicit argument)
        Output: int
        Purpose: return the height of the tree in O(1) time
        Exceptions: throw an EmptyGameTreeException if the height is undefined
        """
        if self.isEmpty():
            raise EmptyGameTreeException("Tree is empty, height undefined")

        return self.t_height

    def is_internal(self, node):
        """
        Input: GameTree (implicit argument), node: Node
        Output: boolean
        Purpose: return whether the node is internal.
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is not None:
            if node.num_children() > 0:
                return True
        return False

    def is_external(self, node):
        """
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), node: Node
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
        Input: GameTree (implicit argument), e: anything
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
        Input: GameTree (implicit argument), node: Node, e: anything
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
        Input: GameTree (implicit argument), node: Node, e: anything
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
        Input: GameTree (implicit argument)
        Output: String representation of GameTree
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