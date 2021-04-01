"""I declare that the following source code was
written solely by me. I understand that copying
any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this
project if I am found in violation of this policy."""


# Hailey Strobelt

class BST:
    """Creates Binary Search Tree."""
    def __init__(self):
        """Initialize values."""
        self.root = None
        self._size = 0


    def is_empty(self):
        """Returns True if empty."""
        return self.root is None

    def size(self):
        """Returns number of items in tree."""
        return self._size

    def height(self, bst):
        """Returns height of tree"""
        # Height of tree is the length of the
        # path from the root to its deepest leaf.
        if self.is_empty():
            return 0
        else:
            return 1 + max(self.height(bst.left_child), self.height(bst.right_child))


    def add(self, key, value):
        """Adds item to its proper place in tree."""
        # Return the modified tree.
        if self.root:
            self._add(key, value, self.root)
        else:
            self.root = TreeNode(key, value)
        self._size = self._size + 1

    def _add(self, key, value, current_node):
        """Add helper function."""
        if key < current_node.key:
            if current_node.left_child:
                self._add(key, value, current_node.left_child)
            else:
                current_node.left_child = TreeNode(
                    key, value, parent=current_node
                )
        else:
            if current_node.right_child:
                self._add(key, value, current_node.right_child)
            else:
                current_node.right_child = TreeNode(
                    key, value, parent=current_node
                )

    def __setitem__(self, key, value):
        """Overwrites setitem with new function."""
        self.add(key, value)

    def remove(self, key):
        """Removes item from tree."""
        # Return the modified tree.
        if self._size > 1:
            node_to_remove = self._find(key, self.root)
            if node_to_remove:
                self._remove(node_to_remove)
                self._size = self._size - 1
            else:
                raise KeyError("Error, key not in tree")
        elif self._size == 1 and self.root.key == key:
            self.root = None
            self._size = self._size - 1
        else:
            raise KeyError("Error, key not in tree")

    def _remove(self, cur_node):
        """Remove helper function."""
        if cur_node.is_leaf():  # removing a leaf
            if cur_node == cur_node.parent.left_child:
                cur_node.parent.left_child = None
            else:
                cur_node.parent.right_child = None
        elif cur_node.has_children():  # removing a node with two children
            successor = cur_node.find_successor()
            successor.splice_out()
            cur_node.key = successor.key
            cur_node.value = successor.value
        else:  # removing a node with one child
            if cur_node.left_child:
                if cur_node.is_left_child():
                    cur_node.left_child.parent = cur_node.parent
                    cur_node.parent.left_child = cur_node.left_child
                elif cur_node.is_right_child():
                    cur_node.left_child.parent = cur_node.parent
                    cur_node.parent.right_child = cur_node.left_child
                else:
                    cur_node.replace_value(
                        cur_node.left_child.key,
                        cur_node.left_child.value,
                        cur_node.left_child.left_child,
                        cur_node.left_child.right_child,
                    )
            else:
                if cur_node.is_left_child():
                    cur_node.right_child.parent = cur_node.parent
                    cur_node.parent.left_child = cur_node.right_child
                elif cur_node.is_right_child():
                    cur_node.right_child.parent = cur_node.parent
                    cur_node.parent.right_child = cur_node.right_child
                else:
                    cur_node.replace_value(
                        cur_node.right_child.key,
                        cur_node.right_child.value,
                        cur_node.right_child.left_child,
                        cur_node.right_child.right_child,
                    )

    def __delitem__(self, key):
        self.remove(key)

    def find(self, key):
        """Returns the matched item."""
        # If item isn't in the tree, raise ValueError.
        if self.root:
            result = self._find(key, self.root)
            if result:
                return result.value
        else:
            raise ValueError

    def _find(self, key, cur_node):
        """Find helper function."""
        if not cur_node:
            return None
        if cur_node.key == key:
            return cur_node
        elif key < cur_node.key:
            return self._find(key, cur_node.left_child)
        else:
            return self._find(key, cur_node.right_child)

    def __getitem__(self, key):
        """Overwrites getitem with new function."""
        return self.find(key)

    def __contains__(self, key):
        """Overwrites contains with new function."""
        return bool(self._find(key, self.root))

    def rebalance(self, node):
        """Rebalances the tree."""
        if node.balance_factor < 0:
            if node.right_child.balance_factor > 0:
                self.rotate_right(node.right_child)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif node.balance_factor > 0:
            if node.left_child.balance_factor < 0:
                self.rotate_left(node.left_child)
                self.rotate_right(node)
            else:
                self.rotate_right(node)

    def rotate_left(self, rotation_root):
        """Allows us to rotate left."""
        new_root = rotation_root.right_child
        rotation_root.right_child = new_root.left_child
        if new_root.left_child:
            new_root.left_child.parent = rotation_root
        new_root.parent = rotation_root.parent
        if rotation_root.is_root():
            self._root = new_root
        else:
            if rotation_root.is_left_child():
                rotation_root.parent.left_child = new_root
            else:
                rotation_root.parent.right_child = new_root
        new_root.left_child = rotation_root
        rotation_root.parent = new_root
        rotation_root.balance_factor = (
                rotation_root.balance_factor + 1 - min(new_root.balance_factor, 0)
        )
        new_root.balance_factor = (
                new_root.balance_factor + 1 + max(rotation_root.balance_factor, 0)
        )

    def rotate_right(self, rotation_root):
        """Allows us to rotate right."""
        new_root = rotation_root.left_child
        rotation_root.left_child = new_root.right_child
        if new_root.right_child:
            new_root.right_child.parent = rotation_root
        new_root.parent = rotation_root.parent
        if rotation_root.is_root():
            self._root = new_root
        else:
            if rotation_root.is_left_child():
                rotation_root.parent.right_child = new_root
            else:
                rotation_root.parent.left_child = new_root
        new_root.right_child = rotation_root
        rotation_root.parent = new_root
        rotation_root.balance_factor = (
                rotation_root.balance_factor + 1 - min(new_root.balance_factor, 0)
        )
        new_root.balance_factor = (
                new_root.balance_factor + 1 + max(rotation_root.balance_factor, 0)
        )


