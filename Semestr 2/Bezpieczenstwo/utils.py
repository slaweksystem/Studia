import random
import time

# Funkcja testu wzorcowego do standaryzacji
def calibration_benchmark():
    start = time.perf_counter()
    for i in range(100_000):
        _ = i ** 2
    return time.perf_counter() - start

# Generowanie danych testowych
def generate_keys(n, scenario):
    if scenario == 'random':
        return [random.randint(0, n*10) for _ in range(n)]
    if scenario == 'ordered':
        base = list(range(n))
        noise = [random.randint(-5,5) for _ in range(n)]
        return [max(0, base[i] + noise[i]) for i in range(n)]
    if scenario == 'collisions':
        return [random.randint(0, n//10) for _ in range(n)]