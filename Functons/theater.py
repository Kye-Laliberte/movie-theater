import sqlite3

valid_status = ('active', 'inactive', 'maintenance')

def addTheater(name,location,capacity,STATUS='active',db_PATH='app.db'):
    """adds a Theater"""  
    

    if STATUS not in valid_status:
            print(f"{STATUS} is not a valid status")
            return False
    if capacity <= 0:
          print("must have 1 or more seating")
          return False
    try:
          
        conn= sqlite3.connect(db_PATH)
        cursor =conn.cursor()

        cursor.execute("""INSERT INTO Theaters (name,location,STATUS,capacity)
        VALUES (?,?,?,?) 
        """,(name,location,STATUS,capacity))
        
        conn.commit()
        print("added Theater")
        return True
    except sqlite3.IntegrityError:
          print("Theater archive already exists")
          return False
    except sqlite3.Error as e:
          print(f"data errere {e}")
          return False
          
    finally:
        conn.close()

def updateStatus(theater_id,new_status,db_path='app.db'):
      """update STATUS of a theater"""
      new_status=new_status.lower().strip()
      
      #Validates is STATUS is usable
      if new_status not in valid_status:
            print(f"{new_status} is not a valid STATUS")
            return False

      try:
            
            conn=sqlite3.connect(db_path) 
            cursor=conn.cursor()

            cursor.execute("SELECT STATUS FROM Theaters WHERE theater_id=?",(theater_id,))
            Theat=cursor.fetchone()

            #validats Theaters
            if not Theat:
                  print(f"no Theaters with {theater_id} as id")
                  return False
            #Theaters STATUS if your duplicating it
            if Theat[0]==new_status:
                  print(f"Theaters is alredy {new_status}")
                  return False
            
            #finds showings in the theater
            cursor.execute("SELECT * FROM Screenings WHERE theater_id=? ",(theater_id,))
            screening=cursor.fetchone()      
            if screening:
                  print("cant shut down theater when showing a movie")
                  return False


            cursor.execute("""UPDATE Theaters
                   SET STATUS=? 
                   WHERE theater_id=?
            """,(new_status,theater_id))
            conn.commit()

            print(f"Theaters {theater_id} STATUS updated to '{new_status}'.")
            return True


      except sqlite3.Error as e:
           print(f"data errer: {e}")
           return False
      finally:
           conn.close()


def inactiveTeater(theater_id,db_path='app.db'):
     return  updateStatus(theater_id,'inactive',db_path)


def maintenanceTheater(theater_id,db_Path='app.db'):
     return updateStatus(theater_id,'maintenance',db_Path)

def activeTeater(theater_id,db_path='app.db'):
     return  updateStatus(theater_id,'active',db_path)

def get_theater_by_id(theater_id,db_path='app.db'):
     try:
            conn=sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor =conn.cursor()

            cursor.execute("SELECT * FROM Theaters WHERE theater_id=? AND STATUS ='active'",(theater_id,))
            theater=cursor.fetchone()

            if not theater:
                  print("no theater at this ID")
                  return False
            
            return dict(theater)


     except sqlite3.Error as e:
          print(f"data errer {e}")
          return False
     finally:
           conn.close() 

def get_screenings_at_theater(theater_id,db_path='app.db'):
      try:
            conn=sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor =conn.cursor()

            cursor.execute("SELECT * FROM Theaters WHERE theater_id=? AND STATUS ='active'",(theater_id,))
            theater=cursor.fetchone()

            if not theater:
                  print("no theater at this ID")
                  return False
            
            cursor.execute("SELECT * FROM Screenings WHERE theater_id=?",(theater_id,))
            showings=cursor.fetchall()
            
            if not showings:
                  return []

            return [dict(row) for row in showings]

      except sqlite3.Error as e:
            print(f"Dtata erer {e}")
            return False
      finally:
            conn.close()