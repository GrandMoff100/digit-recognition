class Rectangle:
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def fill(self):
        return [[1] * self.width for _ in range(self.height)]
