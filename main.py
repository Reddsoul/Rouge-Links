import tkinter as tk
from tkinter import messagebox
from enums import GameMode, CourseType, ClubType
from models.game_engine import GameEngine, HazardType


class DiceGolfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Golf")
        self.engine = None
        self.grid_buttons = []
        self.current_roll = 0
        self.highlighted_cells = []
        self.previous_position = None  # To track the previous position of the ball

        self.create_top_controls()
        self.initialize_game_mode_window()

    def create_top_controls(self):
        """Create a fixed top control panel."""
        self.top_frame = tk.Frame(self.root, bg="lightgray")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.roll_button = tk.Button(self.top_frame, text="Roll Dice", font=("Arial", 14), command=self.roll_dice)
        self.roll_button.pack(side=tk.LEFT, padx=10)

        self.mulligan_button = tk.Button(self.top_frame, text="Use Mulligan", font=("Arial", 14), command=self.use_mulligan)
        self.mulligan_button.pack(side=tk.LEFT, padx=10)

        self.roll_result_label = tk.Label(self.top_frame, text="Dice Roll: -", font=("Arial", 16), bg="lightgray")
        self.roll_result_label.pack(side=tk.LEFT, padx=10)

        self.stroke_label = tk.Label(self.top_frame, text="Strokes: 0", font=("Arial", 16), bg="lightgray")
        self.stroke_label.pack(side=tk.LEFT, padx=10)

    def initialize_game_mode_window(self):
        """Create a popup window to ask the player for game mode and course type."""
        self.mode_window = tk.Toplevel(self.root)
        self.mode_window.title("Choose Gameplay Mode")

        # Mode Selection
        tk.Label(self.mode_window, text="Choose your mode:", font=("Arial", 14)).pack(pady=5)
        self.mode_var = tk.StringVar(value="DICE_GOLF")
        tk.Radiobutton(self.mode_window, text="Normal Mode", variable=self.mode_var, value="DICE_GOLF").pack()
        tk.Radiobutton(self.mode_window, text="Speed Mode", variable=self.mode_var, value="SPEED_GOLF").pack()

        # Course Selection
        tk.Label(self.mode_window, text="Select a Course:", font=("Arial", 14)).pack(pady=5)
        self.course_var = tk.StringVar(value="SHORT_COURSE")
        tk.Radiobutton(self.mode_window, text="Short Course (Par 3)", variable=self.course_var, value="SHORT_COURSE").pack()
        tk.Radiobutton(self.mode_window, text="Medium Course (Par 4)", variable=self.course_var, value="MEDIUM_COURSE").pack()
        tk.Radiobutton(self.mode_window, text="Long Course (Par 5)", variable=self.course_var, value="LONG_COURSE").pack()

        # Start Game Button
        tk.Button(self.mode_window, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        """Initialize the game engine and setup the grid."""
        mode = GameMode[self.mode_var.get()]
        course = CourseType[self.course_var.get()]

        # Initialize GameEngine
        self.engine = GameEngine()
        self.engine.startGame(mode, course)

        self.mode_window.destroy()  # Close the game mode selection window
        self.setup_scrollable_course_grid()

    def setup_scrollable_course_grid(self):
        """Create a scrollable grid of buttons representing the course."""
        for widget in self.root.winfo_children():
            if widget != self.top_frame:
                widget.destroy()

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.grid_buttons = []
        for y in range(self.engine.activeCourse.height):
            row_buttons = []
            for x in range(self.engine.activeCourse.width):
                btn = tk.Button(
                    scrollable_frame, text=" ", font=("Arial", 16), width=3, height=2,
                    command=lambda x=x, y=y: self.on_grid_click(x, y)
                )
                btn.grid(row=y, column=x, padx=2, pady=2)
                row_buttons.append(btn)
            self.grid_buttons.append(row_buttons)

        self.update_grid()

    def roll_dice(self):
        """Roll the dice and update the GUI."""
        self.current_roll = self.engine.dice.rollD6()
        cell = self.engine.activeCourse.getCell(*self.engine.ball.getPosition())

        if cell and cell.getTerrain() == HazardType.FAIRWAY:
            self.current_roll += 1
        elif cell and cell.getTerrain() == HazardType.SAND:
            self.current_roll -= 1

        self.roll_result_label.config(text=f"Dice Roll: {self.current_roll}")
        self.highlight_valid_moves()

    def clear_highlights(self):
        """Clear previously highlighted cells."""
        for x, y in self.highlighted_cells:
            self.grid_buttons[y][x].config(bg="white")  # Reset background color
        self.highlighted_cells = []


    def highlight_valid_moves(self):
        """Highlight valid moves based on the dice roll."""
        self.clear_highlights()  # Clear any previous highlights

        if self.current_roll <= 0:
            return  # If no roll, do nothing

        ball_x, ball_y = self.engine.ball.getPosition()
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]  # NW, N, NE, E, SE, S, SW, W

        for dx, dy in directions:
            for step in range(1, self.current_roll + 1):  # Loop up to the rolled distance
                x, y = ball_x + dx * step, ball_y + dy * step
                if self.engine.activeCourse.isValidPosition(x, y):  # Check if position is valid
                    self.grid_buttons[y][x].config(bg="lightblue")  # Highlight the cell
                    self.highlighted_cells.append((x, y))
                else:
                    break  # Stop highlighting in this direction if the position is invalid

    def on_grid_click(self, x, y):
        """Handle clicks on the grid."""
        if (x, y) not in self.highlighted_cells:
            messagebox.showwarning("Invalid Move", "You can only move to highlighted cells!")
            return

        # Save the current position as the previous position before moving
        self.previous_position = self.engine.ball.getPosition()

        # Move the ball and count the stroke using GameEngine
        self.engine.ball.setPosition(x, y)
        self.engine.player.incrementStrokes()
        self.update_strokes_label()

        self.current_roll = 0  # Reset roll after move
        self.update_grid()

        if self.engine.checkVictoryCondition():
            messagebox.showinfo("Victory!", f"Congratulations! You completed the hole in {self.engine.calculateScore()} strokes.")
            self.root.destroy()

    def use_mulligan(self):
        """Use a mulligan if available."""
        if self.engine.player.getMulligans() > 0 and self.previous_position:
            self.engine.useMulligan()
            self.engine.ball.setPosition(*self.previous_position)  # Restore the previous position
            self.update_grid()
            messagebox.showinfo("Mulligan Used", f"Mulligans left: {self.engine.player.getMulligans()}")
        else:
            messagebox.showwarning("No Mulligans", "You have no mulligans left or no previous position!")

    def update_strokes_label(self):
        """Update the stroke count display."""
        strokes = self.engine.player.getStrokes()
        self.stroke_label.config(text=f"Strokes: {strokes}")

    def update_grid(self):
        """Update the grid to reflect the current course state."""
        self.clear_highlights()

        for y, row in enumerate(self.grid_buttons):
            for x, btn in enumerate(row):
                cell = self.engine.activeCourse.getCell(x, y)
                if (x, y) == self.engine.ball.getPosition():
                    btn.config(text="o", bg="yellow", font=("Arial", 16))
                elif (x, y) == self.engine.activeCourse.getHolePosition():
                    btn.config(text="●", bg="green", font=("Arial", 16))
                elif cell:
                    terrain = cell.getTerrain()
                    if terrain == HazardType.FAIRWAY:
                        btn.config(text="·", bg="lightgreen")
                    elif terrain == HazardType.SAND:
                        btn.config(text="ᨒ", bg="tan")
                    elif terrain == HazardType.WATER:
                        btn.config(text="♒︎", bg="blue")
                    elif terrain == HazardType.SLOPE:
                        btn.config(text="›", bg="gray")
                    elif terrain == HazardType.TREES:
                        btn.config(text="↟", bg="darkgreen")
                    elif terrain == HazardType.ROUGH:
                        btn.config(text="෴", bg="brown")
                else:
                    btn.config(text=" ", bg="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiceGolfApp(root)
    root.mainloop()