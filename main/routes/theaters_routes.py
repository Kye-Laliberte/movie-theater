
from flask import Blueprint, request, jsonify
import sys, os
from Functons.critics import add_critic,get_reviews_by_critic
from Functons.movies import get_movie_by_id
from Functons.getAll import getAll
from Functons.theater import get_screenings_at_theater,get_theater_by_id,updateStatus,addTheater
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

Theaters =Blueprint("Theaters",__name__)

#Theaters------------------------------------------------------------------------------wating for testing
#gets all active theaters
@Theaters.route("/theaters", methods=["GET"])
def get_Theaters():
    stat=request.args.get("status","active").lower().strip()
    
    if stat  not in THEATER_STATUSES:
        return jsonify({"message":f"{stat} is Not a valid status"})
    
    data=getAll("Theaters",stat)
    return jsonify(data if data else {"message": f"No theaters found with status '{stat}'."}), (200 if data else 404)

#gets Theaters by id                                not tested
@Theaters.route("/theaters/by_id", methods=["GET"])
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
@Theaters.route("/theaters/showings", methods=["GET"])
def getShowings():
    theater_id=request.args.get("theaters_id")
    
    if not theater_id:
        return jsonify({"error":"Missing theaters_id"}),400
    
    data=get_screenings_at_theater(theater_id)

    return jsonify(data if data else{"message":f"No showings in this theater"}), (200 if data else 404)

#updates the status of a theater                     
@Theaters.route("/theaters/<int:theaters_id>", methods=["PUT"]) 
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
    Theaters.run(debug=True)

#adds a theater                                             not tested
@Theaters.route("/theaters/add", methods=["POST"])
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
