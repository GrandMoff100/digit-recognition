import numpy as np
import pandas as pd

from model.network import Layer
from model.train import train

dataset = pd.read_csv(
    "https://raw.githubusercontent.com/cerndb/dist-keras/master/examples/data/mnist.csv"
)

labels = [np.eye(10)[i] for i in dataset.iloc[:, 0].values]

dataset.drop(columns=["label"], inplace=True)

my_network = [
    Layer(784, 128),
    Layer(128, 10),
]

if __name__ == "__main__":
    train(my_network, dataset, labels, epochs=20, batch_size=10, learning_rate=2)
