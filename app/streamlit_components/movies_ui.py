import streamlit as st
from app.data import movies
from app.models.recommender import recommend_movies
from app.models.sentiment_analysis import predict_sentiment
import streamlit as st
from app.models import load_movie_data, get_movie_details, get_movie_sentiment

# Render movie details and sentiment analysis in the UI
# def render_movie_details(sentiment_reviews):
#     st.header("Movie Details Extraction")

#     # Load movies data only once
#     movies = load_movie_data()

#     details_movie_title = st.selectbox("Select a movie:", movies['title'].values)
#     if st.button("Extract Movie Details"):
#         # Extract movie details
#         movie_details = get_movie_details(movies, details_movie_title)
        
#         if movie_details:
#             st.write(f"Title: {movie_details['title']}")
#             st.write(f"Release Date: {movie_details['release_date']}")
#             st.write(f"Overview: {movie_details['overview']}")
#             st.write(f"Genres: {movie_details['genres']}")
#             st.write(f"Director: {movie_details['director']}")
#             st.write(f"Writer: {movie_details['writer']}")
#             st.write(f"Top 3 Cast: {movie_details['top_cast']}")

#             # Extract sentiment details
#             sentiment_details = get_movie_sentiment( details_movie_title)
            
#             if sentiment_details:
#                 st.write("Sentiment Analysis Result")
#                 st.write(f"Number of Reviews: {sentiment_details['review_count']}")
#                 st.write(f"Positive Sentiment Percentage: {sentiment_details['positive_percentage']:.2f}%")
#                 st.write(f"Negative Sentiment Percentage: {sentiment_details['negative_percentage']:.2f}%")
#                 st.write(f"Other Sentiment Percentage: {sentiment_details['other_percentage']:.2f}%")
#                 st.write(f"Average Rating: {sentiment_details['average_rating']:.2f}" if sentiment_details['average_rating'] else "Not available")
#             else:
#                 st.write("Sentiment analysis result not available for this movie.")
#         else:
#             st.write(f"Movie with title '{details_movie_title}' not found.")

def render_movie_details():
    st.header("Movie Details Extraction")

    # Load movies data only once
    movies = load_movie_data()

    # Dropdown for movie selection
    details_movie_title = st.selectbox("Select a movie:", movies['title'].values)

    if st.button("Extract Movie Details"):
        # Extract movie details
        movie_details = get_movie_details(movies, details_movie_title)

        if movie_details:
            st.subheader("Movie Details")
            st.write(f"**Title:** {movie_details['title']}")
            st.write(f"**Release Date:** {movie_details['release_date']}")
            st.write(f"**Overview:** {movie_details['overview']}")
            st.write(f"**Genres:** {movie_details['genres']}")
            st.write(f"**Director:** {movie_details['director']}")
            st.write(f"**Writer(s):** {movie_details['writer']}")
            st.write(f"**Top 3 Cast:** {movie_details['top_cast']}")

            # Extract sentiment details
            sentiment_details = get_movie_sentiment(details_movie_title)

            if sentiment_details:
                st.subheader("Sentiment Analysis Result")
                st.write(f"**Number of Reviews:** {sentiment_details['review_count']}")
                st.write(f"**Positive Sentiment Percentage:** {sentiment_details['positive_percentage']:.2f}%")
                st.write(f"**Negative Sentiment Percentage:** {sentiment_details['negative_percentage']:.2f}%")
                st.write(f"**Other Sentiment Percentage:** {sentiment_details['other_percentage']:.2f}%")
                st.write(
                    f"**Average Rating:** {sentiment_details['average_rating']:.2f}"
                    if sentiment_details['average_rating']
                    else "**Average Rating:** Not available"
                )
            else:
                st.warning("Sentiment analysis result not available for this movie.")
        else:
            st.error(f"Movie with title '{details_movie_title}' not found.")

def render_movie_recommendation():
    st.header("Movie Recommendation")
    movie_choice = st.selectbox("Select a movie:", movies.new_movies['title'].values)
    if st.button("Get Movie Recommendations"):
        recommended_movies = recommend_movies(movie_choice, movies.new_movies, movies.similarity_movies)
        st.subheader("Top 5 Recommended Movies:")
        for i, movie in enumerate(recommended_movies, start=1):
            st.write(f"{i}. {movie}")



# def render_sentiment_analysis():
#     st.header("Write review (Sentiment Analysis)")
#     review_movie_choice = st.selectbox("Select a movie for review:", movies.new_movies['title'].values)
#     review_input = st.text_area(f"Enter a review for {review_movie_choice}:")
#     rating_input = st.slider(f"Enter a rating for {review_movie_choice} (0.0 to 10.0):", 0.0, 10.0, 5.0)

#     if st.button("Analyze Sentiment"):
#         sentiment_result = predict_sentiment(review_input)
#         st.subheader("Sentiment Analysis Result:")
#         st.write(f"Sentiment: {sentiment_result}")

import sqlite3

def render_sentiment_analysis():
    st.header("Write Review (Sentiment Analysis)")
    review_movie_choice = st.selectbox("Select a movie for review:", movies.new_movies['title'].values)
    review_input = st.text_area(f"Enter a review for {review_movie_choice}:")
    rating_input = st.slider(f"Enter a rating for {review_movie_choice} (0.0 to 10.0):", 0.0, 10.0, 5.0)

    if st.button("Analyze Sentiment"):
        sentiment_result = predict_sentiment(review_input)
        st.subheader("Sentiment Analysis Result:")
        st.write(f"Sentiment: {sentiment_result}")
        
        # Insert the data into the database
        try:
            conn = sqlite3.connect("movies_data.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_title TEXT NOT NULL,
                    review TEXT NOT NULL,
                    rating REAL NOT NULL,
                    sentiment TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                INSERT INTO reviews (movie_title, review, rating, sentiment)
                VALUES (?, ?, ?, ?)
            """, (review_movie_choice, review_input, rating_input, sentiment_result))
            
            conn.commit()
            st.success("Review saved successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()
