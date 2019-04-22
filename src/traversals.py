from asyncio import Queue

class InvalidInputException(Exception): 
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


""" Preorder, Inorder, Postorder, and Breadth First Traversals of a Binary Tree

"""

def preorder_help(qlist, node):
    """preorder: list, root node -> . 
    Purpose: Runs a preoder traveral on the binary tree. 
    Consumes: list, root node of a tree
    Produces: none
    """
    qlist.append(node)

    if node.hasLeft():
        preorder_help(qlist, node.left())

    if node.hasRight():
        preorder_help(qlist, node.right())

def preorder(bt):
    """preorder: binary tree -> list[Position] 
    Purpose: Runs a preoder traveral on the binary tree. 
    Consumes: a binary tree
    Produces: a list of Position objects preorder
    Example:       A 
       preorder(  / \  ) -> [A B C]
                 B   C 
    If tree is empty, should return an empty list. If the tree
    is null, you should throw InvalidInputException. 
    """
    if bt is None:
        raise InvalidInputException("Input is None")
    if bt.isEmpty():
        return []

    qlist = []
    preorder_help(qlist, bt.root())

    return qlist

def inorder_help(qlist, node):
    """inorder: list, node -> .
    Purpose: Runs an inorder traveral on the binary tree
    Consumes: list, root
    Produces: none
    """
    if node.hasLeft():
        inorder_help(qlist, node.left())
    
    qlist.append(node)

    if node.hasRight():
        inorder_help(qlist, node.right())

def inorder(bt):
    """inorder: binary tree -> list[Position] 
    Purpose: Runs an inorder traveral on the binary tree
    Consumes: a binary tree
    Produces: a list of Position objects inorder
    Example:       A 
        inorder(  / \  ) -> [B A C]
                 B   C 
    If tree is empty, should return an empty list. If the tree
    is null, you should throw InvalidInputException. 
    """
    if bt is None:
        raise InvalidInputException("Input is None")
    if bt.isEmpty():
        return []

    qlist = []
    inorder_help(qlist, bt.root())

    return qlist

def postorder_help(qlist, node):
    """postorder: list, binary tree, root -> .
    Purpose: Runs a postorder traveral on the binary tree
    Consumes: list, root node
    Produces: none
    """
    if node.hasLeft():
        postorder_help(qlist, node.left())
    if node.hasRight():
        postorder_help(qlist, node.right())

    qlist.append(node)

def postorder(bt):
    """postorder: binary tree -> list[Position] 
    Purpose: Runs a postorder traveral on the binary tree
    Consumes: a binary tree
    Produces: a list of Position objects postorder
    Example:       A 
      postorder(  / \  ) -> [B C A]
                 B   C 
    If tree is empty, should return an empty list. If the tree
    is null, you should throw InvalidInputException.   
    """
    if bt is None:
        raise InvalidInputException("Input is None")
    if bt.isEmpty():
        return []

    qlist = []
    postorder_help(qlist, bt.root())

    return qlist

def breadthfirst(bt):
    """breadthfirst: binary tree -> list[Node]
    Purpose: Runs a breadth first search on a binary tree
    Consumes: a binary tree object
    Produces: a list of Nodes in breadth first search order
    Example: 
                    A 
    breadthfirst(  / \  ) -> [A B C]
                  B   C 
    If tree is empty, should return an empty list. If the tree
    is null, you should throw InvalidInputException. 
    """
    if bt is None:
        raise InvalidInputException("Input is None")
    if bt.isEmpty():
        return []

    Q = Queue()
    qlist = []
    qlist.append(bt.root())
    Q.put(bt.root())
    
    while not Q.empty():
        
        node = Q.get()
        
        if bt.hasLeft(node):
            Q.put(bt.left(node))
            qlist.append(bt.left(node))
        if bt.hasRight(node):
            Q.put(bt.right(node))
            qlist.append(bt.right(node))

    return qlist
