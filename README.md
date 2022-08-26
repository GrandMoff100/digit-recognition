# Digit Recognition

Classic hello world of neural networks. Classify handwritten digit images as integer digits. Using the MNIST Handwritten digit dataset.
This project is implemented from scratch, using only numpy and pandas, I've implemented a neural network that works (admittedly not very well at first, by eventually gets fairly accurate after a few epochs).

## Math

Using the calculus of backpropogation we calculus how much we need to adjust each weight and bias based on how it affects the cost function.
In practice that means calculating the partial derivative of the cost function with respect to each weight and bias variable, averaging them over each batch, scaling them by a learning rate constant, before finally adjusting the actual weights and biases.

## Installation

```bash
pip install poetry

poetry install
```

## Running

```py
poetry run main.py
```

## Experimenting

Head over to `main.py` and experiment with the number of layers, layer sizes, batch size, learning rate, etc.

Have fun!
