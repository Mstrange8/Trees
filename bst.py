"""Program containing Node object and Binary Search Tree"""


class Node:
    """Node object class"""
    def __init__(self, data):
        self.data = data
        self.leftChild = None
        self.rightChild = None
        self.parent = None

    def add(self, data):
        """helper method to add node"""
        if self.data == data:
            return False        # As BST cannot contain duplicate data

        elif data < self.data:
            if self.leftChild:
                return self.leftChild.add(data)
            else:
                self.leftChild = Node(data)
                return True

        else:
            if self.rightChild:
                return self.rightChild.add(data)
            else:
                self.rightChild = Node(data)
                return True

    def minValueNode(self, node):
        """returns the min value node"""
        current = node

        while current.leftChild is not None:
            current = current.leftChild

        return current

    def maxValueNode(self, node):
        """returns the max value node"""
        current = node

        while current.rightChild is not None:
            current = current.rightChild

        return current

    def delete(self, data, root):
        """helper method to delete a node"""

        if self is None:
            return None

        # if current node's data is less than that of root node,
        # then only search in left subtree else right subtree
        if data < self.data:
            self.leftChild = self.leftChild.delete(data, root)
        elif data > self.data:
            self.rightChild = self.rightChild.delete(data, root)
        else:
            # deleting node with one child
            if self.leftChild is None:
                if self == root:
                    temp = self.minValueNode(self.rightChild)
                    self.data = temp.data
                    self.rightChild = self.rightChild.delete(temp.data, root)

                temp = self.rightChild
                return temp
            elif self.rightChild is None:

                if self == root:
                    temp = self.maxValueNode(self.leftChild)
                    self.data = temp.data
                    self.leftChild = self.leftChild.delete(temp.data, root)

                temp = self.leftChild
                return temp

            # deleting node with two children
            # first get the inorder successor
            temp = self.minValueNode(self.rightChild)
            self.data = temp.data
            self.rightChild = self.rightChild.delete(temp.data, root)

        return self

    def find(self, data):
        """helper method to find a specific node"""
        if data == self.data:
            return True
        elif data < self.data:
            if self.leftChild:
                return self.leftChild.find(data)
            else:
                return False
        else:
            if self.rightChild:
                return self.rightChild.find(data)
            else:
                return False

    def height(self):
        """helper method to return the height of the tree"""
        if self.leftChild and self.rightChild:
            return 1 + max(self.leftChild.height(), self.rightChild.height())
        elif self.leftChild:
            return 1 + self.leftChild.height()
        elif self.rightChild:
            return 1 + self.rightChild.height()
        else:
            return 1

    def preorder(self, _list):
        '''For preorder traversal of the BST '''

        if self:
            _list.append(self.data)
            if self.leftChild:
                self.leftChild.preorder(_list)
            if self.rightChild:
                self.rightChild.preorder(_list)
            return _list

    def inorder(self, _list):
        ''' For Inorder traversal of the BST '''
        if self:
            if self.leftChild:
                self.leftChild.inorder(_list)
            _list.append(self.data)
            if self.rightChild:
                self.rightChild.inorder(_list)
            return _list

    def postorder(self, _list):
        ''' For postorder traversal of the BST '''
        if self:
            if self.leftChild:
                self.leftChild.postorder(_list)
            if self.rightChild:
                self.rightChild.postorder(_list)
            _list.append(self.data)
            return _list

    def weigh(self):
        """ Return How Left or Right Sided the Tree Is
        Positive Number Means Left Side Heavy, Negative Number Means Right Side Heavy
        """
        if self.leftChild is None:
            left_height = -1
        else:
            left_height = self.leftChild.height()

        if self.rightChild is None:
            right_height = -1
        else:
            right_height = self.rightChild.height()

        balance = left_height - right_height
        return balance

    def rebalance(self, tree):
        """helper method to rebalance the tree"""
        while self.weigh() < -1 or self.weigh() > 1:
            if self.weigh() < 0:
                if self.rightChild.weigh() > 0:
                    self.rightChild.rotate_left()
                new_top = self.rotate_right()
            else:
                if self.leftChild.weigh() < 0:
                    self.leftChild.rotate_right()
                new_top = self.rotate_left()

            if new_top.parent is None:
                tree.root = new_top

    def rotate_right(self):
        """rotates the the tree to the right"""
        to_promote = self.rightChild
        swapper = to_promote.leftChild

        # swap children
        self.rightChild = swapper
        to_promote.leftChild = self
        new_top = self._swap_parents(to_promote, swapper)
        return new_top

    def rotate_left(self):
        """rotates the tree to the left"""
        to_promote = self.leftChild
        swapper = to_promote.rightChild

        # swap children
        self.leftChild = swapper
        to_promote.rightChild = self
        new_top = self._swap_parents(to_promote, swapper)
        return new_top

    def _swap_parents(self, promote, swapper):
        """ re-assign parents, returns new top
        """
        promote.parent = self.parent
        self.parent = promote
        if swapper is not None:
            swapper.parent = self

        if promote.parent is not None:
            if promote.parent.rightChild == self:
                promote.parent.rightChild = promote
            elif promote.parent.leftChild == self:
                promote.parent.leftChild = promote
        return promote


class BST:
    """Binary Search Tree class"""
    def __init__(self):
        self.root = None
        self._size = 0

    def add(self, data):
        """method that adds new node to tree"""
        self._size += 1
        if self.root:
            return self.root.add(data)
        else:
            self.root = Node(data)
            return True

    def remove(self, data):
        """method that removes node from tree"""
        if self.root is not None:
            self._size -= 1
            return self.root.delete(data, self.root)

    def find(self, data):
        """method that finds node in tree"""
        if self.root:
            return self.root.find(data)
        else:
            raise ValueError

    def preorder(self):
        """returns the preorder of the tree in a list"""
        _list = []
        if self.root is not None:
            print()
            return self.root.preorder(_list)

    def inorder(self):
        """returns the inorder of the tree in a list"""
        _list = []
        if self.root is not None:
            return self.root.inorder(_list)

    def postorder(self):
        """returns the postorder of the tree in a list"""
        _list = []
        if self.root is not None:
            return self.root.postorder(_list)

    def size(self):
        """returns the size of the tree"""
        return self._size

    def is_empty(self):
        """returns whether the tree is empty or not"""
        if self.root is None:
            return True
        return False

    def height(self):
        """returns the height of the treee"""
        if self.root:
            return self.root.height()
        else:
            return 0

    def rebalance(self):
        """rebalances the tree"""
        if self.root is not None:
            self.root.rebalance(self)
