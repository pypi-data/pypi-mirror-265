from .layers import Layer
import numpy as np
from nn_error_metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error
)

class NeuralNetwork:
    def __init__(self):
        self._layers = []

    def add_layer(self, layer):
        self._layers.append(layer)

    def feed_forward(self, x):
        for layer in self._layers:
            x = layer.activate(x)
        return x

    def predict(self, x):
        ff = self.feed_forward(x)
        return ff

    def backpropagation(self, X, y, learning_rate):
        output = self.feed_forward(X)
        for i in reversed(range(len(self._layers))):
            layer = self._layers[i]
            if layer == self._layers[-1]:
                layer.error = y - output
                layer.delta = layer.error * layer.apply_activation_derivative(output)
            else:
                next_layer = self._layers[i + 1]
                layer.error = np.dot(next_layer.weights, next_layer.delta)
                layer.delta = layer.error * layer.apply_activation_derivative(layer.last_activation)
        for i in range(len(self._layers)):
            layer = self._layers[i]
            input_to_use = np.atleast_2d(X if i == 0 else self._layers[i - 1].last_activation)
            layer.weights += layer.delta * input_to_use.T * learning_rate

    def train(self, x, y, learning_rate, max_epochs, error_function):
        errors = []
        for i in range(max_epochs):
            temp_errors = []
            for j in range(len(x)):
                self.backpropagation(x[j], y[j], learning_rate)
                if error_function == "MSE":
                    error = mean_squared_error(y, self.feed_forward(x))
                elif error_function == "MAPE":
                    error = mean_absolute_percentage_error(y, self.feed_forward(x))
                elif error_function == "MAE":
                    error = mean_absolute_error(y, self.feed_forward(x))
                elif error_function == "RMSE":
                    error = root_mean_squared_error(y, self.feed_forward(x))
                else:
                    raise ValueError("Unknown error function specified")
                temp_errors.append(error)
            errors.append(sum(temp_errors) / len(temp_errors))
            print('Epoch: #%s, Error: %f' % (i+1, float(error)))
        return errors
