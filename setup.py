import sqlite3
import os
from datetime import datetime, timedelta

db_path = 'app.db'

def set_up_tables(schema_path="data.sql"):
    """Creates tables from SQL file and seeds initial data."""
    
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Step 1: Execute schema to create tables
        with open(schema_path, "r", encoding="utf-8") as file:
            schema_sql = file.read()
        cursor.executescript(schema_sql)
        print(" Tables created successfully.")
        
        # Step 2: Seed Movies
        movies = [
            ("The Silent Dawn", "Drama", 2023, "active"),
            ("Crimson Horizon", "Action", 2024, "active"),
            ("Neon Skies", "Sci-Fi", 2022, "active"),
            ("Echoes of Tomorrow", "Thriller", 2023, "inactive")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Movies (title, genre, release_year, status)
            VALUES (?, ?, ?, ?);
        """, movies)
        print(" Movies table seeded.")
        
        # Step 3: Seed Theaters
        theaters = [
            ("Grandview Cinema", "Downtown", "active", 120),
            ("Skyline Theater", "Uptown", "active", 200),
            ("Riverview Screens", "Riverside", "maintenance", 150)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Theaters (name, location, STATUS, capacity)
            VALUES (?, ?, ?, ?);
        """, theaters)
        print(" Theaters table seeded.")
        
        # Step 4: Seed Critics
        critics = [
            ("Ava Collins", "The Film Review", "active"),
            ("James Redd", "Cinema Central", "active"),
            ("Elena Cruz", "The Reel Times", "retired")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Critics (name, publication, STATUS)
            VALUES (?, ?, ?);
        """, critics)
        print(" Critics table seeded.")
        
        # Step 5: Seed Screenings
        now = datetime.now()
        screenings = [
            (1, 1, (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
            (2, 2, (now + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
            (3, 1, (now + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"))
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Screenings (movie_id, theater_id, show_time)
            VALUES (?, ?, ?);
        """, screenings)
        print(" Screenings table seeded.")


        # Step 6: Seed Reviews   



        conn.commit()
        print("\n Database setup and seeding complete!")
    
    except sqlite3.Error as e:
        print("SQLite error:", e.args)
        conn.rollback()
    finally:
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    set_up_tables()