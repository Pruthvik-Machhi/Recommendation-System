import streamlit as st
import pickle
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow_hub as hub

new_movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity_movies = pickle.load(open('similarity.pkl', 'rb'))
new_books = pickle.load(open('booksnew1.pkl', 'rb')) 
similarity_books = pickle.load(open('similarity_scores1.pkl', 'rb'))  
count_vectorizer = pickle.load(open('count_vectorizer.pkl', 'rb'))

with open('sentiment_analysis_reviews.pkl', 'rb') as f:
    sentiment_reviews = pickle.load(f)

movies = pd.read_csv('reviews_and_sentiments.csv') 
bert_model = load_model('tf.h5', custom_objects={'KerasLayer': hub.KerasLayer})
bert_preproc = hub.load('tf.preproc')

def recommend_movies(movie_title):
    index = new_movies[new_movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity_movies[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [new_movies.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies

def recommend_books(book_title):
    index = new_books[new_books['Book-Title'] == book_title].index[0]
    distances = sorted(list(enumerate(similarity_books[index])), reverse=True, key=lambda x: x[1])
    recommended_books = [new_books.iloc[i[0]]['Book-Title'] for i in distances[1:6]]
    return recommended_books

def predict_sentiment(review_text):
    inputs = bert_preproc(review_text)
    prediction = bert_model.predict(inputs)
    sentiment = 'Positive' if np.argmax(prediction) == 1 else 'Negative'
    return sentiment

def extract_movie_info(movie_title):
    movies = pd.read_csv('tmdb_5000_credits.csv.zip')
    credits = pd.read_csv('tmdb_5000_movies.csv.zip')
    movies = movies.merge(credits, on='title')
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

        st.write(f"Title: {title}")
        st.write(f"Release Date: {release_date}")
        st.write(f"Overview: {overview}")
        st.write(f"Genres: {genres}")
        st.write(f"Director: {director}")
        st.write(f"Writer: {writer}")
        st.write(f"Top 3 Cast: {top_cast}")

        sentiment_result = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()]['Sentiment'].values
        if len(sentiment_result) > 0:
            review_count = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()].shape[0]
            positive_percentage = (sentiment_reviews[(sentiment_reviews['Movie'].str.lower() == movie_title.lower()) & (sentiment_reviews['Sentiment'] == 'Positive')].shape[0] / review_count) * 100
            negative_percentage = (sentiment_reviews[(sentiment_reviews['Movie'].str.lower() == movie_title.lower()) & (sentiment_reviews['Sentiment'] == 'Negative')].shape[0] / review_count) * 100
            other_percentage = 100 - (positive_percentage + negative_percentage)

            st.write(f"Sentiment Analysis Result")
            st.write(f"Number of Reviews: {review_count}")
            st.write(f"Positive Sentiment Percentage: {positive_percentage:.2f}%")
            st.write(f"Negative Sentiment Percentage: {negative_percentage:.2f}%")
            st.write(f"Other Sentiment Percentage: {other_percentage:.2f}%")

            average_rating = sentiment_reviews[sentiment_reviews['Movie'].str.lower() == movie_title.lower()]['Rating'].mean()
            st.write(f"Average Rating: {average_rating:.2f}" if not pd.isna(average_rating) else "Not available")
        else:
            st.write("Sentiment analysis result not available for this movie.")
    else:
        st.write(f"Movie with title '{movie_title}' not found.")

def main():
    global sentiment_reviews, book_sentiment_reviews

    st.title("Recommendation and Sentiment Analysis System")
    option = st.radio("Movie or Book:", ("Movie", "Book"))

    if option == "Movie":
        st.header("Movie Recommendation")

        movie_choice = st.selectbox("Select a movie:", new_movies['title'].values, key="recommendation_movie_choice")

        if st.button("Get Movie Recommendations"):
            recommended_movies = recommend_movies(movie_choice)
            st.subheader("Top 5 Recommended Movies:")
            for i, movie in enumerate(recommended_movies, start=1):
                st.write(f"{i}. {movie}")

        st.header("Movie Details Extraction")

        details_movie_title = st.selectbox("Select a movie:", new_movies['title'].values, key="details_movie_choice")

        if st.button("Extract Movie Details"):
            extract_movie_info(details_movie_title)
            st.write(f"Movie details extracted for {details_movie_title}")

        st.header("Write review (Sentiment Analysis)")

        review_movie_choice = st.selectbox("Select a movie for review:", new_movies['title'].values, key="review_movie_choice")
        review_input = st.text_area(f"Enter a review for {review_movie_choice}:", key="review_input_text_area")
        rating_input = st.slider(f"Enter a rating for {review_movie_choice} (0.0 to 10.0):", 0.0, 10.0, 5.0)

        if st.button("Analyze Sentiment"):
            sentiment_result = predict_sentiment(review_input)
            st.subheader("Sentiment Analysis Result:")
            st.write(f"Sentiment: {sentiment_result}")

            new_review = pd.DataFrame(
                {'Movie': [review_movie_choice], 'Review': [review_input], 'Sentiment': [sentiment_result],
                'Rating': [rating_input]})
            sentiment_reviews = pd.concat([sentiment_reviews, new_review], ignore_index=True)

            with open('sentiment_analysis_reviews.pkl', 'wb') as f:
                pickle.dump(sentiment_reviews, f)

            st.write("Review submitted successfully!")
            st.write(f"Review for {review_movie_choice}:")
            st.write(f"Review: {review_input}")
            st.write(f"Rating: {rating_input}")

    elif option == "Book":
        st.header("Book Recommendation")

        book_choice = st.selectbox("Select a book:", new_books['Book-Title'].values, key="recommendation_book_choice")

        if st.button("Get Book Recommendations"):
            recommended_books = recommend_books(book_choice)
            st.subheader("Top 5 Recommended Books:")
            for i, book in enumerate(recommended_books, start=1):
                st.write(f"{i}. {book}")

        st.header("Book Sentiment Analysis")

        review_book_choice = st.selectbox("Select a book for review:", new_books['Book-Title'].values, key="review_book_choice")
        review_input = st.text_area(f"Enter a review for {review_book_choice}:", key="review_input_text_area_book")
        rating_input = st.slider(f"Enter a rating for {review_book_choice} (0.0 to 10.0):", 0.0, 10.0, 5.0)

        if st.button("Analyze Book Sentiment"):
            sentiment_result = predict_sentiment(review_input)
            st.subheader("Sentiment Analysis Result:")
            st.write(f"Sentiment: {sentiment_result}")

            new_review = pd.DataFrame(
                {'Book': [review_book_choice], 'Review': [review_input], 'Sentiment': [sentiment_result],
                 'Rating': [rating_input]})
            book_sentiment_reviews = pd.concat([book_sentiment_reviews, new_review], ignore_index=True)

            with open('book_sentiments.pkl', 'wb') as f:
                pickle.dump(book_sentiment_reviews, f)

            st.write("Book review submitted successfully!")
            st.write(f"Review for {review_book_choice}:")
            st.write(f"Review: {review_input}")
            st.write(f"Rating: {rating_input}")

    st.info("Developed by Pruthvik Machhi")

if __name__ == "__main__":
    main()