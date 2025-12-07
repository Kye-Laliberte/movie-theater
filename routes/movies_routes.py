#from flask import Blueprint, request, jsonify

from fastapi import FastAPI,APIRouter,HTTPException,Query,Path
from pydantic import BaseModel,validator 
from enum import Enum
from typing import Optional
from datetime import datetime
from Functons.movies import get_movie_by_id,add_movie,get_movies_by_genre,get_reviews_for_movie
from Functons.movies import get_screenings_for_movie,activeMovie,archivedMovie,inactiveMovie
from Functons.getAll import getAll
from Functons.screenings import add_screening, deletescreening
MOVIE_STATUSES = ('active', 'active', 'archived')
THEATER_STATUSES=('active', 'inactive', 'maintenance')
CRITIC_STATUSES= ('active','banned','retired')

class MOVIESTATUSES(str,Enum):
    active ='active'
    inactive='inactive'
    archived='archived'

class MOVIE(BaseModel):
    title: str
    genre:str
    release_year: int
    status: str

    @validator("title","genre","status")
    def normalize_str(cls,v):
        if not isinstance(v,str):
            raise ValueError("Must be a string")
        return v.lower().strip()

    @validator("status")
    def validate_status(cls,v):
        if v not in MOVIE_STATUSES:
            raise ValueError(f"invalid status {v}")
        return v




#movies = Blueprint("movies", __name__)

movie=APIRouter(prefix="/movie",tags=["movie"])
# movies------------------------------------------------------------------------------

#gets all movies by genre

# gets all movies of given status
@movie.get("/")
def get_movies(status:MOVIESTATUSES):
    # Get the query string parameter
    #status = request.args.get("status", "active").lower().strip()
    
    # Fetch movies using your getAll function
    data = getAll("Movies", status)

    if not data:
        #return jsonify({"message": f"No movies found with status '{status}'."}), 404
        raise HTTPException(status_code=404,detail=f"No movies found with status '{status}'.")
    #return jsonify(data), 200
    return data

#gets movie by id                                   
@movie.get("/{movie_id}/by_id")
def get_movieByid(movie_id: int =Path(...,description="The ID of the movie to retrieve",gt=0) ):
    
      
    data=get_movie_by_id(movie_id)

    if data:
        return data
    raise HTTPException(status_code=404,detail=f"movie id with {movie_id} not found")
       

# gets reviews for a moivie                                                             
@movie.get("/{movie_id}/reveiws")
def getmovie_reviews(movie_id: int=Path(...,gt=0,description="gets reviews for a moivie")):

    #if movie_id is None:
    #  return jsonify({"error": "Missing movie_id"}), 400
    
    data=get_reviews_for_movie(movie_id)
    
    if not data and not data==[]:
        raise HTTPException(status_code=404,detail="movie id not found")
    
    if data==[]: 
        return {"message": f"Movie with ID {movie_id} exists but has no reviews"}
    
    return data
    

#screenings for a movie 
@movie.get("/{movie_id}/screenings")
def getmovie_screenings(movie_id: int =Path(...,gt=0,description="get screenings for a movie")):

    data=get_screenings_for_movie(movie_id)
    
    if data is None:
        raise HTTPException(status_code=404,detail="movie id not found")

    if data==[]: 
        return {"message": f"Movie with ID {movie_id} exists but has no screenings"}

    return data


#updates movies status                                         
@movie.put("/{movie_id}")
def updateStatus(status:MOVIESTATUSES,movie_id:int=Path(...,gt=0,description="updates movie status")):
    """updates movie status"""
    
    status_functions = {
    "active": activeMovie,
    "inactive": inactiveMovie,
    "archived": archivedMovie
    }

    func=status_functions.get(status.value)
    
    updated = func(movie_id)
    if updated is None:
        raise HTTPException(status_code=400,detail=f"Movie is still showing; cannot archive or inactive.")
    
    if updated =="same":
        raise HTTPException(status_code=404,detail=f"Movie {movie_id} is already currently {status.value}")

    if updated:
        return {"message": f"Movie {movie_id} updated to '{status.value}'"}
    
    raise HTTPException(status_code=404,detail=f"Failed to update movie {movie_id}.douse not exist")
        
    
#adds a movie                          
@movie.post("/add")
def addMovie(new_movie:MOVIE, status_code=201):
    """ Add a new movie to the database."""

    val=add_movie(new_movie.title,new_movie.genre,new_movie.release_year,new_movie.status)

    if val is None:
        raise HTTPException( status_code=409,detail="movie already existed")
         
    if val:
        return {"message":f"{new_movie.title} has been added"}
    
    raise HTTPException(status_code=400,detail="failed to add movie")

class ScreeningCreate(BaseModel):
    movie_id: int
    theater_id: int
    show_time: Optional[datetime] = None

#adds screening
@movie.post("/screenings/add",status_code=201)
def addScreening(screen:ScreeningCreate):
    """Add a new screening for a movie."""
    
    movie_id=screen.movie_id
    theater_id=screen.theater_id
    show_time=screen.show_time

    var=add_screening(movie_id,theater_id,show_time)
    
    if var is None:
        raise HTTPException(status_code=400,detail="bolth movie and theater need to be active, or do not exist")
    
    if var:
        return {"message":"screening has been added"}

    raise HTTPException (status_code=400,detail="Screening already exists or cannot be added")



#deleted/screenings
@movie.delete("/screenings/{screening_id}")
def delete_screening(screening_id: int):
    """Deletes a screening if it has already occurred."""
    val=deletescreening(screening_id)
    
    if val is None:
        raise HTTPException(status_code=404,detail="no screening at this id")
           
    if val:
        return{"message":"Successfully deleted from table"}

    raise HTTPException(status_code=403,detail="Cannot delete a screening that has not yet occurred")