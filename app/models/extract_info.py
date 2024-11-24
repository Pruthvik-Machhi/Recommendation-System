import pandas as pd
import streamlit as st

# Load and merge movie data
def load_movie_data():
    credits = pd.read_csv(r'D:\GthubFiles\Recommendation-System\data\tmdb_5000_credits.csv')
    movies = pd.read_csv(r'D:\GthubFiles\Recommendation-System\data\tmdb_5000_movies.csv')
    movies = movies.merge(credits, on='title')
    return movies

# Extract movie details from the dataset
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

# Extract sentiment analysis for a movie
def get_movie_sentiment(sentiment_reviews, movie_title):
    sentiment_result = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()]['Sentiment'].values
    if len(sentiment_result) > 0:
        review_count = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()].shape[0]
        positive_percentage = (sentiment_reviews[(sentiment_reviews['Movie'].str.lower() == movie_title.lower()) & (sentiment_reviews['Sentiment'] == 'Positive')].shape[0] / review_count) * 100
        negative_percentage = (sentiment_reviews[(sentiment_reviews['Movie'].str.lower() == movie_title.lower()) & (sentiment_reviews['Sentiment'] == 'Negative')].shape[0] / review_count) * 100
        other_percentage = 100 - (positive_percentage + negative_percentage)

        average_rating = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()]['Rating'].mean()
        
        return {
            'review_count': review_count,
            'positive_percentage': positive_percentage,
            'negative_percentage': negative_percentage,
            'other_percentage': other_percentage,
            'average_rating': average_rating if not pd.isna(average_rating) else None
        }
    else:
        return None
