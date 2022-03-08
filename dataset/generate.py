import os
import random
from pathlib import Path
from typing import Generator, List, Tuple

from PIL import Image

from .circles import Circle
from .rectangles import Rectangle


class Dataset:
    width: int
    minimum_shape_width: int
    output_training: Path = Path("training")
    output_testing: Path = Path("testing")

    def __init__(self, width: int, minimum_shape_width: int = 4) -> None:
        self.width = width
        self.minimum_shape_width = minimum_shape_width
        os.system(f"rm -rf {self.output_training.absolute()}")
        os.system(f"rm -rf {self.output_testing.absolute()}")
        self.output_training.mkdir()
        self.output_testing.mkdir()

    def all_circle_sizes(
        self,
        prec: int,
    ) -> Tuple[List[List[List[int]]], List[Tuple[int, int]]]:
        circles, sizes = [], []
        i = self.minimum_shape_width
        while True:
            arr = Input(Circle(i / prec).fill())
            w, h = arr.size
            if w > self.width or h > self.width:
                break
            if arr.pixels not in circles:
                circles.append(arr.pixels)
                sizes.append(arr.size)
            i += 1
        return circles, sizes

    def all_circles(
        self, prec: int = 5,
    ) -> Generator[Tuple["Output", bool], None, None]:
        circles, sizes = self.all_circle_sizes(prec)
        for circle, (w, h) in zip(circles, sizes):
            for x in range(self.width - w):
                for y in range(self.width - h):
                    pixels = Input(circle).pixels
                    if pixels[0][0] == 0:
                        yield Output(x, y, self.size, pixels), not bool(
                            random.randint(0, 10)
                        )

    def generate_circles(self) -> None:
        training = self.output_training / "circles"
        testing = self.output_testing / "circles"
        training.mkdir()
        testing.mkdir()
        for i, (shape, is_training) in enumerate(self.all_circles()):
            if is_training:
                shape.save(training / f"{str(i).zfill(10)}.png")
            else:
                shape.save(testing / f"{str(i).zfill(10)}.png")

    def all_rectangles(self) -> Generator[Tuple["Output", bool], None, None]:
        for x in range(self.width - self.minimum_shape_width):
            for y in range(self.width - self.minimum_shape_width):
                for width in range(self.minimum_shape_width, self.width - x):
                    for height in range(self.minimum_shape_width, self.width - y):
                        yield Output(
                            x,
                            y,
                            self.size,
                            Input(Rectangle(width, height).fill()).pixels,
                        ), not bool(random.randint(0, 10))

    def generate_rectangles(self):
        training = self.output_training / "rectangles"
        testing = self.output_testing / "rectangles"
        training.mkdir()
        testing.mkdir()
        for i, (shape, is_training) in enumerate(self.all_rectangles()):
            if is_training:
                shape.save(training / f"{str(i).zfill(10)}.png")
            else:
                shape.save(testing / f"{str(i).zfill(10)}.png")

    def generate_all(self):
        self.generate_rectangles()
        self.generate_circles()

    @property
    def size(self) -> Tuple[int, int]:
        return (self.width,) * 2


class Output:
    pixels: List[List[int]]

    def __init__(self, x: int, y: int, size: Tuple[int, int], pixels: List[List[int]]):
        self.pixels = [[0] * size[0] for _ in range(size[1])]
        for j, layer in enumerate(pixels):
            for i, pixel in enumerate(layer):
                if pixel == 1:
                    self.pixels[y + j][x + i] = 1

    def save(self, location: Path) -> None:
        size = len(self.pixels[0]), len(self.pixels)
        img = Image.new("L", size)
        px = img.load()  # type: ignore
        for y, layer in enumerate(self.pixels):
            for x, value in enumerate(layer):
                px[x, y] = value * 255
        img.save(location)


class Input:
    pixels: List[List[int]]

    def __init__(self, pixels: List[List[int]]) -> None:
        self.pixels = self.trim(pixels)

    def trim(self, shape: List[List[int]], depth: int = 0) -> List[List[int]]:
        trim_further = 1 not in shape[0] or 1 not in shape[-1]
        if 1 not in shape[0]:
            shape.pop(0)
        if 1 not in shape[-1]:
            shape.pop(-1)
        if trim_further or depth < 2:
            return self.trim(list(zip(*shape)), depth + 1)  # type: ignore
        return shape

    @property
    def size(self) -> Tuple[int, int]:
        return len(self.pixels[0]), len(self.pixels)
