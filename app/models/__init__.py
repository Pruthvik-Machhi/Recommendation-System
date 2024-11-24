# app/models/__init__.py
from .recommender import recommend_movies
from .recommender import recommend_books
from .sentiment_analysis import predict_sentiment
from .extract_info import get_movie_sentiment,load_movie_data,get_movie_details