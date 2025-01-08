from typing import Optional

from enums import GameMode, HazardType, ClubType, CourseType
from .dice import Dice
from .clubs import Driver, Iron, Putter
from .course import Course
from .player import Player
from .ball import Ball

class GameEngine:
    """Controls the flow of the game and integrates all components."""
    def __init__(self):
        self.currentMode: Optional[GameMode] = None
        self.dice: Dice = Dice()
        self.activeCourse: Optional[Course] = None
        self.player: Optional[Player] = None
        self.ball: Optional[Ball] = None
        self.strokeCount: int = 0

    def startGame(self, mode: GameMode, courseType: CourseType):
        self.currentMode = mode
        self.player = Player("Golfer1")
        self.ball = Ball()

        # Generate or load a course
        width, height = 8, 13  # Example defaults
        if courseType == CourseType.MEDIUM_COURSE:
            width, height = 10, 15
        elif courseType == CourseType.LONG_COURSE:
            width, height = 12, 17

        self.activeCourse = Course(width, height, courseType)
        self.activeCourse.generate()

        # Place ball at bottom fairway (center)
        start_x = width // 2
        start_y = height - 1
        self.ball.setPosition(start_x, start_y)

        self.strokeCount = 0
        print(f"Game Started: {mode.name} on {courseType.name} course.")
        print(f"Ball start: ({start_x}, {start_y}). Hole at {self.activeCourse.getHolePosition()}.")
        self.renderCourse()

    def takeShot(self, clubType: ClubType, dx: int, dy: int):
        """
        - DICE_GOLF: roll d6, apply terrain modifiers.
        - SPEED_GOLF: pick club base distance, adjust for terrain.
        dx, dy = direction deltas.
        """
        if not (self.currentMode and self.activeCourse and self.ball and self.player):
            print("Game not properly initialized.")
            return

        if self.currentMode == GameMode.DICE_GOLF:
            # For demonstration, roll a D6:
            distance = self.dice.rollD6()

            # If on fairway => +1, if on sand => -1
            cell = self.activeCourse.getCell(self.ball.x, self.ball.y)
            if cell and cell.getTerrain() == HazardType.FAIRWAY:
                distance += 1
            elif cell and cell.getTerrain() == HazardType.SAND:
                distance -= 1

            move_x = dx * distance
            move_y = dy * distance

        else:  # SPEED_GOLF
            if clubType == ClubType.DRIVER:
                club = Driver()
            elif clubType == ClubType.IRON:
                club = Iron()
            else:
                club = Putter()

            distance = club.getBaseDistance()

            # If in sand and not Iron => -1
            cell = self.activeCourse.getCell(self.ball.x, self.ball.y)
            if cell and cell.getTerrain() == HazardType.SAND and clubType != ClubType.IRON:
                distance -= 1

            move_x = dx * distance
            move_y = dy * distance

        # Attempt to move the ball
        new_x = self.ball.x + move_x
        new_y = self.ball.y + move_y

        # Check for bounds
        if not self.activeCourse.isValidPosition(new_x, new_y):
            print("Shot goes out of bounds or into invalid position. Handle penalty or revert shot.")
            # You might revert the move or apply a penalty, up to you:
            # e.g., self.player.incrementStrokes()
        else:
            # Move the ball
            self.ball.setPosition(new_x, new_y)
            # Apply hazard effects
            self.applyHazardEffects()

        # Increment stroke
        self.strokeCount += 1
        self.player.incrementStrokes()
        print(f"Shot taken. Distance: {distance}, Ball now at ({new_x}, {new_y}). Strokes: {self.player.getStrokes()}")

        # After the shot, render course again
        self.renderCourse()

    def applyHazardEffects(self):
        """Check the cell for hazards and apply effects (water, slope, etc.)."""
        if not (self.activeCourse and self.ball and self.player):
            return

        x, y = self.ball.getPosition()
        cell = self.activeCourse.getCell(x, y)
        if cell is None:
            return

        terrain = cell.getTerrain()
        if terrain == HazardType.WATER:
            print("Ball landed in WATER (♒︎)! +1 stroke penalty. Moving ball down 1 space.")
            self.player.incrementStrokes()  # penalty
            self.ball.move(0, 1)
        elif terrain == HazardType.SLOPE:
            # For demo, let slope push ball 1 space downward
            print("Ball slid on SLOPE (›). Moving ball down 1 space.")
            self.ball.move(0, 1)
        elif terrain == HazardType.TREES:
            # In a real game, you'd prevent or handle this more carefully
            print("Encountered TREES (↟). Ball can only pass if shot from fairway, etc.")
        # Add more logic if needed for ROUGH, etc.

    def useMulligan(self):
        """If the player has mulligans left, use one and add a stroke."""
        if self.player.getMulligans() > 0:
            self.player.decrementMulligan()
            self.player.incrementStrokes()  # Mulligan cost
            print(f"Mulligan used! Remaining: {self.player.getMulligans()}. Strokes: {self.player.getStrokes()}")
        else:
            print("No mulligans left!")

    def checkVictoryCondition(self) -> bool:
        """Check if the ball is in the hole."""
        if not (self.activeCourse and self.ball):
            return False
        hole_x, hole_y = self.activeCourse.getHolePosition()
        return (self.ball.x == hole_x and self.ball.y == hole_y)

    def endTurn(self):
        """Check for end-of-turn or victory."""
        if self.checkVictoryCondition():
            print("Ball in the Hole! Congratulations!")
            if self.player:
                print(f"Total Strokes: {self.player.getStrokes()}")
            return True
        return False

    def calculateScore(self) -> int:
        """Return final stroke count or other scoring logic."""
        if self.player:
            return self.player.getStrokes()
        return 0

    # ----------------------------------------------------
    #   ASCII RENDERING OF THE COURSE AND OBJECTS
    # ----------------------------------------------------
    def renderCourse(self):
        """
        Print the course grid to console using the specified symbols.
          o : Ball
          ● : Hole
          ෴ : Rough
          · : Fairway
          › : Slope
          ᨒ : Sand Trap
          ♒︎ : Water
          ↟ : Trees
        """

        if not self.activeCourse:
            return

        hole_x, hole_y = self.activeCourse.getHolePosition()
        ball_x, ball_y = (None, None)
        if self.ball:
            ball_x, ball_y = self.ball.getPosition()

        for y in range(self.activeCourse.height):
            row_str = ""
            for x in range(self.activeCourse.width):

                # If ball is here, print ball symbol
                if x == ball_x and y == ball_y:
                    row_str += "o"
                    continue

                # If hole is here, print hole symbol
                if x == hole_x and y == hole_y:
                    row_str += "●"
                    continue

                # Otherwise, print terrain symbol
                cell = self.activeCourse.getCell(x, y)
                if not cell:
                    row_str += " "  # Out of bounds or missing cell
                    continue

                terrain = cell.getTerrain()
                symbol = self.getTerrainSymbol(terrain)
                row_str += symbol

            print(row_str)
        print()  # Extra newline after printing the course

    def getTerrainSymbol(self, terrain: HazardType) -> str:
        """Map each HazardType to its ASCII symbol."""
        if terrain == HazardType.ROUGH:
            return "෴"
        elif terrain == HazardType.FAIRWAY:
            return "·"
        elif terrain == HazardType.SAND:
            return "ᨒ"
        elif terrain == HazardType.WATER:
            return "♒︎"
        elif terrain == HazardType.SLOPE:
            return "›"
        elif terrain == HazardType.TREES:
            return "↟"
        # Default
        return " "  # Fallback, just in case