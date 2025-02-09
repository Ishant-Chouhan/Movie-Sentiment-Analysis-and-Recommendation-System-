from sqlalchemy import create_engine,Table, MetaData, update, select
import pandas as pd
import numpy as np

user = "root"
host="localhost"
password="*******"
database="movies_info"
#creating connection 
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# function to fetch movie title
def get_titles():
    movie_array=np.asarray(pd.read_sql("select original_title from movies",con=engine))
    l=[]
    for i in range(len(movie_array)):
        l.append(movie_array[i][0])

    return l


#funtion to fetch poter_path of given movie id
def get_poster(movie_id):
    poster=pd.read_sql(f"select poster_path from movies where id={movie_id}",con=engine)
    return poster.iloc[0,0]

# function to get id to fetch movie informations
def get_ids():
    id_array=np.asarray(pd.read_sql("select id from movies",con=engine))
    return id_array


#updating poster_path into movies table in sql database
metadata = MetaData()
movies = Table("movies", metadata, autoload_with=engine)

# Function to update poster_path
def update_poster(movie_id, new_poster_path):
    """Update poster_path only if it's NULL. If no NULL values exist, display a message."""
    
    # Check if the poster_path is NULL for the given movie_id
    stmt_check = select(movies.c.id).where((movies.c.id == movie_id) & (movies.c.poster_path.is_(None)))

    with engine.connect() as conn:
        result = conn.execute(stmt_check).fetchone()
        
        if result:
            # If a NULL poster_path exists, update it
            stmt_update = update(movies).where(movies.c.id == movie_id, movies.c.poster_path.is_(None)).values(poster_path=new_poster_path)
            conn.execute(stmt_update)
            conn.commit()
            print(f"Updated movie {movie_id} with new poster path: {new_poster_path}")
        else:
            # If there's no NULL poster_path for this movie_id
            print(f"No update needed: Movie {movie_id} already has a poster path.")

print(get_ids())