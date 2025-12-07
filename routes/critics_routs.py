#from flask import Blueprint, request, jsonify
#import sys, os
from enum import Enum
from fastapi import APIRouter, HTTPException,Query,Path
from pydantic import BaseModel,validator
from Functons.critics import add_critic,get_reviews_by_critic,ban_critic,active_critic,retire_critic,get_critic
from Functons.movies import get_movie_by_id
from Functons.getAll import getAll
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

#critic = Blueprint('critic',__name__)
critics=APIRouter(prefix="/critics",tags=["critic"])
# critic----------------------------------------------------------------------------------



class CriticCreate(BaseModel):
    name: str
    publication: str
    status: str = "active"

    @validator("name", "publication", "status")
    def normalize_str(cls, v):
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        return v.lower().strip()

    @validator("status")
    def validate_status(cls, v):
        if v not in CRITIC_STATUSES:
            raise ValueError("Invalid status")
        return v
    

class CriticStatus(str, Enum):
    active = "active"
    banned = "banned"
    retired = "retired"


#gets all reviews by critics               
@critics.get("/{critic_id}/reviews")
def getCritic_Reviews(critic_id: int = Path(...,description="gets all reviews by critics",gt=0) ):     
    data=get_reviews_by_critic(critic_id)
    if data:
        return data 
    raise HTTPException(status_code=404,detail=f"Critic with ID {critic_id} is not found")
    
#gets critic by ID
@critics.get("/{critic_id}/by_id")
def get_byid(critic_id: int =Path(...,gt=0)):
    critic=get_critic(critic_id)
    if critic:
        return critic
    else:
        raise HTTPException(status_code=404, detail="Not a valid critic id")
    
# gets all critics of given status 
@critics.get("/") 
def get_crit(status: CriticStatus = Query(CriticStatus.active, description="Filter critics by status")):   
    
    data=getAll("Critics",status.value)
    if data:
        return data
    return{"message":"No Critics found."}

# Add new critic
@critics.post("/add",status_code=201)
def create_critic(newCritic: CriticCreate):

    val = add_critic(newCritic.name, newCritic.publication, newCritic.status)
    
    if val:
        return {"message":f"Critic '{newCritic.name}' added."}
    
    raise HTTPException(status_code=409,detail=f"Critic '{newCritic.name}' already exists")
    
# Update critic status
@critics.put("/{critic_id}")
def update_critic_status(critic_id: int, new_status:  CriticStatus):
    
    status_functions={
        "banned":ban_critic,
        "retired": retire_critic,
        "active":active_critic
    }
    
    func=status_functions.get(new_status.value)

    if not func:
        raise HTTPException(status_code=400, detail=f"Invalid status '{new_status.value}'")
    updated = func(critic_id)
    
    if updated:
        return{"message": f"Critic {critic_id} updated to '{new_status.value}'"}
    else:
         raise HTTPException(status_code=404,detail=f"Critic may not exist or is already '{new_status.value}'")

   