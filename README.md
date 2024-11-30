# Recommendation-System

## Overview

Recommendation system for **books and movies**, built using both **content-based** and **collaborative filtering approaches**. It provides users with personalized recommendations and includes the following features:

- **Detailed Movie Information**: Displays an overview of movies, including genre, release year, cast, director, number of reviews (positive/negative), and average ratings.  
- **User Interaction**: Allows users to give reviews and ratings directly on the platform.  
- **Sentiment Analysis**: Analyzes user reviews to determine sentiment, which is then used to improve recommendations for individual users.  
- **Dynamic Updates**: Integrates an SQLite database to store and update user reviews and ratings, ensuring the detailed movie information stays current.   

**Video Demo**: [YouTube Video](https://www.youtube.com/watch?v=9_OgIKGtZY4)  

<p align="center">
  <img src="screenshots/Screenshot 2024-11-30 173457.png" alt="Screenshot 1" width="45%">
  <img src="screenshots/Screenshot 2024-11-30 173522.png" alt="Screenshot 2" width="45%">
</p>

---

## Working

<p align="center">
  <img src="screenshots/Screenshot 2024-11-30 185545.png" alt="Screenshot 3">
</p>


## Libraries Used

- Numpy
- Pandas
- Matplotlib
- Seaborn
- sklearn
- Re
- NLTK
- TensorFlow
- Hugging Face's Transformers Library
- Streamlit

## Git Clone and Run the App

1. **Clone the Repository**

2. **Install Dependencies**

    ```
    pip install -r requirements.txt
    ```


3. **Run the App**

    ```
    streamlit run app.py
    ```

## **Recommendation System**  

#### **1 Movie Recommendation - Content-Based Approach**  
The content-based recommendation system for movies uses information about the movies themselves to suggest similar ones. This is achieved by analyzing features like genre, overview, year, cast, director, etc.  

**Working**:  
1. **Feature Extraction**: Each movie is represented by a set of attributes. These attributes are processed into a feature vector. For example, the genre might be encoded as a binary vector where each position represents the presence or absence of a genre.  
2. **Similarity Calculation**: When a user interacts with a movie (e.g., watches or rates it), the system calculates the similarity between that movie and others using metrics like **cosine similarity** or **Euclidean distance**.  
3. **Recommendation**: Based on the similarity scores, movies most similar to the user's preferences are recommended.  

#### **2 Book Recommendation - Collaborative Filtering Approach**  
The collaborative filtering system for books relies on **user interaction data** to generate recommendations. Unlike content-based methods, collaborative filtering focuses on patterns in user behavior.  

**Working**:  
1. **User-Item Matrix**: A matrix is created where rows represent users and columns represent books, with the entries reflecting interactions like ratings.  
2. **Finding Similarities**:  
   - **User-Based Filtering**: Identifies users with similar reading preferences. If two users have liked the same books, the system assumes they may enjoy other books liked by their counterparts.  
   - **Item-Based Filtering**: Finds books that are often rated similarly by many users. For instance, if two books frequently receive similar ratings, they are considered similar.  
3. **Recommendation**: For a given user, books liked by similar users or those similar to already rated books are recommended.  

---

## **Detail Extraction**  

#### **Basic Information**:  
- **Title**: The name of the movie.  
- **Genre**: Categories like Action, Comedy, Drama, etc.  
- **Year of Release**: When the movie was released.  

#### **Cast and Crew**:  
- **Cast**: Names of the main actors and actresses.  
- **Director**: The person who directed the movie.  

#### **Overview**:  
- A brief synopsis of the movie, giving users an idea of its storyline.  

#### **User Sentiments and Ratings**:  
- **Positive Reviews**: Number of reviews with positive sentiments.  
- **Negative Reviews**: Number of reviews with negative sentiments.  
- **Average Rating**: The average score calculated based on user ratings.  

#### **Dynamic Updates**:  
All these details are dynamically updated based on user interactions, such as reviews and ratings, using an **integrated SQLite database**.  

---

## **Sentiment Analysis**  
Sentiment analysis is used to understand user feedback in the form of reviews and ratings. When users provide reviews for movies or books and rate them, the system performs **sentiment analysis** to classify these reviews as **positive** or **negative**. The results, along with the ratings, are stored in an **SQLite database** to dynamically update the movie details and improve recommendations.  

#### **Initial Approach: Machine Learning Algorithms**  
Initially, I experimented with traditional machine learning algorithms for sentiment analysis, such as:  
- **Naive Bayes**  
- **Random Forest**  
- **Decision Tree**  
- **Boosting Algorithms** (e.g., Gradient Boosting, XGBoost)  

These models showed improvement, with **accuracy increasing by 21% over baseline methods**, but they struggled to effectively capture the nuances of user reviews. Sentiment in text can be highly contextual, and machine learning models have limitations in understanding long-term dependencies and subtle emotional cues.  

#### **Deep Learning Approach: RNN and LSTM**  
To address these limitations, I implemented **deep learning techniques**, particularly:  
- **Recurrent Neural Networks (RNNs)**  
- **Long Short-Term Memory (LSTM) Networks**  

**Advantages**:  
- **Context Understanding**: RNNs and LSTMs can process sequential data, making them well-suited for text analysis where word order matters.  
- **Handling Dependencies**: LSTMs are specifically designed to capture long-term dependencies in text, which is crucial for understanding complex sentences.  

#### **Transformer-Based Approach: BERT and DistilBERT**  
Finally, I utilized **transformer-based large language models (LLMs)** for sentiment analysis:  
- **BERT (Bidirectional Encoder Representations from Transformers)**  
- **DistilBERT (a lighter version of BERT)**  

**Advantages**:  
- **Bidirectional Contextual Understanding**: Unlike RNNs and LSTMs, BERT processes text bidirectionally, understanding the context of each word based on its surroundings.  
- **Pretrained Knowledge**: BERT and DistilBERT are pretrained on massive datasets, allowing them to excel in understanding the complexity of natural language.  
- **Efficiency**: DistilBERT offers faster inference and requires less computational power while maintaining high performance.  
- **Fine-Tuning Capability**: These models can be fine-tuned on the specific sentiment analysis task using a relatively small dataset, achieving high accuracy.  

With **BERT and DistilBERT**, I achieved **up to 97% accuracy**, making them the best-performing models for sentiment analysis in this project.  

The results of sentiment analysis are stored in an **SQLite database**.  
