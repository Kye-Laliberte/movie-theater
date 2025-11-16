from flask import Blueprint, request, jsonify
import sys, os
from Functons.critics import add_critic,get_reviews_by_critic,ban_critic,active_critic,retire_critic,get_critic
from Functons.movies import get_movie_by_id
from Functons.getAll import getAll
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

critic = Blueprint('critic',__name__)

# critic----------------------------------------------------------------------------------

#gets all reviews by critics               
@critic.route("/critics/<int:critic_id>/reviews", methods=["GET"])
def getCritic_Reviews(critic_id):

    if not critic_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    try:
        critic_id=int(critic_id)
    except ValueError:
        return jsonify({"error": "critic_id must be an integer"}), 400

    critic=get_critic(critic_id)
    if not critic:
        return jsonify({"error":f"Critic with ID {critic_id} is not found"}), 404

    data=get_reviews_by_critic(critic_id) or []

    return jsonify({
        "critic":critic,
        "reviews":data
    })

#gets critic by ID
@critic.route("/critics/<int:critic_id>/by_id")
def get_byid(critic_id):
    
    if critic_id is None:
        return jsonify({"error":"a critic_id is needed."}),400
    try:
        critic_id=int(critic_id)
    except ValueError:
        
        return jsonify({"error":"This is not a valid id"}),400
    critic=get_critic(critic_id)
    
    if critic:
        return jsonify(critic), 200
    else:
        return jsonify({"message": "Not a valid critic id"}), 404

# gets all critics of given status 
@critic.route("/critics", methods=["GET"]) 
def get_crit():
    status=request.args.get("status",'active')
    
    status=str(status).lower().strip()
    
    
    if status  not in CRITIC_STATUSES:
        return jsonify({"message":f"{status} is Not a valid status"}),404
    
    data=getAll("Critics",status)
    return jsonify(data if data else{"message":"No Critics found."}),200

# Add new critic
@critic.route("/critics/add", methods=["POST"])
def create_critic():
    data = request.get_json()
    name=data.get("name")
    publication = data.get("publication")
    status = data.get("status", "active")

    if not all([name,publication,status]):
        return jsonify({"errer":"all inputs are needed"})

    try:
        name=str(name).lower().strip()
        publication=str(publication).lower().strip()
        status=str(status).lower().strip()
    except Exception:
        return jsonify({"error":"the (inputs are not vaid) are needed"}),400
    
    if status not in CRITIC_STATUSES:
        return jsonify({"error":"not a valid status"}),400
    
    val=add_critic(name,publication,status)
    if val:
        return jsonify({"message":f"Critic '{name}' added."}), 201
    else:
        return jsonify({"message":"Critic '{name} alredy exists'"}),409
# Update critic status
@critic.route("/critics/<int:critic_id>", methods=["PUT"] )
def update_critic_status(critic_id):
    #data = request.get_json()
    #new_status = data.get("status")
    new_status = request.args.get("status","active")
    status_functions={
        "banned":ban_critic,
        "retired": retire_critic,
        "active":active_critic
    }
    
    try:
        new_status=str(new_status).lower().strip()
    except Exception:
        return jsonify({"error":"the status is an string"}),400
    
    func=status_functions.get(new_status)

    if not func:
        return jsonify({"error": f"Invalid status '{new_status}'"}), 400
    
    updated = func(critic_id)
    if updated:
        return jsonify({"message": f"Critic {critic_id} updated to '{new_status}'"}), 200
    else:
        return jsonify({"error": f"Failed to update movie {critic_id}. Critic may not exist or is alredy {new_status}"}),404

   