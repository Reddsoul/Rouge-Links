class Player:
    """Represents the golfer."""
    def __init__(self, name: str = "Player"):
        self.name = name
        self.totalStrokes: int = 0
        self.mulligansRemaining: int = 6  # Default for Dice Golf

    def incrementStrokes(self, count: int = 1):
        self.totalStrokes += count

    def decrementMulligan(self):
        if self.mulligansRemaining > 0:
            self.mulligansRemaining -= 1

    def getStrokes(self) -> int:
        return self.totalStrokes

    def getMulligans(self) -> int:
        return self.mulligansRemaining