from datetime import datetime
from fastapi import FastAPI, HTTPException, Path
from Functons.theater import get_theater_by_id
from Functons.screenings import add_screening
from Functons.movies import get_movie_by_id
from Functons.review import addreview
from Functons.critics import get_critic
from routes.movies_routes import movie
from routes.critics_routs import critics
from routes.theaters_routes import Theaters
from pydantic import BaseModel,validator 
app = FastAPI(title="Movie Theater API")

app.include_router(movie)
app.include_router(critics)
app.include_router(Theaters)

@app.get("/")
def home():
    return {"message":"Welcome to the Movie Theater API! Try /movies, /theaters, /critics, /screenings"}

class Review(BaseModel):
    critic_id: int
    rating: float
    comment: str = "no comment"
class Screening(BaseModel):
    theater_id:int
    show_time:datetime


#reviews
#add from pydantic import BaseModel,validator     
@app.post("/reviews/{movie_id}/add",status_code=201)
def addReview(review: Review,movie_id: int =Path(...,gt=0,description="adds a Review")):

    movie=get_movie_by_id(movie_id)
    crit=get_critic(review.critic_id)
    
    if not movie:
        raise HTTPException(status_code=404,detail="movie not found")
    
    if not crit:
        raise HTTPException(status_code=404,detail="critic not found")
    
    val=addreview(movie_id,review.critic_id,review.rating,review.comment)

    if val:
        return {"message":"review has been added."}

    raise HTTPException(status_code=400,detail="Cannot add review; check inputs")
        
#screening --------------------------------------------------------------------------------------
# adds a screening                                      not tested
@app.post("/movie/{movie_id}/screening", status_code=201)
def addScreening(screning: Screening,movie_id: int=Path(...,gt=0,description="adds a screening")):
    """adds Screening"""

    movie = get_movie_by_id(movie_id)
    theat = get_theater_by_id(screning.theater_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if not theat:
        raise HTTPException(status_code=404,detail="theater not found")

    val = add_screening(movie_id, screning.theater_id, screning.show_time)

    if val:
        return {"message": "Screening has been added."}
    raise HTTPException(status_code=400, detail="Cannot add screening; theater or move my be inactave")
    

    
#reviews -----------------------------------------------------------------------------------------------------------------

#python -m main.app



#    uvicorn main.app:app --reload
#/docs 
#/redoc
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)