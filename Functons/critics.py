import sqlite3

DB_PATH = 'app.db'
valid_status = ('active', 'banned', 'retired')

def add_critic(name, publication, status='active', db_path='app.db'):
    """Add a new critic to the database."""
        

    if status not in valid_status:
        print(f"{status} is not a valid status.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Critics (name, publication, STATUS)
            VALUES (?, ?, ?);
        """, (name, publication, status))

        conn.commit()
        print(f"Added {name} to the Critics table.")
        return True

    except sqlite3.IntegrityError:
        print("Critic already exists.")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


def update_critic_status(critic_id, new_status, db_path='app.db'):
    """Change a critic's status (e.g., retire, ban, reactivate)."""
    new_status = new_status.lower().strip()
    
    if new_status not in valid_status:
        print(f"{new_status} is not a valid status.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT STATUS FROM Critics WHERE critics_id = ?", (critic_id,))
        critic = cursor.fetchone()

        if not critic:
            print("Critic not found.")
            return False

        if critic[0] == new_status:
            print(f"Critic is already {new_status}.")
            return False

        cursor.execute("""
            UPDATE Critics
            SET STATUS = ?
            WHERE critics_id = ?;
        """, (new_status, critic_id))
        conn.commit()

        print(f"Critic {critic_id} status updated to '{new_status}'.")
        return True

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        conn.close()

def retire_critic(critic_id, db_path='app.db'):
    """Set a critic's status to retired."""
    return update_critic_status(critic_id, 'retired', db_path)

def ban_critic(critic_id, db_path='app.db'):
    """Set a critic's status to banned."""
    return update_critic_status(critic_id, 'banned', db_path)

def active_critic(critic_id,db_path='app.db'):
    """Set a critic's status to active."""
    return update_critic_status(critic_id, 'active', db_path)

def get_critic(critic_id, db_path='app.db'):
    try:

        conn=sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Critics WHERE critics_id=?",(critic_id,))
        val=cursor.fetchone()

        if not val:
            return False
        
        return dict(val)

    except sqlite3.Error as e:
        print(f"data erere {e}")
        return False

def get_reviews_by_critic(critic_id, db_path='app.db'):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor =conn.cursor()

         # Check if critic exists
        cursor.execute("SELECT * FROM Critics WHERE critics_id = ?", (critic_id,))
        critic= cursor.fetchone()

        if not critic:
            print("Critic not found.")
            return False
        
         # Get all reviews by this critic
        cursor.execute("SELECT * FROM Reviews WHERE critic_id=?",(critic_id,))

        rev=cursor.fetchall()

        if not rev:
            return []

        return [dict(row) for row in rev]


    except sqlite3.Error as e:
        print(f"data eree {e}")
        return False
    finally:
        conn.close()

def delete_critic_permanently(critic_id, db_path='app.db'):
    """Permanently delete a critic (only if not active)."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if critic exists and is safe to delete
        cursor.execute("SELECT STATUS FROM Critics WHERE critics_id= ?", (critic_id,))
        critic = cursor.fetchone()

        if not critic:
            print("Critic not found.")
            return False

        if critic[0] == 'active':
            print("Cannot delete an active critic. Retire or ban first.")
            return False


     # Check if critic has reviews
        cursor.execute("SELECT COUNT(*) FROM Reviews WHERE critic_id=?",(critic_id,))
        review_count = cursor.fetchone()[0]

        if review_count > 0:
            print(f"Cannot delete critic {critic_id} — they have {review_count} review(s).")
            return False


        cursor.execute("DELETE FROM Critics WHERE critics_id = ?", (critic_id,))
        conn.commit()
        print(f"Critic {critic_id} permanently deleted.")
        return True

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        conn.close()