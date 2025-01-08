import random
from typing import Optional, Tuple

from enums import HazardType, CourseType
from .cell import Cell

class Course:
    """A Course holds a grid of cells and has a hole position."""
    def __init__(self, width: int, height: int, course_type: CourseType):
        self.width = width
        self.height = height
        self.course_type = course_type
        self.cells = []  # type: list[list[Cell]]
        self.holePosition = (width // 2, 0)  # By default, near top middle

    def generate(self):
        """
        Procedurally generate the course grid with hazards, etc.
        This is a simplistic generator for demo purposes.
        """
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Random terrain for demonstration only:
                terrain = random.choice(list(HazardType))
                row.append(Cell(terrain))
            self.cells.append(row)

        # Make the bottom row (start) always fairway
        for x in range(self.width):
            self.cells[self.height - 1][x] = Cell(HazardType.FAIRWAY)

        # Make the top row (hole area) always fairway
        for x in range(self.width):
            self.cells[0][x] = Cell(HazardType.FAIRWAY)

        # Place the hole somewhere on the top row
        hole_x = random.randint(0, self.width - 1)
        self.holePosition = (hole_x, 0)

    def getCell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def getHolePosition(self) -> Tuple[int, int]:
        return self.holePosition

    def isValidPosition(self, x: int, y: int) -> bool:
        return (0 <= x < self.width) and (0 <= y < self.height)