import pandas as pd
import numpy as np


similarity = np.load("similarity.npy")
movies_tag_set = pd.read_csv("movies_tag_set.csv")

def movie_names():
    return np.array(movies_tag_set["original_title"])

def movie_idss():
    return np.array(movies_tag_set["id"])

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
    
print(recommendations("Avatar"))
    
