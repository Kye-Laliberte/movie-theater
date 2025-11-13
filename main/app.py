from flask import Flask, jsonify, request
import sys, os
from Functons.getAll import getAll
from Functons.critics import add_critic,get_reviews_by_critic,ban_critic,retire_critic,active_critic,get_critic
from Functons.theater import get_screenings_at_theater,get_theater_by_id,updateStatus,addTheater
from Functons.screenings import add_screening
from Functons.movies import get_movie_by_id
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')
# Make sure we can import from /Functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)

@app.route("/")


def home():
    return "Welcome to the Movie Theater API! Try /movies, /theaters, /critics, /screenings"

# movies
# gets all movies of given status
@app.route("/movie", methods=["GET"])
def get_movies():
    # Get the query string parameter
    status = request.args.get("status", "active").lower().strip()

    # Check if status is valid
    if status not in MOVIE_STATUSES:
        
        return jsonify({"error": f"Invalid status '{status}'. Valid options: {MOVIE_STATUSES}"}), 400

    # Fetch movies using your getAll function
    data = getAll("Movies", status)

    if not data:
        return jsonify({"message": f"No movies found with status '{status}'."}), 404
    
    return jsonify(data), 200

#gets movie by id                                   not tested
@app.route("/movie/by_id",methods=["GET"])
def get_movieByid():
    movie_id= request.args.get("movie_id")
  
    if movie_id is None:
      return jsonify({"error": "Missing movie_id"}), 400
      
    try:
        movie_id=int(movie_id)
    except ValueError:
        return jsonify({"error":"this is not a valid id format."}),400
  
    data=get_movie_by_id(movie_id)
    return jsonify(data if data else{"message":f"not a valad id"}), (200 if data else 404)   


# critic
#gets all reviews by critics               
@app.route("/critics/reviews", methods=["GET"])
def getCritic_Reviews():

    critic_id=request.args.get("critics_id")

    if not critic_id:
        return jsonify({"error": "Missing 'id' query parameter"}), 400
    
    data=get_reviews_by_critic(critic_id)
    return jsonify(data if data else {"message": f"No reviews found by critic_id '{critic_id}'."}), (200 if data else 404)

# gets all critics of given status 
@app.route("/critics", methods=["GET"]) 
def get_crit():
    status=request.args.get("status").lower().strip()
    
    if status  not in CRITIC_STATUSES:
        return jsonify({"message":f"{status} is Not a valid status"}),404
    
    data=getAll("Critics",status)
    return jsonify(data if data else{"message":"No Critics found."}),200

# Add new critic
@app.route("/critics/add", methods=["POST"])
def create_critic():
    data = request.get_json()
    name=data.get("name").lower().strip()
    publication = data.get("publication").lower().strip()
    status = data.get("status", "active").lower().strip()

    add_critic(name,publication,status)
    return jsonify({"message":f"Critic '{name}' added."}), 201

# Update critic status
@app.route("/critics/<int:critic_id>", methods=["PUT"] )
def update_critic_status(critic_id):
    data = request.get_json()
    new_status = data.get("status").lower().strip()
    
    # Choose function based on new status
    if new_status == "banned":
        ban_critic(critic_id)
    elif new_status == "retired":
        retire_critic(critic_id)
    elif new_status == "active":
        active_critic(critic_id)
    else:
        return jsonify({"error": f"Invalid status '{new_status}'"}), 400

    return jsonify({"message": f"Critic {critic_id} updated to '{new_status}'"}), 200


#Theaters
#gets all active theaters
@app.route("/theaters", methods=["GET"])
def get_Theaters():
    stat=request.args.get("status","active").lower().strip()
    
    if stat  not in THEATER_STATUSES:
        return jsonify({"message":f"{stat} is Not a valid status"})
    
    data=getAll("Theaters",stat)
    return jsonify(data if data else {"message": f"No theaters found with status '{stat}'."}), (200 if data else 404)

#gets Theaters by id                                not tested
@app.route("/theaters/by_id", methods=["GET"])
def get_Theaters_by_id():
  theaters_id= request.args.get("theaters_id")
  
  if theaters_id is None:
      return jsonify({"error": "Missing theaters_id"}), 400
      
  try:
    theaters_id=int(theaters_id)
  except ValueError:
        return jsonify({"error":"this is not a valid id format."}),400
  
  data=get_theater_by_id(theaters_id)
  return jsonify(data if data else{"message":f"not a valad id"}), (200 if data else 404)   

#gets all showing for a theater                             
@app.route("/theaters/showings", methods=["GET"])
def getShowings():
    theater_id=request.args.get("theaters_id")
    
    
    if not theater_id:
        return jsonify({"error":"Missing theaters_id"}),400
    
    data=get_screenings_at_theater(theater_id)

    return jsonify(data if data else{"message":f"No showings in this theater"}), (200 if data else 404)

#updats the status of a theater                     
@app.route("/theaters/<int:theaters_id>", methods=["PUT"]) 
def theaters_status(theaters_id):
    data = request.get_json()
    new_status = data.get("status").lower().strip()
    
    if new_status not in THEATER_STATUSES:
        return jsonify({"error":f"Invalid status '{new_status}'"}), 400
    
    val=updateStatus(theaters_id,new_status)
    if val:
        return jsonify({"message":"Update was sucsess"}),200
    else:
        return jsonify({"message":"you cant update this theater it has a showing"}), 200
if __name__ == "__main__":
    app.run(debug=True)

#adds a theater                                             not tested
@app.route("/theaters/add", methods=["POST"])
def addTheater():
    data = request.get_json()

    if not data:
            return jsonify({"error": "Missing JSON body"}), 400

    name=data.get("name").lower().strip()
    location=data.get("location").lower().strip()
    capacity=int(data.get("capacity"))
    status = data.get("status", "active").lower().strip()
    
    if status not in THEATER_STATUSES:
        return jsonify({"error":f"cant add errer with this {status}"})

    
    val=addTheater(name,location,capacity,status)
    if val:
        return jsonify({"message":" theater has been aded."}),201
    else:
        return jsonify({"error":"cant add errer with inputs"}),400

#screening 
# adds a screening                                      not tested
@app.route("/screening/add", methods=["POST"])
def addScreening():
    data = request.get_json()

    if not data:
            return jsonify({"error": "Missing JSON body"}), 400
    
    movie_id=data.get("movie_id")
    theater_id=data.get("theater_id")
    show_time=data.get("show_time")# this is a DATETIME

    if movie_id is None:
        return jsonify({"error": "movie_id is required"}),400
    if theater_id is None:
         return jsonify({"error": "theater_id is required"}), 400
    
    try:
        movie_id = int(movie_id)
        theater_id = int(theater_id)
    except ValueError:
         return jsonify({"error": "movie_id and theater_id must be integers"}), 400

    movie=get_movie_by_id(movie_id)
    theater=get_theater_by_id(theater_id)

    if not movie:
        return jsonify({"error":"movie id is missing"}),404
    if not theater:
        return jsonify({"error":"theater id is missing"}),404

    val=add_screening(movie_id,theater_id,show_time)

    if val:
        return jsonify({"message":"screening has been added."}),201
    else:
        return jsonify({"error":"cant add errer with inputs"}),400
#reviews        

#python -m main.app