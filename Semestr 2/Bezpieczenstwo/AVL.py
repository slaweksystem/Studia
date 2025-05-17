class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = max(self._height(node.left), self._height(node.right)) + 1

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # rotation
        x.right = y
        y.left = T2

        # update heights
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # rotation
        y.left = x
        x.right = T2

        # update heights
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node, key):
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            # Left-Right case
            if key > node.left.key:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            # Right-Left case
            if key < node.right.key:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self.insert(node.left, key, value)
        elif key > node.key:
            node.right = self.insert(node.right, key, value)
        else:
            node.value = value
            return node

        return self._rebalance(node, key)

    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [AVLTree() for _ in range(size)]

    def hash_func(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_func(key)
        tree = self.table[index]
        tree.root = tree.insert(tree.root, key, value)

    def search(self, key):
        index = self.hash_func(key)
        node = self.table[index].search(self.table[index].root, key)
        return node.value if node else None