class TreeNode:
    """Creates tree node."""
    def __init__(self, key, value, left=None, right=None, parent=None):
        """Initialize values."""
        self.key = key
        self.value = value
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def is_left_child(self):
        """Checks if left child."""
        return self.parent and self.parent.left_child is self

    def is_right_child(self):
        """Checks if right child."""
        return self.parent and self.parent.right_child is self

    def is_root(self):
        """Checks if root."""
        return not self.parent

    def is_leaf(self):
        """Checks if leaf."""
        return not (self.right_child or self.left_child)

    def has_a_child(self):
        """Checks if node has child."""
        return self.right_child or self.left_child

    def has_children(self):
        """Checks if node has children."""
        return self.right_child and self.left_child

    def replace_value(self, key, value, left, right):
        """Replaces current value."""
        self.key = key
        self.value = value
        self.left_child = left
        self.right_child = right
        if self.left_child:
            self.left_child.parent = self
        if self.right_child:
            self.right_child.parent = self

    def find_successor(self):
        """Gives us our successor."""
        successor = None
        if self.right_child:
            successor = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    successor = self.parent
                else:
                    self.parent.right_child = None
                    successor = self.parent.find_successor()
                    self.parent.right_child = self
        return successor

    def find_min(self):
        """Finds min value."""
        current = self
        while current.left_child:
            current = current.left_child
        return current

    def splice_out(self):
        """Takes value out."""
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_a_child():
            if self.left_child:
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

    def inorder(self):
        """Returns a list with the data items
        in order of inorder traversal."""
        if self.left_child:
            self.left_child.inorder()
        print(self.key)
        if self.right_child:
            self.right_child.inorder()

    def preorder(self):
        """Returns a list with the data items
        in order of preorder traversal."""
        print(self.key)
        if self.left_child:
            self.left_child.preorder()
        if self.right_child:
            self.right_child.preorder()

    def postorder(self):
        """Returns a list with the data items
        in order of postorder traversal."""
        if self.left_child:
            self.left_child.postorder()
        if self.right_child:
            self.right_child.postorder()
        print(self.key)


