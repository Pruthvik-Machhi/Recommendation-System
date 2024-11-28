import pandas as pd
import streamlit as st
import os

def load_movie_data():
    base_path = os.path.join(os.getcwd(), 'data') 
    credits_path = os.path.join(base_path, 'tmdb_5000_credits.csv')
    movies_path = os.path.join(base_path, 'tmdb_5000_movies.csv')
    credits = pd.read_csv(credits_path)
    movies = pd.read_csv(movies_path)
    movies = movies.merge(credits, on='title')
    
    return movies
def get_movie_details(movies, movie_title):
    movie_data = movies[movies['title'].str.lower() == movie_title.lower()]
    
    if not movie_data.empty:
        title = movie_data['title'].values[0]
        release_date = pd.to_datetime(movie_data['release_date'].values[0]).strftime('%Y-%m-%d')
        overview = movie_data['overview'].values[0]
        genres_list = movie_data['genres'].values[0]
        genres = ', '.join([genre['name'] for genre in eval(genres_list)])
        crew_list = eval(movie_data['crew'].values[0])
        director = ', '.join([crew['name'] for crew in crew_list if crew['job'] == 'Director'])
        writer_list = [crew['name'] for crew in crew_list if crew['job'] == 'Screenplay'][:3]
        writer = ', '.join(writer_list)
        cast_list = eval(movie_data['cast'].values[0])
        top_cast = ', '.join([cast['name'] for cast in cast_list[:3]])

        return {
            'title': title,
            'release_date': release_date,
            'overview': overview,
            'genres': genres,
            'director': director,
            'writer': writer,
            'top_cast': top_cast
        }
    else:
        return None


import sqlite3

def get_movie_sentiment(movie_title):
    try:
        conn = sqlite3.connect("movies_data.db")
        cursor = conn.cursor()
        
        query = """
        SELECT sentiment, rating
        FROM reviews
        WHERE LOWER(movie_title) = LOWER(?)
        """
        cursor.execute(query, (movie_title,))
        reviews = cursor.fetchall()
        
        if reviews:
            review_count = len(reviews)
            positive_count = sum(1 for review in reviews if review[0] == 'Positive')
            negative_count = sum(1 for review in reviews if review[0] == 'Negative')
            positive_percentage = (positive_count / review_count) * 100
            negative_percentage = (negative_count / review_count) * 100
            other_percentage = 100 - (positive_percentage + negative_percentage)
            average_rating = sum(review[1] for review in reviews if review[1] is not None) / review_count
            
            return {
                'review_count': review_count,
                'positive_percentage': positive_percentage,
                'negative_percentage': negative_percentage,
                'other_percentage': other_percentage,
                'average_rating': average_rating if not pd.isna(average_rating) else None
            }
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

