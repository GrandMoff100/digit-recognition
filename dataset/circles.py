import math
import time
from decimal import Decimal
from typing import List, Generator, Tuple
from functools import cached_property

class Circle:
    diameter: Decimal

    def __init__(self, diameter: float) -> None:
        self.diameter = Decimal(diameter)

    def __str__(self) -> str:
        return "\n".join(map(lambda x: " ".join(map(str, x)), self.fill()))

    def fill(self) -> List[List[int]]:
        arr, size = self.blank_output_array()
        h, k = self.center(size)
        for i in range(size):
            for j in range(size):
                if self.logic(i, j, h, k):
                    arr[j][i] = 1
        return arr

    def logic(self, x: int, y: int, h: int, k: int) -> bool:
        return Decimal(x - h + 1) ** 2 + Decimal(y - k + 1) ** 2 <= self.radius ** 2

    def blank_output_array(self) -> Tuple[List[List[int]], int]:
        size = math.ceil(self.diameter) + 2
        return [[0] * size for _ in range(size)], size

    @cached_property
    def radius(self) -> Decimal:
        return self.diameter / 2

    def center(self, size: int) -> Tuple[int, int]:
        return (math.ceil(size / 2),) * 2


if __name__ == "__main__":
    for i in range(2 * 100, 20 * 100):
        circle = Circle(i / 100)
        print("--------------")
        print(circle)
        print("--------------")
        time.sleep(0.001)
        print(chr(27) + "[2J")
    circle = Circle(i / 100)
    print("--------------")
    print(circle)
    print("--------------")
    