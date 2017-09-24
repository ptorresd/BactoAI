import numpy as np
import math


# -------------------------------  Neuron  --------------------------------------

class Neuron:

    def __init__(self, size):
        self.weights = np.random.random(size) - 0.5
        self.bias = 0
        self.output = 0
        self.lRate = 0.001
        self.delta = 0

    def get_output(self):
        return self.output

    def get_weights(self):
        return self.weights

    def get_delta(self):
        return self.delta

    def feed(self, input):
        res = np.dot(self.weights, input)
        self.output = 1 / (1 + math.exp(-1 * (res + self.bias)))

    def adjust_weights(self, input):
        self.weights = self.weights + self.lRate * input - self.delta
        self.bias += self.lRate * self.delta

    def update_delta(self, error):
        self.delta = (1 - self.output) * self.output * error


# -------------------------------   Layer  ---------------------------------------

class Layer:

    def __init__(self, layer_size, input_size):
        self.neurons = []
        self.input_size = input_size
        for i in range(layer_size):
            self.neurons += [Neuron(input_size)]

    def feed(self, input):
        for n in self.neurons:
            n.feed(input)

    def get_size(self):
        return len(self.neurons)

    def propagate(self, errors):
        for i in range(self.get_size()):
            self.neurons[i].update_delta(errors[i])

    def get_error(self):
        error = np.zeros(self.input_size)
        for n in self.neurons:
            error += n.get_delta() * n.get_weights()
        return error

    def adjust_weights(self, input):
        for n in self.neurons:
            n.adjust_weights(input)

    def get_output(self):
        res = []
        for n in self.neurons:
            res += [n.get_output()]
        return np.array(res)


# -------------------------------  Network  ----------------------------------------

class Network:

    def __init__(self, input_size, network_shape):
        self.layers = []
        self.layers += [Layer(network_shape[0], input_size)]
        for i in range(1, len(network_shape)):
            self.layers += [Layer(network_shape[i], network_shape[i-1])]

    def first(self):
        return self.layers[0]

    def last(self):
        return self.layers[len(self.layers) - 1]

    def get_output(self):
        return self.last().get_output()

    def feed(self, input):
        self.first().feed(input)
        for i in range(1, len(self.layers)):
            output = self.layers[i - 1].get_output()
            self.layers[i].feed(output)

    def back_propagation(self, expected_output):
        output = self.get_output()
        error = expected_output - output
        self.last().propagate(error)
        for i in range(len(self.layers) - 2, -1, -1):
            error = self.layers[i + 1].get_error()
            self.layers[i].propagate(error)

    def adjust_weights(self, input):
        self.first().adjust_weights(input)
        for i in range(1, len(self.layers)):
            output = self.layers[i - 1].get_output()
            self.layers[i].adjust_weights(output)

    def train(self, input, expected_output):
        self.feed(input)
        self.back_propagation(expected_output)
        self.adjust_weights(input)
