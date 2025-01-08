from enums import ClubType

class Club:
    """Base class for clubs."""
    def __init__(self, club_type: ClubType):
        self.clubType = club_type

    def getType(self) -> ClubType:
        return self.clubType

    def getBaseDistance(self) -> int:
        """Override in subclasses."""
        return 0

class Driver(Club):
    def __init__(self):
        super().__init__(ClubType.DRIVER)

    def getBaseDistance(self) -> int:
        return 6  # e.g., 6 spaces

class Iron(Club):
    def __init__(self):
        super().__init__(ClubType.IRON)

    def getBaseDistance(self) -> int:
        return 3  # e.g., 3 spaces normally

class Putter(Club):
    def __init__(self):
        super().__init__(ClubType.PUTTER)

    def getBaseDistance(self) -> int:
        return 1  # e.g., 1 space