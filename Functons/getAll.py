import sqlite3
VALID_TABLES = ('Critics', 'Theaters', 'Movies', 'Screenings', 'Reviews')
STATUS_TABLES = {
    "Critics": ('active','banned','retired'),# i did have a inactive 
    "Theaters": ('active', 'inactive', 'maintenance'),
    "Movies": ('active', 'inactive', 'archived')
}
def getAll(table, status=None, db_path='app.db'):
    """gets all table rows, can let you filter by its status"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # restrict which tables can be queried
        if table not in VALID_TABLES:
            print(f"Invalid or unauthorized table name: {table}")
            return False
        
        if not table:
            print(f"Invalid table name: {table}")
            return False

        

        #checks if it has a status to use 
        if status is not None:
            if table not in STATUS_TABLES:
                print(f"'{table}' does not have a STATUS feature.")
                return False
            
        #get all the pasubal status for a table
            valid_status = STATUS_TABLES[table]

            if status not in valid_status:
                print("not valid status")
                return False
        
          
            cursor.execute(f"SELECT * FROM {table} WHERE status = ?;", (status,))
        #get alll
        else:
            cursor.execute(f"SELECT * FROM {table};")

        results = [dict(row) for row in cursor.fetchall()]
        if not results:
            print(f"No records found in {table}")
            return False
        
        print(f"Found {len(results)} record(s) in {table}.")
        return results

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    finally:
        conn.close()
   
def get_critics_by_status(status='active'):
    return getAll("Critics",status)

def get_Theaters_by_status(status='active'):
    return getAll("Theaters",status)

def get_Movies_by_status(status='active'):
    return getAll("Movies",status)