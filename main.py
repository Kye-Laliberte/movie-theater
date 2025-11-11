import sqlite3
from Functons.tableView import view_table
from Functons.movies import add_movie,activeMovie,updateMoviesSTATUS,archivedMovie,inactiveMovie,get_movie_by_id,get_screenings_for_movie,get_movies_by_genre,search_movies
from Functons.theater import addTheater,inactiveTeater,maintenanceTheater,activeTeater,get_theater_by_id,get_screenings_at_theater
from Functons.critics import ban_critic,retire_critic,add_critic,delete_critic_permanently,active_critic,get_critic,get_reviews_by_critic
from Functons.movies import activeMovie,archivedMovie,inactiveMovie
from Functons.screenings import add_screening,end_screening,updateScreeningTime,get_screening_by_id,get_upcoming_screenings
from Functons.review import addreview,get_review_id,get_reviews_by_critic,get_average_rating,get_reviews_for_movie
from Functons.getAll import getAll,get_critics_by_status
STATUS_TABLES = {
    "Critics": ('active', 'inactive','banned','retired'),
    "Theaters": ('active', 'inactive', 'maintenance'),
    "Movies": ('active', 'inactive', 'archived')}
def main():
    list =['Movies','Critics','Screenings','Theaters','reviews']
    
    
    
    print(get_movie_by_id(4))
    print()
    view_table(list[0])
    return


if __name__ == "__main__":
    main()