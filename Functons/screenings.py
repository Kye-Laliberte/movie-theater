import sqlite3
from datetime import datetime


def add_screening(movie_id, theater_id, show_time=None, db_path='app.db'):
    """adds a showing to the screening table"""
    if show_time is None:
        show_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()

        #movie identifier
        cursor.execute("SELECT STATUS FROM Movies WHERE movie_id=?",(movie_id,))
        movie_status = cursor.fetchone()  
        if not movie_status or movie_status[0] != 'active':
            print("Movie is not active or does not exist.")
            return False

        #theader identifier
        cursor.execute("SELECT status FROM Theaters WHERE theater_id = ?", (theater_id,))
        theater_status=cursor.fetchone()
        if not theater_status or theater_status[0] != 'active':
            print("Theater is not active or does not exist.")
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
    

def end_screening(screening_id, db_path='app.db'):
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()

        cursor.execute("SELECT movie_id, theater_id FROM Screenings WHERE screening_id = ?", (screening_id,))
        screening = cursor.fetchone()
    

        if not screening:
            print("no screening at this id")
            return False

        movie_id, theater_id = screening


        cursor.execute("SELECT STATUS FROM Movies WHERE movie_id = ?", (movie_id,))
        movie_status = cursor.fetchone()
        cursor.execute("SELECT status FROM Theaters WHERE theater_id = ?", (theater_id,))
        theater_status = cursor.fetchone()
    

        #Validats status and if the screening is showing
        if movie_status and movie_status[0] != 'active':
            print("Cannot remove — movie is not active.")
            return False

        if theater_status and theater_status[0] != 'active':
            print("Cannot remove — theater is not active.")
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


def get_upcoming_screenings_of_movie(movie_id,date=None,db_path='app.db'):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Screenings WHERE show_time >= ? AND movie_id=? ORDER BY show_time ASC",(date,movie_id))

        showings=cursor.fetchall()
        return [dict(row) for row in showings]

    except sqlite3.Error as e:
        print(f"data err {e}" )
    finally:
        conn.close()