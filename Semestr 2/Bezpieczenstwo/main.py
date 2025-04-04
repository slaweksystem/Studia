from BST import HashTable

from time import time
n_val = 300000
hash_tree_size = 10000

print(f"Test-Hash-Table - size {n_val}")

bst_tree = HashTable(hash_tree_size)
regular_dic = {}

time_start = time()

for i in range(n_val):
    bst_tree.insert(i, i)
    regular_dic[i] = i
time_stop = time()

create_time = time_stop - time_start

time_start = time()
search_tree_val = bst_tree.search(213769)
time_stop = time()
search_time = time_stop - time_start

print("Szukanie w słowniku")

time_start = time()
search_dict_val = regular_dic[213769]
time_stop = time()
search_time_dict = time_stop - time_start

print(f"Tworzenie trwało {create_time}")
print(f"Szukanie w drzewie trwało: {search_time}")
print(f"Znaleziono {search_tree_val }")
print(f"Szukanie w słowniku trwało: {search_time_dict}")
print(f"Znaleziono {search_dict_val }")