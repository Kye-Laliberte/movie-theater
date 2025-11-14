import datetime
from flask import Flask, jsonify, request
import sys, os
from Functons.getAll import getAll
from Functons.theater import get_theater_by_id,updateStatus,addTheater
from Functons.screenings import add_screening
from Functons.movies import get_movie_by_id
from Functons.review import addreview
from Functons.critics import get_critic
from routes.movies_routes import movies
from routes.critics_routs import critic
from routes.theaters_routes import Theaters


MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')
# Make sure we can import from /Functions
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)

app.register_blueprint(movies)
app.register_blueprint(critic)
app.register_blueprint(Theaters)
@app.route("/")


def home():
    return "Welcome to the Movie Theater API! Try /movies, /theaters, /critics, /screenings"
#reviews
#add review                                 not tested
@app.route("/movie/<int:movie_id>/reviews", methods=["POST"])
def addReview(movie_id):
    data =request.get_json()
    if not data:
         return jsonify({"error": "Missing JSON body"}), 400
    
    critic_id=data.get("critic_id")
    rating=data.get("rating")
    comment=data.get("comment","no comment")
    
    if critic_id is None:
         return jsonify({"error": "critic_id is required"}),400
    if rating is None:
          return jsonify({"rating": "critic_id is required"}),400
    
    try:
         critic_id=int(critic_id)
         rating=float(rating)
         comment=str(comment)
    except ValueError:
         return jsonify({"error": "movie_id and critic_id must be integers; rating must be a number"}), 400
    
    movie=get_movie_by_id(movie_id)
    crit=get_critic(critic_id)
    
    if not movie:
         return jsonify({"error":"movie not found"}),404
    if not crit:
         return jsonify({"error":"critic not found"}),404
    
    val=addreview(movie_id,critic_id,rating,comment)

    if val:
        return jsonify({"message":"review has been added."}),201
    else:
        return jsonify({"error":"cant add errer with inputs"}),400
         


#screening --------------------------------------------------------------------------------------
# adds a screening                                      not tested
@app.route("/movie/<int:movie_id>/screening", methods=["POST"])
def addScreening(movie_id):
    data = request.get_json()

    if not data:
            return jsonify({"error": "Missing JSON body"}), 400
    
    theater_id=data.get("theater_id")
    show_time=data.get("show_time")# this is a DATETIME

    if theater_id is None:
         return jsonify({"error": "theater_id is required"}), 400
    
    try:
        theater_id = int(theater_id)
        show_time = datetime.fromisoformat(show_time)
    except ValueError:
         return jsonify({"error": "movie_id and theater_id must be integers and show_time must be a datetime"}), 400

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
    



if __name__ == "__main__":
    app.run(debug=True)
#reviews -----------------------------------------------------------------------------------------------------------------

#python -m main.app