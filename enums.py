from enum import Enum, auto

class GameMode(Enum):
    DICE_GOLF = auto()
    SPEED_GOLF = auto()

class HazardType(Enum):
    WATER = auto()
    SAND = auto()
    SLOPE = auto()
    TREES = auto()
    ROUGH = auto()
    FAIRWAY = auto()

class CourseType(Enum):
    SHORT_COURSE = auto()
    MEDIUM_COURSE = auto()
    LONG_COURSE = auto()

class ClubType(Enum):
    DRIVER = auto()
    IRON = auto()
    PUTTER = auto()