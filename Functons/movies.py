import sqlite3 
valid_status = ('active','inactive','archived')

def add_movie(title,genre,release_year,status='active',db_PATH='app.db'):

    try:
    
        conn =sqlite3.connect(db_PATH)
        cursor= conn.cursor()

        
        if status not in valid_status:
            print(f"{status} is not a valid status")
            conn.close()
            return False
        
        cursor.execute("SELECT * FROM Movies WHERE title=? AND genre=? AND release_year=? ",(title,genre,release_year))
        val=cursor.fetchone()
        
        if val:# movie alredy exists
            conn.close()
            return None

        cursor.execute("""
            INSERT INTO Movies (title, genre, release_year, STATUS)
            VALUES (?, ?, ?, ?)
        """, (title, genre, release_year, status))

        conn.commit()
        print(f"Movie '{title}' added successfully!")
        return True
    
    except sqlite3.IntegrityError:
        print(f"Movie '{title}' already exists in the database.")
        return False
    except sqlite3.Error as e:
        print(f"Datta errer {e}")
        return False
    
    finally:
        conn.close()

def updateMoviesSTATUS(movies_id,status,db_path='app.db'):
   
    status = status.lower().strip()
    #Check that status is valid
    if status not in valid_status:
            print(f"{status} is not a valid status")
            return False
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor() 
        
        #Check if movie exists
        cursor.execute("SELECT STATUS FROM Movies WHERE movie_id=?",(movies_id,))
        Movie=cursor.fetchone()


        #cheks if it is still screning 
        cursor.execute("SELECT theater_id FROM Screenings WHERE movie_id=?",(movies_id,))
        screening=cursor.fetchone()
        if screening:
            print("this is still showing")
            return None

        if not Movie:
            print("Movie dosent exist")
            return False

        if Movie[0]==status:
            print("alredy at the givin STATUS")
            return "same"
        

        cursor.execute("""UPDATE Movies
                       SET STATUS=?
                       WHERE movie_id=?;
                       """,(status,movies_id))
        conn.commit()

        print(f"Movie {movies_id} status updated to '{status}'.")
        return True
    except sqlite3.Error as e:
         print(f"DATA ere {e}")
         return False
    finally:
        conn.close()

def activeMovie(id,db_path='app.db'):
    return updateMoviesSTATUS(id,'active',db_path)

def inactiveMovie(id,db_path='app.db'):
    return updateMoviesSTATUS(id,'inactive',db_path)

def archivedMovie(id,db_path='app.db'):
    return updateMoviesSTATUS(id,'archived',db_path)

def get_movie_by_id(movie_id,db_path='app.db'):
    try:
        conn=sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor=conn.cursor()
        
        cursor.execute("SELECT * FROM Movies WHERE movie_id=?",(movie_id,))
        movie=cursor.fetchone()

        if not movie:
            print("no movie at this id")
            return False
        
        return dict(movie)

    except sqlite3.Error as e:
        print("data errer {e}")
        return False
    finally:
        conn.close()

def get_movies_by_genre(genre,db_path='app.db'):
    try:
        conn=sqlite3.connect(db_path)
        conn.row_factory =sqlite3.Row
        cursor=conn.cursor()
        
        cursor.execute("SELECT * FROM Movies WHERE genre=? AND STATUS='active'",(genre,))
        movies=cursor.fetchall()

        if not movies:
            print("no movie with this genre")
            return []
        
        return [dict(row) for row in movies]

    except sqlite3.Error as e:
        print("data errer {e}")
        return False
    finally:
        conn.close()

def search_movies(title_part,db_path='app.db'):
    try:
        conn=sqlite3.connect(db_path)
        conn.row_factory =sqlite3.Row
        cursor=conn.cursor()
        
        cursor.execute("SELECT * FROM Movies WHERE title LIKE ? AND STATUS='active'",(f"%{title_part}%",))
        movie=cursor.fetchall()

        if not movie:
            print("no movie at this name part")
            return False
        
        return [dict(row) for row in movie]

    except sqlite3.Error as e:
        print("data errer {e}")
        return False
    finally:
        conn.close()

def get_reviews_for_movie(movie_id,db_path='app.db'):
    try:

        conn=sqlite3.connect(db_path)
        conn.row_factory =sqlite3.Row
        cursor=conn.cursor()

        #movie id dosent exised
        cursor.execute("SELECT * FROM Movies WHERE movie_id=?",(movie_id,))#---------------------------------------------------added
        val=cursor.fetchone()
        if not val:
            print("movie id dosent exised")
            return None
        
        #cursor.execute("""SELECT * FROM Reviews WHERE movie_id=?""",(movie_id,))
        cursor.execute("""SELECT
                       --Review info
                       r.review_id,
                       r.rating,
                       r.comment,
                       r.review_date,
                       
                       --Movie info
                       m.movie_id,
                       m.title AS movie_title,
                       m.genre,
                       m.release_year,
                       
                        -- critic info
                        c.critic_id,
                        c.name AS critic_name,
                        c.publication                       
                       FROM Reviews r
                       JOIN Critics c ON r.critic_id = c.critic_id
                       JOIN Movies  m ON r.movie_id = m.movie_id
                       WHERE r.movie_id=?""",(movie_id,))


        movies=cursor.fetchall()

        if not movies:
            print("no reviews for this movie")
            return []
        
        return [dict(row) for row in movies]

    except sqlite3.Error as e:
        print(f"data errer {e}")
        return False
    finally:
        conn.close()

def get_screenings_for_movie(movie_id,db_path='app.db'):
    try:

        conn=sqlite3.connect(db_path)
        conn.row_factory =sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Movies WHERE movie_id=?",(movie_id,))#---------------------------------------------------added
        val=cursor.fetchone()
        if not val:
            print("not a valid movie id")
            return None
        
        cursor.execute("""SELECT 
                       --Screenings info
                        s.screening_id,
                        s.show_time,
                       
                        --movie info
                        m.movie_id,
                        m.title AS movie_title,
                        m.genre,
                       m.release_year,
                       m.STATUS AS movie_status,

                       --theater
                       t.theater_id,
                       t.name,
                       t.location,
                       t.STATUS AS theater_status

                       FROM Screenings s
                       JOIN Theaters t ON s.theater_id = t.theater_id
                       JOIN Movies  m ON s.movie_id = m.movie_id

                       WHERE s.movie_id=?
                       AND m.status = 'active'
                       AND t.status = 'active'
                       --AND s.show_time > CURRENT_TIMESTAMP remeber to add back when testing is done
                       """,(movie_id,))
        
        movies=cursor.fetchall()

        if not movies:
            print("no Screenings for this movie")
            return []
        
        return [dict(row) for row in movies]

    except sqlite3.Error as e:
        print(f"data errer {e}")
        return False
    finally:
        conn.close()   