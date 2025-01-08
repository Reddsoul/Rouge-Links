from typing import Tuple

class Ball:
    """Represents the position of the ball."""
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def setPosition(self, x: int, y: int):
        self.x = x
        self.y = y

    def getPosition(self) -> Tuple[int, int]:
        return (self.x, self.y)