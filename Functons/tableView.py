import sqlite3
import os

db_path = 'app.db'

def view_table(table_name):
    """Display all rows of the specified table."""
    if not os.path.exists(db_path):
        print("Database not found. Run setup first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        if not columns_info:
            print(f"Table '{table_name}' does not exist.")
            return
        column_names = [col[1] for col in columns_info]
        
        # Fetch all rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Print header
        header = " | ".join(column_names)
        print(header)
        print("-" * len(header) * 2)
        
        # Print rows
        for row in rows:
            print(" | ".join(str(item) for item in row))
        
        print(f"\nTotal rows: {len(rows)}")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    while True:
        table = input("Enter table name to view (or 'quit' to exit): ").strip()
        if table.lower() == 'quit':
            break
        view_table(table)
        print("\n")