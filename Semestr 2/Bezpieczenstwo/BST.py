class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, node, key, value):
        if node is None:
            return BSTNode(key, value)
        if key < node.key:
            node.left = self.insert(node.left, key, value)
        elif key > node.key:
            node.right = self.insert(node.right, key, value)
        else:
            node.value = value  # aktualizacja istniejącego klucza
        return node

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
        self.table = [BST() for _ in range(size)]

    def hash_func(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_func(key)
        bst = self.table[index]
        bst.root = bst.insert(bst.root, key, value)

    def search(self, key):
        index = self.hash_func(key)
        bst = self.table[index]
        return bst.search(bst.root, key).value