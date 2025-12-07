import sqlite3
from datetime import datetime

def addreview(movie_id,critic_id,rating,comment="",db_path='app.db'):

    try:
        
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()
        #movies varification
        cursor.execute("""SELECT STATUS FROM Movies 
                       WHERE movie_id=?""",(movie_id,))
        movie=cursor.fetchone()
        if not movie and movie[0]!='active':
            print("this movie Is not active or dousent exest")
            return False
        
        #critic varifcation
        cursor.execute("SELECT STATUS FROM Critics WHERE critic_id =?",(critic_id,))
        
        crit=cursor.fetchone()
        if not crit and crit[0]!='active':
            print("Critic is not active or does not exist.")
            return False
        
        
        #INSERT INTO Reviews
        cursor.execute("""
            INSERT INTO Reviews (movie_id, critic_id, rating, comment)
            VALUES (?, ?, ?, ?);
        """, (movie_id, critic_id, rating, comment))
       
        conn.commit()
        print("Review added successfully.")
        return True    


    except sqlite3.Error as e:
        print(f"data Errer {e}")
        return False
    finally:
        conn.close()

def get_review_id(review_id,db_path='app.db'):
    try:
        conn= sqlite3.connect(db_path)
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Reviews WHERE review_id=?",(review_id,))
        rev=cursor.fetchone()

        if not rev:
            print("no review with this id")
            return False

        return dict(rev)
        
    except sqlite3.Error as e:
        print(f"data ere {e}")
    finally:
        conn.close()

def get_reviews_for_movie(movie_id,db_path='app.db'):
    try:
        conn= sqlite3.connect(db_path)
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Reviews WHERE movie_id=?",(movie_id,))
        
        rows=cursor.fetchall()


        if not rows:
            print("there are no reviews for this movie")
            return []
        
        

        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"data ere {e}")
        return False
    finally:
        conn.close()

def get_reviews_by_critic(critic_id,db_path='app.db'):
    try:
        conn= sqlite3.connect(db_path)
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Reviews WHERE critic_id=?",(critic_id,))
        revs=cursor.fetchall()

        if not revs:
            print("there this critic has no reviews")
            return []

        return [dict(row) for row in revs]
        
    except sqlite3.Error as e:
        print(f"data ere {e}")
        return False
    finally:
        conn.close()

def get_average_rating(movie_id,db_path='app.db'):
    try:
        conn= sqlite3.connect(db_path)
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT rating FROM Reviews WHERE movie_id=?",(movie_id,))
        ratings=cursor.fetchall()

        if not ratings:
            print("No reviews found for this movie.")
            return None
        
        values=[row["rating"] for row in ratings if row["rating"] is not None]
        avg_rating = sum(values) / len(values)
        return round(avg_rating, 2)
    
    except sqlite3.Error as e:
        print(f"data errere {e} ")
        return False
    finally:
        conn.close()


def get_reviews_movie(movie_id, db_path='app.db'):
    """
    Fetch reviews for a movie including critic and movie info.
    Returns a list of nested dictionaries.
    """

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # allows us to access columns by name
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM Movies WHERE movie_id = ?", (movie_id,))
        movie_exists = cursor.fetchone()
        if not movie_exists:
            print("Movie not found.")
            return False

        # SQL JOIN to get critic name and movie title in the same query
        cursor.execute("""
            SELECT 
                r.review_id,
                r.rating,
                r.comment,
                r.review_date,
                c.critic_id,
                c.name AS critic_name,
                m.movie_id,
                m.title AS movie_title
            FROM Reviews r
            JOIN Critics c ON r.critic_id = c.critic_id
            JOIN Movies  m ON r.movie_id = m.movie_id
            WHERE r.movie_id = ?
        """, (movie_id,))

        rows = cursor.fetchall()  # fetch all matching reviews

        if not rows:
            return []  # no reviews for this movie

        # Step 3 — restructure flat rows into nested JSON
        result = []
        for row in rows:
            review_dict = {
                "review_id": row["review_id"],
                "rating": row["rating"],
                "comment": row["comment"],
                "review_date": row["review_date"],
                "critic": {             # nested critic object
                    "id": row["critic_id"],
                    "name": row["critic_name"]
                },
                "movie": {              # nested movie object
                    "id": row["movie_id"],
                    "title": row["movie_title"]
                }
            }
            result.append(review_dict)

        return result

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        conn.close()