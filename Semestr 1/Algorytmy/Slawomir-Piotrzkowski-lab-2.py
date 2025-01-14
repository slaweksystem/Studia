import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Dane uczące
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Inicjalizacja wag
np.random.seed(42)
weights_input_hidden = np.random.uniform(-1, 1, (2, 2))
weights_hidden_output = np.random.uniform(-1, 1, (2, 1))

learning_rate = 0.1

# Proces uczenia
cycles = 100000
for epoch in range(cycles):
    # Propagacja w przód
    hidden_layer_input = np.dot(X, weights_input_hidden)
    hidden_layer_output = sigmoid(hidden_layer_input)

    final_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
    final_layer_output = sigmoid(final_layer_input)

    # Obliczenie błędu
    error = y - final_layer_output
    
    # Propagacja wsteczna
    d_output = error * sigmoid_derivative(final_layer_output)
    error_hidden_layer = d_output.dot(weights_hidden_output.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    # Aktualizacja wag
    weights_hidden_output += hidden_layer_output.T.dot(d_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden_layer) * learning_rate

print(f"Wyjście sieci po nauce dla {cycles} epok:\n", final_layer_output)