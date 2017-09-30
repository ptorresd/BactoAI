import numpy as np
import math
import time
from datetime import datetime

# -------------------------------  Neuron  --------------------------------------

class Neuron:

    def __init__(self, size):
        self.weights = np.random.random(size) - 0.5
        self.bias = 0
        self.output = 0
        self.delta = 0

    def get_output(self):
        return self.output

    def get_weights(self):
        return self.weights

    def get_delta(self):
        return self.delta

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias

    def feed(self, input):
        res = np.dot(self.weights, input)
        self.output = 1 / (1 + math.exp(-1 * (res + self.bias)))

    def adjust_weights(self, input, learning_rate):
        self.weights = self.weights + self.delta * learning_rate * input
        self.bias += learning_rate * self.delta

    def update_delta(self, error):
        self.delta = (1 - self.output) * self.output * error

    def export_neuron(self, file):
        file.write(str(self.weights[0]))
        for i in range(1,self.weights.shape[0]):
            file.write(' ' + str(self.weights[i]))
        file.write('\n' + str(self.bias) + '\n')

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

    def get_input_size(self):
        return self.input_size

    def set_weights(self, weights):
        for i in range(len(self.neurons)):
            self.neurons[i].set_weights(weights[i])

    def set_bias(self, bias):
        for i in range(len(self.neurons)):
            self.neurons[i].set_bias(bias[i])

    def propagate(self, errors):
        for i in range(self.get_size()):
            self.neurons[i].update_delta(errors[i])

    def get_error(self):
        error = np.zeros(self.input_size)
        for n in self.neurons:
            error += n.get_delta() * n.get_weights()
        return error

    def adjust_weights(self, input, learning_rate):
        for n in self.neurons:
            n.adjust_weights(input, learning_rate)

    def get_output(self):
        res = []
        for n in self.neurons:
            res += [n.get_output()]
        return np.array(res)

    def export_layer(self, file):
        for n in self.neurons:
            n.export_neuron(file)

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

    def set_weights(self,weights):
        for i in range(len(self.layers)):
            self.layers[i].set_weights(weights[i])

    def set_bias(self, bias):
        for i in range(len(self.layers)):
            self.layers[i].set_bias(bias[i])

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

    def adjust_weights(self, input, learning_rate):
        self.first().adjust_weights(input, learning_rate)
        for i in range(1, len(self.layers)):
            output = self.layers[i - 1].get_output()
            self.layers[i].adjust_weights(output, learning_rate)

    def train(self, input, expected_output, lRate=0.5):

        #t1 = datetime.now()
        self.feed(input)
        #t2 = datetime.now()
        self.back_propagation(expected_output)
        #t3 = datetime.now()
        self.adjust_weights(input, lRate)
        #t4 = datetime.now()
        #print(str((t2-t1).microseconds))
        #print(str((t3-t2).microseconds))
        #print(str((t4-t3).microseconds))

    def export_network(self, direc):
        file = open(direc, 'w')
        shape = [self.first().get_input_size()]
        file.write(str(shape[0]))
        for l in self.layers:
            file.write("," + str(l.get_size()))
            shape += [l.get_size()]
        file.write('\n')
        for l in self.layers:
            l.export_layer(file)
        file.close()


def import_network(direc):
    file = open(direc)
    line = file.readline().split(",")
    shape = []
    for i in line:
        shape += [int(i)]
    input_size = shape.pop(0)
    network = Network(input_size, shape)
    shape.insert(0,input_size)
    bias = []
    weights = []
    for i in range(1,len(shape)):
        aux_bias = []
        aux_weights = []
        for j in range(shape[i]):
            s=file.readline().replace('\n','').split()
            aux_weights += [np.array(s).astype(np.float)]
            aux_bias += [float(file.readline())]
        weights += [aux_weights]
        bias += [aux_bias]
    network.set_weights(weights)
    network.set_bias(bias)
    file.close()
    return network


def main():
    test_cases = [np.array([0, 0]), np.array([1, 0]), np.array([0, 1]), np.array([1, 1])]
    expected_output = [np.array([1, 0]), np.array([0, 1]), np.array([0, 1]), np.array([1, 0])]
    network = Network(2, [100, 50, 50, 20, 2])
    epoch = 1000
    for i in range(epoch):
        for j in range(4):
            network.train(test_cases[j], expected_output[j],10)
    for i in test_cases:
        network.feed(i)
        output = network.get_output()
        print("("+str(i[0])+","+str(i[1])+")->("+str(output[0])+","+str(output[1])+")")

    network.export_network("asd.txt")



if __name__ == '__main__':
    main()