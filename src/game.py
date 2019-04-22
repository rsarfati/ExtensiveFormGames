import bintree

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
        toReturn = 'Num. Players: ' + str(self.n_players) + '\n'
        toReturn += 'Size: ' + str(self.size()) + '\n'
        toReturn += 'Height: ' + str(self.height()) + '\n'
        return toReturn