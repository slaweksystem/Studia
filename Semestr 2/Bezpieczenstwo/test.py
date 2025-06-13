import numpy as np
import pandas as pd

# importy lokalnych modułów
from BST import HashTable as HashTableBST
from AVL import HashTable as HashTableAVL

from Benchmark import calibration_benchmark
from Benchmark import performance_benchmark
from Benchmark import benchmark_builtin_structures
from Generators import generate_keys

# Parametry
test_size = 10000
table_cls = 100
scenarios = ['Posortowana', 'Posortowana szum', 'Losowa unikalna', 'Losowa', 'Powtarzajaca']

calibration = calibration_benchmark()
print(f"Pomiar kalibracyjny trwał: {calibration} s")

# Generowanie wartości
keys = {}
for scenario in scenarios:
    keys[scenario] = generate_keys(test_size, scenario)

# Pomiary
sample_values = pd.DataFrame({ s: keys[s][10:20] for s in scenarios })

structures = ['BST', 'AVL', 'List', 'Dict']

results_insert = pd.DataFrame({'Struktura': structures}).set_index('Struktura')
results_insert_normalized = pd.DataFrame({'Struktura': structures}).set_index('Struktura')
results_search = pd.DataFrame({'Struktura': structures}).set_index('Struktura')
results_search_normalized = pd.DataFrame({'Struktura': structures}).set_index('Struktura')

for scenario in scenarios:
    bst_ins, bst_srch = performance_benchmark(HashTableBST, table_cls, keys[scenario])

    bst_ins, bst_srch = performance_benchmark(HashTableBST, table_cls, keys[scenario])
    avl_ins, avl_srch = performance_benchmark(HashTableAVL, table_cls, keys[scenario])
    list_perf, dict_perf = benchmark_builtin_structures(keys[scenario])

    results_insert[f"{scenario}"]            = [bst_ins, avl_ins, list_perf[0], dict_perf[0]]
    results_insert_normalized[f"{scenario}"] = [bst_ins / calibration,
                                                avl_ins/ calibration,
                                                list_perf[0] / calibration, 
                                                dict_perf[0] / calibration]

    results_search[f"{scenario}"]             = [bst_srch, avl_srch, list_perf[1], dict_perf[1]]
    results_search_normalized [f"{scenario}"] = [bst_srch / calibration,
                                                 avl_srch / calibration,
                                                 list_perf[1] / calibration,
                                                 dict_perf[1] / calibration]

# Zapis wyników
results_insert.to_csv("wyniki-dodawanie.csv")
results_insert_normalized.to_csv("wyniki-dodawanie-znormalizowane.csv")
results_search.to_csv("wyniki-wyszukiwanie.csv")
results_search_normalized.to_csv("wyniki-wyszukiwanie-znormalizowane.csv")