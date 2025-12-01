
#from flask import Blueprint, request, jsonify
# import sys, os

from fastapi import APIRouter, HTTPException,Query,Path
from pydantic import BaseModel
from typing import Optional, List

from Functons.critics import add_critic,get_reviews_by_critic
from Functons.movies import get_movie_by_id
from Functons.getAll import getAll
from Functons.theater import get_screenings_at_theater,get_theater_by_id,updateStatus,addTheater
MOVIE_STATUSES = ('active', 'inactive', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

Theaters = APIRouter(prefix="/theaters", tags=["theaters"])#router
#Theaters =Blueprint("Theaters",__name__)
class TheaterIn(BaseModel):
    name: str
    location: str
    capacity: int
    status: Optional[str] = "active"

#Theaters
#gets all active theaters
@Theaters.get("/")
def get_Theaters(status: str=Query("active")):
    status=status.lower().strip()
    
    if status  not in THEATER_STATUSES:
        raise HTTPException(status_code=400,detail=f"{status} not a valid status")
    
    data=getAll("Theaters",status)

    if not data:
        raise HTTPException(status_code=404,detail=f"No theaters found with status {status}")
    
    return data

#gets Theaters by id    <int:critic_id>                     
@Theaters.get("/{theaters_id}/by_id")
def get_Theaters_by_id(theaters_id: int = Path(...)):
  
  if theaters_id is None:
      raise HTTPException(status_code=400,detail="theater id is needed")
   
  data=get_theater_by_id(theaters_id)
  if not data:
    raise HTTPException(status_code=404,detail="theater not found")
  return data  

#gets all showing for a theater                             
@Theaters.get("/{theater_id}/showings")
def getShowings(theater_id: int=Path(...)):

    if not theater_id:
        raise HTTPException(status_code=400,detail="theater id is needed")

    data=get_screenings_at_theater(theater_id)

    if not data:
        raise HTTPException(status_code=404,detail="No showing in this theater")
    return

#updates the status of a theater                     
@Theaters.put("/{theater_id}") 
def theaters_status(theater_id: int =Path(...), 
                    status: str=Query("active")):

    new_status=status.lower().strip()
    
    if new_status not in THEATER_STATUSES:
        raise HTTPException(status_code=400,detail="not a valid status")
    val=updateStatus(theater_id,new_status)

    if val==2:
        return {"message":f"theater is alredy {new_status}"}

    if val:
        return {"message":"Update was sucsess"}
    else:
        raise HTTPException(status_code=400,detail="Cannot update this theater, it has active showing or not real.")


@Theaters.post("/add", status_code=201)
def add_theater_route(theater: TheaterIn):
    
    theater.status=theater.status.lower().strip()

    if theater.status not in THEATER_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status {theater.status}")
    
    
    theater.location=theater.location.lower().strip()
    theater.name=theater.name.lower().strip()
    
    val = addTheater(theater.name, theater.location, theater.capacity, theater.status)
    if not val:
        raise HTTPException(status_code=409, detail="Failed to add theater or it already exists")
    
    return {"message": "Theater has been added."}