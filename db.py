import sqlite3

def init_db(db_path: str = "dicegolf.db"):
    """
    Initialize the SQLite database with the tables 
    (players, saves, courses, cells) if they do not exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create players table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create saves table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        current_mode TEXT,
        strokes INTEGER,
        mulligans_remaining INTEGER,
        ball_pos_x INTEGER,
        ball_pos_y INTEGER,
        saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(player_id) REFERENCES players(id)
    )
    """)

    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_type TEXT,
        width INTEGER,
        height INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create cells table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cells (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        x INTEGER,
        y INTEGER,
        hazard_type TEXT,
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """)

    conn.commit()
    conn.close()

def save_game_state(db_path: str, save_data: dict) -> None:
    """
    Example function to save a game state into the 'saves' table.
    `save_data` might look like:
    {
      "player_id": 1,
      "current_mode": "DICE_GOLF",
      "strokes": 5,
      "mulligans_remaining": 3,
      "ball_pos_x": 10,
      "ball_pos_y": 5
    }
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO saves (
            player_id,
            current_mode,
            strokes,
            mulligans_remaining,
            ball_pos_x,
            ball_pos_y
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        save_data["player_id"],
        save_data["current_mode"],
        save_data["strokes"],
        save_data["mulligans_remaining"],
        save_data["ball_pos_x"],
        save_data["ball_pos_y"]
    ))

    conn.commit()
    conn.close()