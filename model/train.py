
def evaluate_network(network: list[Layer], label: np.ndarray) -> np.ndarray:
    layer_inputs = [label]
    for layer in network:
        layer_inputs.append(layer.forward(layer_inputs[-1]))
    # print(layer_inputs[-1])
    return np.eye(10)[np.argmax(layer_inputs[-1])]


def train(
    network: list[Layer],
    training_data: pd.DataFrame,
    training_labels: list[np.ndarray],
    epochs: int = 20,
    batch_size: int = 10,
    learning_rate: float = 0.1,
) -> None:
    for epoch in range(epochs):
        print(f"Epoch {epoch}")
        for batch_index in range(0, len(training_data), batch_size):
            print("Batch", batch_index // batch_size)
            batch = training_data.loc[batch_index : batch_index + batch_size].values
            batch_labels = training_labels[batch_index : batch_index + batch_size]
            for layer_input, label in zip(batch, batch_labels):
                # Forward pass
                layer_inputs = [layer_input]
                for layer in network:
                    layer_inputs.append(layer.forward(layer_inputs[-1]))
                # Backward pass
                layer_error = label - layer_inputs.pop(-1)
                for layer in reversed(network):
                    layer_error = layer.backward(layer_inputs.pop(-1), layer_error)
            # Update weights and biases with averaged gradients
            for layer in network:
                layer.update_weights(learning_rate=learning_rate, batch_size=batch_size)
            for layer in network:
                layer.update_biases(learning_rate=learning_rate, batch_size=batch_size)
            # Evaluate accuracy on the training set
            score = 0
            for image, label in zip(training_data.values, training_labels):
                if np.array_equal(evaluate_network(network, image), label):
                    score += 1
            print("Accuracy:", score / len(training_data))