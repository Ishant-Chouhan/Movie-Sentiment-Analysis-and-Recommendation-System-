import requests
import time
from sql_connectivity import get_ids,update_poster


# function to fetch movie info
def fetch_movie_data(movie_id, retries=3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=<your api key>"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
            break
        except requests.exceptions.RequestException as e:
            time.sleep(1)  # Wait before retrying
    return None

j=0
for i in get_ids():
    j+=1
    print(i,j)
    fetched=fetch_movie_data(i[0])
    if fetched == None:
        update_poster(i[0],fetched)
    else:
        update_poster(i[0],fetched["poster_path"])   
