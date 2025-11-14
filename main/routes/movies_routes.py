from flask import Blueprint, request, jsonify
from Functons.critics import add_critic,get_reviews_by_critic
from Functons.movies import get_movie_by_id,add_movie,get_movies_by_genre,get_reviews_for_movie,get_screenings_for_movie
from Functons.getAll import getAll
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

movies = Blueprint("movies", __name__)

# movies------------------------------------------------------------------------------
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

#gets movie by id                                   not tested
@movies.route("/movie/by_id",methods=["GET"])
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

#adds a movie                           not tested
@movies.route("/movie/add",methods=["POST"])
def addMovie():
    data= request.get_json()

    title = data.get("title")
    genre = data.get("genre")
    release_year = data.get("release_year")
    status = data.get("status")

    if not all([title, genre, release_year, status]):
        return jsonify({"error": "All fields (title, genre, release_year, status) are required"}), 400
    
    try:
        title=title.lower().strip()
        genre=genre.lower().strip()
        release_year=release_year.strip()
        status=status.lower().strip()
    except ValueError:
        return jsonify({"error":"input is not valid"}),400
    
    if status not in MOVIE_STATUSES:
        return jsonify({"error":"not a valid status"}),400
    
    val=add_movie(title,genre,release_year,status)
       
    if val:
        return jsonify({"message":"movie added"}),201
    else:
        return jsonify({"error":"faled to add movie or it alredy existed"}),409
