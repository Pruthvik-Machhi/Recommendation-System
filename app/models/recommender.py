def recommend_movies(movie_title, new_movies, similarity_movies):
    index = new_movies[new_movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity_movies[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [new_movies.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies

def recommend_books(book_title, new_books, similarity_books):
    index = new_books[new_books['Book-Title'] == book_title].index[0]
    distances = sorted(list(enumerate(similarity_books[index])), reverse=True, key=lambda x: x[1])
    recommended_books = [new_books.iloc[i[0]]['Book-Title'] for i in distances[1:6]]
    return recommended_books
