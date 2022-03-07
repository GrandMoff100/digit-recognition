import os
import copy
from pathlib import Path
from typing import List, Generator, Any
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

    def all_circles(self) -> Generator[List[List[int]], None, None]:
        if 0:
            yield [[1]]

    def generate_circles(self) -> None:
        path = self.output / "circles"
        path.mkdir()
        for i, shape in enumerate(self.all_circles()):
            Input(shape).save(path / f"{str(i).zfill(10)}.png")

    def all_rectangles(self) -> Generator[List[List[int]], None, None]:
        for x in range(self.width - self.minimum_shape_width):
            for y in range(self.width - self.minimum_shape_width):
                for width in range(self.minimum_shape_width, self.width - x):
                    for height in range(self.minimum_shape_width, self.width - y):
                        yield Rectangle(width, height).fill()

    def generate_rectangles(self):
        path = self.output / "rectangles"
        path.mkdir()
        for i, shape in enumerate(self.all_rectangles()):
            Input(shape).save(path / f"{str(i).zfill(10)}.png")

    def generate_all(self):
        self.generate_rectangles()
        self.generate_circles()


class Input:
    pixels: List[List[int]]

    def __init__(self, pixels: List[List[int]]) -> None:
        self.trim(pixels)
        self.pixels = pixels

    def trim(self, shape: List[List[int]]) -> None:
        trim_further = 1 not in shape[0] or 1 not in shape[-1]
        if 1 not in shape[0]:
            shape.pop(0)
        if 1 not in shape[-1]:
            shape.pop(-1)
        if trim_further:
            self.trim(list(zip(*shape)))  # type: ignore

    def save(self, location: Path) -> None:
        size = len(self.pixels[0]), len(self.pixels)
        img = Image.new("RGB", size)
        px = img.load()  # type: ignore
        for y, layer in enumerate(self.pixels):
            for x, value in enumerate(layer):
                px[x,y] = (value * 255,) * 3
        img.save(location)

