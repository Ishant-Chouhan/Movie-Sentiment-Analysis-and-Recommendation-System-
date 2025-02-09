import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from dataset import recommendations
from sql_connectivity import get_poster
import urllib.parse

# Get movie name from URL parameters
query_params = st.query_params
movie_name = query_params.get("movie", None)

if not movie_name:
    st.error("No movie selected!")
    st.stop()

movie_name = urllib.parse.unquote(movie_name)  # Decode URL-encoded movie name

# Load tokenizer and model
with open("tokenizer.json", "r", encoding="utf-8") as f:
    tokenizer_json = f.read()
    tokenizer = tokenizer_from_json(tokenizer_json)

model = load_model("sentiment_predictor.h5")

def predict_sentiment(review):
    review = review.replace("<br />", "").replace("\'", "").replace("-", "").replace(",", "").replace(":", "").replace(".", "").replace("(", "").replace(")", "")
    sequence = tokenizer.texts_to_sequences([review])
    pd_sequence = pad_sequences(sequence, maxlen=200, padding="post")
    prediction = model.predict(pd_sequence)
    return prediction

# Database connection
user = "root"
host = "localhost"
password = "******"
database = "movies_info"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def movie_information(movie_name):
    query = "SELECT original_title, genres, overview, cast, crew, poster_path FROM movies WHERE original_title = %s"
    title = pd.read_sql(query, con=engine, params=(movie_name,))

    if title.empty:
        st.error("Movie not found.")
        return

    st.title(title.iloc[0, 0])
    poster_path = title.iloc[0, 5]
    full_poster_url = IMAGE_BASE_URL + poster_path if poster_path else None

    col = st.columns(2)

    if full_poster_url:
        col[0].image(full_poster_url, caption=title.iloc[0, 0], use_container_width=True)

    col[1].markdown(f"**Title:**<br>{title.iloc[0, 0]}", unsafe_allow_html=True)
    col[1].markdown(f"**Genre:**<br>{title.iloc[0, 1]}", unsafe_allow_html=True)
    col[1].markdown(f"**Cast:**<br>{title.iloc[0, 3]}", unsafe_allow_html=True)
    col[1].markdown(f"**Director:**<br>{title.iloc[0, 4]}", unsafe_allow_html=True)
    
    st.markdown(f"**Overview:**<br>{title.iloc[0, 2]}", unsafe_allow_html=True)
    st.markdown("<h3>__________________More For You__________________</h3>", unsafe_allow_html=True)
    st.write("Note: You can search for this movies at home page")
    recommendations_list = recommendations(movie_name)[1:]
    columns = st.columns(5)  # Create 6 columns
    placeholder = "https://image.tmdb.org/t/p/w500/pyCk5JgtRZwRxnXwfrvyzukaKue.jpg"

    for idx, i in enumerate(recommendations_list):
        path = get_poster(i[0])
        full_poster_url = IMAGE_BASE_URL + path if path else placeholder

        with columns[idx % 5]:
            st.image(full_poster_url,caption=i[1], use_container_width=True)

    movie_reviews = np.array(pd.read_sql("SELECT reviews FROM movies m INNER JOIN reviews r ON m.id=r.movie_id WHERE original_title=%s", con=engine, params=(movie_name,)))
    
    st.markdown("<h3>____________________Reviews____________________</h3>", unsafe_allow_html=True)
    user_input=st.text_input("Write your review here...")
    review_button=st.button("SAVE")
    if review_button or user_input:
        st.write("________________________________________________________________________")
        prediction = predict_sentiment(user_input)
        if prediction[0][0] >= 0.5:
            st.markdown(f'<p style="color: green; font-size: 10px;">{user_input}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color: red; font-size: 10px;">{user_input}</p>', unsafe_allow_html=True)

    for i in movie_reviews:
        st.write("________________________________________________________________________")
        prediction = predict_sentiment(i[0])
        if prediction[0][0] >= 0.5:
            st.markdown(f'<p style="color: green; font-size: 10px;">{i[0]}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color: red; font-size: 10px;">{i[0]}</p>', unsafe_allow_html=True)

movie_information(movie_name)
