# How To Use

```python
from neural_network_implementation.neural_network import NeuralNetwork
from neural_network_implementation.layers import Layer
import numpy as np

x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

nn = NeuralNetwork()
nn.add_layer(Layer(2, 10, 'sigmoid'))
nn.add_layer(Layer(10, 1, 'sigmoid'))
errors = nn.train(x, y, 0.75, 500, 'MSE')

```