import click
from typing import Generator, List, Optional


def denest(shape: List[List[int]]) -> Generator[int, None, None]:
    for layer in shape:
        for pixel in layer:
            yield pixel


class Network:
    size: int

    def __init__(self, size: int, bias: int, weights: Optional[List[float]]) -> None:
        self.size = size
        if weights is None:
            weights = [0] * self.size**2
        self.weights = weights
        self.bias = bias

    def feed(self, image: List[List[int]]) -> bool:
        out = sum([inp * weight for inp, weight in zip(denest(image), self.weights)])
        return out > self.bias

    def adjust(self, image: List[List[int]], direction: int) -> None:
        for j, layer in enumerate(image):
            for i, pixel in enumerate(layer):
                self.weights[j * self.size + i] += direction * pixel

    def train(self, image: List[List[int]], expected: bool) -> None:
        output = self.feed(image)
        if output is True and expected is False:
            self.adjust(image, -1)
        elif output is False and expected is True:
            self.adjust(image, 1)
        # click.echo(self.weights)
