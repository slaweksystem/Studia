import numpy as np
import matplotlib.pyplot as plt

# Funkcja kosztu: f(x) = x^2 + 3x
def cost_function(x):
    return x**2+3*x

# Gradient funkcji kosztu: f'(x) = 2x + 3
def gradient(x):
    return 2 * x + 3

# Parametry Gradient Descent
learning_rate = 0.1  # Tempo uczenia
iterations = 50      # Liczba iteracji
x_start = 6          # Początkowa wartość x

# Lista do przechowywania wyników
x_values = [x_start]
cost_values = [cost_function(x_start)]

# Gradient Descent
x = x_start
for i in range(iterations):
    grad = gradient(x)              # Oblicz gradient
    x = x - learning_rate * grad    # Aktualizacja x
    x_values.append(x)              # Zapis nowego x
    cost_values.append(cost_function(x))  # Zapis wartości funkcji kosztu

# Wynik końcowy
print(f"Minimum funkcji przybliżone w x = {x:.4f}")
print(f"Wartość funkcji kosztu w minimum: {cost_function(x):.4f}")

# Wizualizacja
plt.figure(figsize=(10, 6))

# Wykres funkcji kosztu
x_plot = np.linspace(-6, 6, 100)
plt.plot(x_plot, cost_function(x_plot), label="Funkcja kosztu: $f(x) = x^2 + 3x$", color="blue")

# Punkty optymalizacji
plt.scatter(x_values, cost_values, color="red", label="Kroki Gradient Descent")

# Oznaczenie startu i końca
plt.scatter(x_values[0], cost_values[0], color="green", label="Start", zorder=5)
plt.scatter(x_values[-1], cost_values[-1], color="orange", label="Koniec (minimum)", zorder=5)

# Opis osi i tytuł
plt.title("Gradient Descent - minimalizacja funkcji $f(x) = x^2 + 3x$")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
