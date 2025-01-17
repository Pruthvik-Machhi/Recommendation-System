import streamlit as st
# from app.data import movies, books
# import pandas as pd
from app.models import recommend_movies, recommend_books, predict_sentiment

from app.streamlit_components import movies_ui, books_ui

def main():
    st.title("Recommendation and Sentiment Analysis System")
    option = st.radio("Movie or Book:", ("Movie", "Book"))

    if option == "Movie":
        movies_ui.render_movie_recommendation()
        movies_ui.render_movie_details()
        movies_ui.render_sentiment_analysis()

    elif option == "Book":
        books_ui.render_book_recommendation()
        books_ui.render_book_sentiment_analysis()

    st.info("Developed by Pruthvik Machhi")

if __name__ == "__main__":
    main()
