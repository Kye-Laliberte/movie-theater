from flask import Blueprint, request, jsonify
from Functons.movies import get_movie_by_id,add_movie,get_movies_by_genre,get_reviews_for_movie
from Functons.movies import get_screenings_for_movie,activeMovie,archivedMovie,inactiveMovie
from Functons.getAll import getAll
from Functons.screenings import add_screening, deletescreening
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

movies = Blueprint("movies", __name__)

# movies------------------------------------------------------------------------------

#gets all movies by genre

# gets all movies of given status
@movies.route("/movie", methods=["GET"])
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

#gets movie by id                                   
@movies.route("/movie/<int:movie_id>/by_id",methods=["GET"])
def get_movieByid(movie_id):
    #movie_id= request.args.get("movie_id")
  
    if movie_id is None:
      return jsonify({"error": "Missing movie_id"}), 400
      
    try:
        movie_id=int(movie_id)
    except ValueError:
        return jsonify({"error":"this is not a valid id format."}),400
  
    data=get_movie_by_id(movie_id)
    return jsonify(data if data else{"message":f"not a valad id"}), (200 if data else 404)   

# gets reviews for a moivie                                                             
@movies.route("/movie/<int:movie_id>/reveiws",methods=["GET"])
def getmovie_reveiws(movie_id):

    if movie_id is None:
      return jsonify({"error": "Missing movie_id"}), 400
    
    data=get_reviews_for_movie(movie_id)
    
    if data is False:
        return jsonify({"error": "Movie not found"}), 404

    if data==[]:
        return jsonify({
            "message": "Movie exists but has no reviews",
            "reviews": []}), 200
    return jsonify({
        "message": "Reviews retrieved",
        "reviews": data}), 200

#screenings for a moivie 
@movies.route("/movie/<int:movie_id>/screenings",methods=["GET"])
def getmovie_screenings(movie_id):

    if movie_id is None:
      return jsonify({"error": "Missing movie_id"}), 400
    
    data=get_screenings_for_movie(movie_id)
    
    if data is False:
        return jsonify({"message": "screenings not found"}), 404

    if data==[]:
        return jsonify({
            "message": "No screenings exists",
            "reviews": []}), 200

    return jsonify({
        "message": "screenings retrieved",
        "reviews": data}), 200


#updates movies status                                         not testid or done
@movies.route("/movie/<int:movie_id>",methods=["PUT"])
def updateStatus(movie_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    
    new_status = data.get("status")

    if new_status is None:
        return jsonify({"error":"must have a status to update to"}),400

    new_status=str(new_status).lower().strip()

    status_functions = {
    "active": activeMovie,
    "inactive": inactiveMovie,
    "archived": archivedMovie
    }
    func=status_functions.get(new_status)
    
    if not func:
        return jsonify({"error": f"Invalid status '{new_status}'."}), 400
    
    updated = func(movie_id)
    if updated is None:
        return jsonify({"message":"Movie may is be showing"}),400
    if updated:
        return jsonify({"message": f"Movie {movie_id} updated to '{new_status}'"}), 200
    else:
        return jsonify({"error": f"Failed to update movie {movie_id}. not exist"}),404
    
#adds a movie                          
@movies.route("/movie/add",methods=["POST"])
def addMovie():
    data= request.get_json()

    title = data.get("title")
    genre = data.get("genre")
    release_year = data.get("release_year")
    status = data.get("status",'active')

    if not all([title, genre, release_year, status]):
        return jsonify({"error": "All fields (title, genre, release_year, status) are required"}), 400
    
    try:
        title=str(title).lower().strip()
        genre=str(genre).lower().strip()
        release_year=int(release_year)
        status=str(status).lower().strip()
    except Exception:
        return jsonify({"error":"input is not valid"}),400
    
    if status not in MOVIE_STATUSES:
        return jsonify({"error":"not a valid status"}),400
    
    val=add_movie(title,genre,release_year,status)

    if val is None:
        return jsonify({"error":"failed to add movie or it already existed"}),409  

    if val:
        return jsonify({"message":"movie added"}),201
    else:
        return jsonify({"error":""}),400 

#adds screening
@movies.route("/movie/screenings/add",methods=["POST"])
def addScreening():
    data=request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    
    movie_id=data.get("movie_id")
    theater_id=data.get("theater_id")
    show_time= data.get("show_time") # is a datetime but can be a none
    try:
        movie_id=int(movie_id)
        theater_id=int(theater_id)
    except Exception:
        return jsonify ({"error":"input is not valid"}), 400
    
    var=add_screening(movie_id,theater_id,show_time)
    if var is None:
        return jsonify({"erreor":"bolth movie and theater need to be active"}),400

    if var:
        return jsonify({"message":"screening has been added"}),201
    return jsonify({"error":"movie or theater doesn't exist"}),400

@movies.route("/DELETE/screenings/<int:screening_id>",methods=["DELETE"])
def delete_screening(screening_id):
    
    if screening_id is None:
      return jsonify({"error": "Missing screening_id"}), 400
    
    val=deletescreening(screening_id)
    
    if val is None:
        return jsonify({"error":"no screening at this id"}),404
    
    if val:
        return jsonify({"message":"Successfully deleated from table"}),200
    else:
        return jsonify({"error":"Cannot delete a screening that has not yet occurred"}),403