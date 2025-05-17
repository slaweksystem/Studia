import random

# Generowanie danych
def generate_keys(n, scenario):
    if scenario == 'Posortowana':
        return list(range(n))
    elif scenario == 'Losowa unikalna':
        base = list(range(n))
        random.shuffle(base)
        return base
    elif scenario == 'Losowa':
        return [random.randint(0, n*10) for _ in range(n)]
    elif scenario == 'Posortowana szum':
        base = list(range(n))
        noise = [random.randint(-5,5) for _ in range(n)]
        return [max(0, base[i] + noise[i]) for i in range(n)]
    elif scenario == 'Powtarzajaca':
        return [random.randint(0, n//10) for _ in range(n)]
