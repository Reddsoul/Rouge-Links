"""
Entry point. Orchestrates initialization, starts a game, simulates a few shots, and saves state.
"""
from enums import GameMode, CourseType, ClubType
from models.game_engine import GameEngine
from db import init_db, save_game_state

def main():
    # Initialize database
    init_db("dicegolf.db")

    # Create and start the game
    engine = GameEngine()
    engine.startGame(GameMode.DICE_GOLF, CourseType.SHORT_COURSE)

    # Example shots (just to demonstrate)
    engine.takeShot(ClubType.DRIVER, dx=0, dy=-1)  # Move "up"
    finished = engine.endTurn()
    if finished:
        return

    engine.takeShot(ClubType.IRON, dx=0, dy=-1)
    finished = engine.endTurn()
    if finished:
        return

    # Save game state example
    if engine.player and engine.ball and engine.currentMode:
        save_data = {
            "player_id": 1,  # Typically from your 'players' table
            "current_mode": engine.currentMode.name,
            "strokes": engine.player.getStrokes(),
            "mulligans_remaining": engine.player.getMulligans(),
            "ball_pos_x": engine.ball.x,
            "ball_pos_y": engine.ball.y
        }
        save_game_state("dicegolf.db", save_data)
        print("Game state saved. Exiting demo.")

if __name__ == "__main__":
    main()