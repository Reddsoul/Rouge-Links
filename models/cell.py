from enums import HazardType

class Cell:
    """Each cell on the course. Could contain hazards."""
    def __init__(self, terrain: HazardType):
        self.terrain = terrain

    def getTerrain(self) -> HazardType:
        return self.terrain