import random

class Dice:
    """Dice logic for Dice Golf mode."""
    @staticmethod
    def rollD6() -> int:
        return random.randint(1, 6)