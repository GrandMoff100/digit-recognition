from typing import Generator, Optional

import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid function.
    """
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of the sigmoid function.
    """
    return np.multiply(sigmoid(x), 1 - sigmoid(x))


def cost(output: np.ndarray, y: np.ndarray) -> float:
    """
    Cost function.
    """
    return np.sum(np.square(output - y)) / 2


def cost_derivative(output: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Derivative of the cost function.
    """
    return output - y


class Layer:
    def __init__(self, inp_size: int, out_size: int) -> None:
        self.weights = np.random.rand(inp_size, out_size)
        self.biases = np.random.rand(out_size)
        self.weight_gradient = np.zeros((inp_size, out_size))
        self.biases_gradient = np.zeros(out_size)

    def update_weights(self, learning_rate: float, batch_size: int) -> None:
        """
        Updates the weights of the Layer.
        """
        self.weights -= self.weight_gradient / batch_size * learning_rate
        self.weight_gradient = np.zeros(self.weights.shape)

    def update_biases(self, learning_rate: float, batch_size: int) -> None:
        """
        Updates the biases of the Layer.
        """
        self.biases -= self.biases_gradient / batch_size * learning_rate
        self.biases_gradient = np.zeros(self.biases.shape)

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass of the Layer.
        """
        return sigmoid(np.matmul(inputs, self.weights) + self.biases)

    def backward(self, inputs: np.ndarray, error: np.ndarray) -> np.ndarray:
        """
        Backward pass of the layer.
        Returns the error of the previous layer.
        """
        weighted_error = error * sigmoid_derivative(
            np.matmul(inputs, self.weights) + self.biases
        )
        self.weight_gradient -= np.array(
            [
                [previous_neuron * error for error in weighted_error]
                for previous_neuron in inputs
            ]
        )
        self.biases_gradient -= np.sum(
            error * sigmoid_derivative(self.forward(inputs)), axis=0
        )
        return np.matmul(
            self.weights,
            error * sigmoid_derivative(np.matmul(inputs, self.weights) + self.biases),
        )
