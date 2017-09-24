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

    def feed(self, input):
        res = np.dot(self.weights, input)
        self.output = 1 / (1 + math.exp(-1 * (res + self.bias)))

    def adjust_weights(self,input):
        self.weights = self.weights + self.lRate * input - self.delta
        self.bias += self.lRate * self.delta


# -------------------------------   Layer  ---------------------------------------

class Layer:

    def __init__(self, layer_size, input_size):
        self.neurons = []
        for i in range(layer_size):
            self.neurons += [Neuron(input_size)]

    def feed(self, input):
        for n in self.neurons:
            n.feed(input)

    def get_size(self):
        return len(self.neurons)


