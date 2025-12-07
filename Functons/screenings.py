import sqlite3
from datetime import datetime


def add_screening(movie_id, theater_id, show_time=None, db_path='app.db'):
    """adds a showing to the screening table"""
    
    if show_time is None:
        show_time=datetime.now() 
    
    if isinstance(show_time, datetime):
        show_time = show_time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()

        #movie identifier
        cursor.execute("SELECT 1 FROM Movies WHERE movie_id=? AND status='active'",(movie_id,))
        movie_status = cursor.fetchone()  
        if movie_status is None:
            print("Movie does not exist.")
            return None
        
        #theader identifier
        cursor.execute("SELECT 1 FROM Theaters WHERE theater_id = ? AND status='active'", (theater_id,))
        theater_status=cursor.fetchone()
        if theater_status is None:
            print("Theater is not active or does not exist.")
            return None
        
        #check if screening already exists
        cursor.execute("SELECT * FROM Screenings WHERE movie_id=? AND theater_id=? AND show_time=?",(movie_id, theater_id, show_time))
        if cursor.fetchone():
            print("Screening already exists.")
            return False
        
        #INSERT INTO Screenings
        cursor.execute(
            "INSERT INTO Screenings (movie_id, theater_id, show_time) VALUES (?, ?, ?);",
            (movie_id, theater_id, show_time)
        )
        conn.commit()
        print("Screening added.")
        return True
    except sqlite3.Error as e:
        print(f"Data erer {e}")
        return False

    finally:
        conn.close()

def updateScreeningTime(screening_id, new_time, db_path='app.db'):

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT show_time FROM Screenings WHERE screening_id=?", (screening_id,))
        screening = cursor.fetchone()
        if not screening:
            print("Screening not found.")
            return False
        
        try:
            datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid datetime format. Use YYYY-MM-DD HH:MM:SS")
            return False
        
        cursor.execute("UPDATE Screenings SET show_time = ? WHERE screening_id = ?", (new_time, screening_id))
        conn.commit()
        print(f"Screening time updated to {new_time}.")
        return True

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        conn.close()
    

def deletescreening(screening_id, db_path='app.db'):
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()

        cursor.execute("SELECT show_time FROM Screenings WHERE screening_id = ?", (screening_id,))
        screening = cursor.fetchone()
        
        if not screening:
            print("no screening at this id")
            return None

        show_time_str=screening[0]
        show_time= datetime.fromisoformat(show_time_str)

        if show_time>datetime.now():
            print("Cannot delete a screening that has not yet occurred.")
            return False

        cursor.execute("DELETE FROM Screenings WHERE screening_id = ?",(screening_id,))
        conn.commit()
        print("sucsesfull DELETE")
        return True

    except sqlite3.Error as e:
        print(f"data errer{e}")
        return False
    finally:
        conn.close()


def get_screening_by_id(screening_id, db_path='app.db'):

    try:
        conn =sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor=conn.cursor()
    
        cursor.execute("SELECT * FROM Screenings WHERE screening_id =? ;",(screening_id,))
        screning=cursor.fetchone()
    
        if not screning:
            return False

        return dict(screning)
    
    except sqlite3.Error as e:
        print(f"data erer{e}")
        return False
    
def get_upcoming_screenings(date=None, db_path='app.db'):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Screenings WHERE show_time >= ? ORDER BY show_time ASC",(date,))

        showings=cursor.fetchall()
        return [dict(row) for row in showings]

    except sqlite3.Error as e:
        print(f"data err {e}" )

