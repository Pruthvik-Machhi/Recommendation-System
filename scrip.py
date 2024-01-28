import numpy as np
import pandas as pd
movies = pd.read_csv("C:\\Users\\pruth\\Downloads\\tmdb_5000_movies.csv.zip")
credits = pd.read_csv("C:\\Users\\pruth\\Downloads\\tmdb_5000_credits.csv.zip") 
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.head()
print(movies)