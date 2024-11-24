import streamlit as st
from app.data import books
from app.models.recommender import recommend_books
from app.models.sentiment_analysis import predict_sentiment

def render_book_recommendation():
    st.header("Book Recommendation")
    book_choice = st.selectbox("Select a book:", books.new_books['Book-Title'].values)
    if st.button("Get Book Recommendations"):
        recommended_books = recommend_books(book_choice, books.new_books, books.similarity_books)
        st.subheader("Top 5 Recommended Books:")
        for i, book in enumerate(recommended_books, start=1):
            st.write(f"{i}. {book}")

def render_book_sentiment_analysis():
    st.header("Book Sentiment Analysis")
    review_book_choice = st.selectbox("Select a book for review:", books.new_books['Book-Title'].values)
    review_input = st.text_area(f"Enter a review for {review_book_choice}:")
    rating_input = st.slider(f"Enter a rating for {review_book_choice} (0.0 to 10.0):", 0.0, 10.0, 5.0)

    if st.button("Analyze Book Sentiment"):
        sentiment_result = predict_sentiment(review_input)
        st.subheader("Sentiment Analysis Result:")
        st.write(f"Sentiment: {sentiment_result}")
