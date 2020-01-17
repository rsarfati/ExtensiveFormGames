class Game:

    def __init__(self, num_players, tree) :
        """
        Input: Game (implicit argument), num_player: Int, value: anything
        Output: a Node with a parent node and a value
        Purpose: constructor for a Node
        """
        self.num_players = num_players
        self.tree = GameTree() if tree is None else tree

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
        self.n_player          = player
        self.n_information_set = inf_set
        self.n_payoffs         = None
        self.n_children        = []

        if self.n_parent is None:
            # Vacuously first child
            self.n_id    = 1
            self.n_depth = 0 
            
            # Maps players to the sequences getting them to node
            self.n_sequences  = {player: []}
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
        return len(self.n_children)
    
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

        for child in self.n_children:
            output += "; Child " + str(child.n_id) + ": "
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
        if self.is_empty():
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
        if self.is_empty():
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

        return node.num_children() == 0

    def is_root(self, node):
        """
        Input: GameTree (implicit argument), node: Node
        Output: Boolean
        Purpose: return whether the node is the root
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")

        if node.parent() is None:
            return True
        return False

    def get_child(self, node, child_id):
        """
        Input: GameTree (implicit argument), node: Node
        Output: Node
        Purpose: get the left child of the node (if possible)
        Exceptions: throw an InvalidInputException if input is None
        """
        if node is None or child_id is None:
            raise InvalidInputException("Input/Child ID is None")
        
        if node.num_children() < child_id:
            raise InvalidInputException("Node does not have such a child.")
        
        return node.children[child_id]

    def is_child(self, node, child):
        """
        Input: GameTree (implicit), node: Node, child: Node
        Output: Boolean
        Purpose: Indicate whether child is of node.
        """
        if node is None or child is None:
            raise InvalidInputException("Input is None")

        for node_child in node.children():
            if child == node_child:
                return True

        return False

    def add_root(self, player, inf_set):
        """
        Input: GameTree (implicit argument), player: Int, inf_set: Int.
        Output: Node (the root node)
        Purpose: add a root to the tree only if there isn't one already and return it.
                 If there is one already, just return it
        """
        if self.t_root is None:
            self.t_root  = Node(None, player, inf_set)
            self.t_root.sequences = {}
            self.t_size += 1
        return self.t_root

    def add_child(self, node, player, inf_set):
        """
        Input: GameTree (implicit argument), node: Node, player: Int, inf_set: Int.
        Output: Node (the added node)
        Purpose: Add a child to the node  and return it.
        Exceptions: throw an InvalidInputException if node input is None
        """
        if node is None:
            raise InvalidInputException("Input is None")
        
        child = node.add_child(player, inf_set)

        self.t_size += 1
        if child.depth() > self.t_height:
            self.t_height = child.depth()
        return child
        
    def __str__(self):
        """
        Input: GameTree (implicit argument)
        Output: String representation of GameTree
        Purpose: printing
        """
        toReturn  = 'Size: ' + str(self.size()) + '\n'
        toReturn += 'Height: ' + str(self.height()) + '\n'
        toReturn += str(self.root()) 
        return toReturn

 
    def get_height(self, node):
        if not node:
            return 0
        else:
            return max([getheight(x) for x in node.children()]) + 1
