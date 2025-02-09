# Movie-Sentiment-Analysis-and-Recommendation-System-

<h3>📝Overview</h3><br>
The main objective of the project is to create a web site showing sentiment behind reviews of selected movie (Positive -> green and Negative -> red), it will also suggest movies on the basis of that selected movie.<br> 
<br>ℹ️Dataset links:<br>
1. TMDB movies dataset: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata<br>
2. IMDB reviews dataset: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews<br>
<br><h3>🎋Work Flow</h3><br>
1. Model building for sentiment analysis and saving model (.h5)/tokenizer (tokenizer.json).<br>
2. Database creation (in MYSQL)
3. Develop recommendation system and saving dataFrame (.csv)/ similarity.npy (not uploded but can be extracted from "movie recommendation system - copy.ipynb")<br>
4. Improrting dataframe into the database.<br>
5. Fetching movie posters through tmdb API and dumping into database (api_to_sql.py).<br>
6. Creating frontend through streamlit (Home.py).<br>


