import numpy as np
import matplotlib.pyplot as plt

# Funkcja kosztu: f(x) = x^2
def cost_function(x):
    return x**2

# Gradient funkcji kosztu: f'(x) = 2x
def gradient(x):
    return 2 * x

# Implementacja Gradient Descent
def gradient_descent(initial_x, learning_rate, iterations):
    x = initial_x  # Punkt startowy
    history = []   # Lista do przechowywania historii x i f(x)
    
    for i in range(iterations):
        grad = gradient(x)                 # Oblicz gradient
        x = x - learning_rate * grad       # Aktualizacja x
        history.append((x, cost_function(x)))  # Zapis stanu

    return history

# Parametry
initial_x = 5.0         # Punkt początkowy
learning_rate = 0.1     # Tempo uczenia
iterations = 50         # Liczba iteracji

# Uruchomienie Gradient Descent
history = gradient_descent(initial_x, learning_rate, iterations)

# Wyniki końcowe
final_x, final_cost = history[-1]
print(f"Przybliżone minimum funkcji osiągnięte w x = {final_x:.4f}")
print(f"Wartość funkcji kosztu w tym punkcie: {final_cost:.4f}")

# Wizualizacja
x_values, cost_values = zip(*history)

plt.figure(figsize=(10, 6))

# Wykres funkcji kosztu
x_plot = np.linspace(-6, 6, 100)
plt.plot(x_plot, cost_function(x_plot), label="Funkcja kosztu $f(x) = x^2$", color="blue")

# Punkty Gradient Descent
plt.scatter(x_values, cost_values, color="red", label="Kroki Gradient Descent", zorder=5)

# Oznaczenie punktów początkowego i końcowego
plt.scatter(x_values[0], cost_values[0], color="green", label="Start", zorder=10)
plt.scatter(x_values[-1], cost_values[-1], color="orange", label="Koniec (minimum)", zorder=10)

# Opis osi i legenda
plt.title("Gradient Descent – Minimalizacja funkcji $f(x) = x^2$")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
plt.legend()
plt.grid(True)
plt.show()
