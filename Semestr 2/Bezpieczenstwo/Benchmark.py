import time
from memory_profiler import memory_usage

# Test kalibracyjny
def calibration_benchmark():
    start = time.perf_counter()
    for i in range(100_000):
        _ = i ** 2
    return time.perf_counter() - start

# Pomiar czasu
def performance_benchmark(table_cls, table_size, keys):
    ht = table_cls(size=table_size)
    start = time.perf_counter()
    for k in keys:
        ht.insert(k, k)
    t_insert = (time.perf_counter() - start)

    start = time.perf_counter()
    for k in keys:
        _ = ht.search(k)
    t_search = (time.perf_counter() - start)

    return t_insert, t_search

# Pomiar pamięci
def memory_benchmark(table_cls, keys):
    def run():
        ht = table_cls(size=100)
        for k in keys:
            ht.insert(k, k)
        for k in keys:
            _ = ht.search(k)

    mem_usage = memory_usage(run, max_iterations=1, interval=0.01)
    return max(mem_usage) - min(mem_usage)

# Pomiar dla listy i słownika
def benchmark_builtin_structures(keys):
    data_list = []
    data_dict = {}

    start = time.perf_counter()
    for k in keys:
        data_list.append((k, k))
    t_insert_list = (time.perf_counter() - start)

    start = time.perf_counter()
    for k in keys:
        _ = next((v for key, v in data_list if key == k), None)
    t_search_list = (time.perf_counter() - start)

    start = time.perf_counter()
    for k in keys:
        data_dict[k] = k
    t_insert_dict = (time.perf_counter() - start)

    start = time.perf_counter()
    for k in keys:
        _ = data_dict.get(k)
    t_search_dict = (time.perf_counter() - start)

    return (t_insert_list, t_search_list), (t_insert_dict, t_search_dict)