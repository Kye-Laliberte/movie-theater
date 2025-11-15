
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
@Theaters.route("/theaters/<int:theater_id>/showings", methods=["GET"])
def getShowings(theater_id):
    
    if not theater_id:
        return jsonify({"error":"Missing theaters_id"}),400
    
    theater_id=int(theater_id)

    data=get_screenings_at_theater(theater_id)

    return jsonify(data if data else{"message":f"No showings in this theater"}), (200 if data else 404)

#updates the status of a theater                     
@Theaters.route("/theaters/<int:theater_id>", methods=["PUT"]) 
def theaters_status(theater_id):

    new_status = request.args.get("status","active")
    
    
    new_status=str(new_status).lower().strip()
    
    if new_status not in THEATER_STATUSES:
        return jsonify({"error":f"Invalid status '{new_status}'"}), 400
    
    val=updateStatus(theater_id,new_status)

    if val==2:
        return jsonify({"message":f"theater is alredy {new_status}"})

    if val:
        return jsonify({"message":"Update was sucsess"}),200
    else:
        return jsonify({"message":"you cant update this theater, it has a active showing or is not real."}), 400


if __name__ == "__main__":
    Theaters.run(debug=True)

#adds a theater                                             not tested
@Theaters.route("/theaters/add", methods=["POST"])
def addTheater():
    data = request.get_json()

    if not data:
            return jsonify({"error": "Missing JSON body"}), 400

    name=data.get("name")
    location=data.get("location")
    capacity=data.get("capacity")
    status= data.get("status", "active")

    if not all([capacity,location,name]):
        return jsonify({"error":"Invalid input format"}),400
    
    try:
        name=str(name).lower().strip()
        location=str(location).lower().strip()
        capacity=int(capacity)
        status=str(status).lower().strip()
    except Exception:
        return jsonify({"error":"not valid inputs"}),400
   
    if status not in THEATER_STATUSES:
        return jsonify({"error":f"cant add errer with this {status}"}),400

    
    val=addTheater(name,location,capacity,status)
    if val:
        return jsonify({"message":" theater has been aded."}),201
    else:
        return jsonify({"error":"Failed to add theater or it already exists"}),409
