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
    output: Path = Path("shapes")

    def __init__(self, width: int, minimum_shape_width: int = 4) -> None:
        self.width = width
        self.minimum_shape_width = minimum_shape_width
        os.system(f"rm -rf {self.output.absolute()}")
        self.output.mkdir()

    def all_circle_sizes(
        self, prec: int
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

    def all_circles(self, prec: int = 5) -> Generator["Output", None, None]:
        circles, sizes = self.all_circle_sizes(prec)
        for circle, (w, h) in zip(circles, sizes):
            for x in range(self.width - w):
                for y in range(self.width - h):
                    pixels = Input(circle).pixels
                    if pixels[0][0] == 0:
                        yield Output(x, y, self.size, pixels)

    def generate_circles(self) -> None:
        path = self.output / "circles"
        path.mkdir()
        for i, shape in enumerate(self.all_circles()):
            shape.save(path / f"{str(i).zfill(10)}.png")

    def all_rectangles(self) -> Generator["Output", None, None]:
        for x in range(self.width - self.minimum_shape_width):
            for y in range(self.width - self.minimum_shape_width):
                for width in range(self.minimum_shape_width, self.width - x):
                    for height in range(self.minimum_shape_width, self.width - y):
                        yield Output(
                            x,
                            y,
                            self.size,
                            Input(Rectangle(width, height).fill()).pixels,
                        )

    def generate_rectangles(self):
        path = self.output / "rectangles"
        path.mkdir()
        for i, shape in enumerate(self.all_rectangles()):
            shape.save(path / f"{str(i).zfill(10)}.png")

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
        if not bool(random.randint(0, 10)):
            return
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
