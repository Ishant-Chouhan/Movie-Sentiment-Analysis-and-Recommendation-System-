import streamlit as st
import numpy as np
import pandas as pd
from sql_connectivity import get_poster
import urllib.parse  # For encoding movie names in URLs

def top_five(movie):
    idx = movies_tag_set[movies_tag_set["original_title"] == movie].index[0]
    listidx = list(enumerate(similarity[idx]))
    similar = sorted(listidx, key=lambda x: x[1], reverse=True)

    temp = []
    for i in similar[:6]:  # Get top 6 recommendations
        MT = movies_tag_set.iloc[i[0]]["original_title"]
        MID = movies_tag_set.iloc[i[0]]["id"]
        temp.append((MID, MT))
    return temp

def recommendations(movie):
    try:
        return top_five(movie)
    except IndexError:
        return "No such Movie Exist...!!"

# Load similarity and movie dataset
similarity = np.load("similarity.npy")
movies_tag_set = pd.read_csv("movies_tag_set.csv")
movies = np.array(movies_tag_set["original_title"])
ids = np.array(movies_tag_set["id"])

st.title("So Called Entertainment")

option = st.selectbox("Search here", movies)

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
placeholder = "https://image.tmdb.org/t/p/w500/pyCk5JgtRZwRxnXwfrvyzukaKue.jpg"

if option:
    recommendations_list = recommendations(option)
    columns = st.columns(6)  # Create 6 columns

    for idx, i in enumerate(recommendations_list):
        path = get_poster(i[0])
        full_poster_url = IMAGE_BASE_URL + path if path else placeholder

        with columns[idx % 6]:
            st.image(full_poster_url, use_container_width=True)
            if st.button(f"{i[1]}", key=f"btn_{idx}"):
                movie_name_encoded = urllib.parse.quote(i[1])  # Encode for URL
                st.markdown(f'<meta http-equiv="refresh" content="0; url=/review_page?movie={movie_name_encoded}">', unsafe_allow_html=True)

# Display movies in rows with 5 per row
for i in range(0, 1000, 5):
    cols = st.columns(5)  # Create 5 columns
    for j in range(5):
        if i + j < len(ids):
            path = get_poster(ids[i + j])
            full_poster_url = IMAGE_BASE_URL + path if path else placeholder

            with cols[j]:
                st.image(full_poster_url, use_container_width=True)
                if st.button(f"{movies[i + j]}", key=f"btn_grid_{i+j}"):
                    movie_name_encoded = urllib.parse.quote(movies[i + j])  # Encode for URL
                    st.markdown(f'<meta http-equiv="refresh" content="0; url=/review_page?movie={movie_name_encoded}">', unsafe_allow_html=True)
