import numpy as np
import pandas as pd
movies = pd.read_csv("C:\\Users\\pruth\\Downloads\\tmdb_5000_movies.csv.zip")
credits = pd.read_csv("C:\\Users\\pruth\\Downloads\\tmdb_5000_credits.csv.zip") 
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
# movies.head()
# print(movies)
import ast

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)
# movies.head()

movies['keywords'] = movies['keywords'].apply(convert)
# movies.head()

import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 

movies['cast'] = movies['cast'].apply(convert)
# movies.head()

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 

movies['crew'] = movies['crew'].apply(fetch_director)

#movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.sample(5)
# print(movies)