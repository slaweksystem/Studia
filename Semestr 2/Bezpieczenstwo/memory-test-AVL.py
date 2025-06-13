# importy lokalnych modułów
from BST import HashTable as HashTableAVL

from Benchmark import memory_benchmark
from Generators import generate_keys

if __name__ == '__main__':
    test_size = 1000000
    keys = generate_keys(test_size, 'Losowa')
    memory_used = memory_benchmark(HashTableAVL, keys)

    print(f"AVL Iloasc elementów: {test_size}: Zużyta Pamiec: {memory_used} MiB")