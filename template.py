import os
import json

structure = {
    "ai_recommendation_system": {
        "setup.py": "# Setup script for installation\n\n# Add setup code here",
        "requirements.txt": "streamlit\ntensorflow\nnumpy\npandas\nscikit-learn\npickle5",
        "README.md": "# AI Recommendation System\n\nProject description and instructions.",
        "LICENSE": "",

        "app": {
            "__init__.py": "",
            "main.py": (
                "import streamlit as st\n\n"
                "def main():\n"
                "    st.title('AI Recommendation System')\n"
                "    st.sidebar.selectbox('Choose Option', ['Books', 'Movies', 'Sentiment Analysis'])\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            ),
            "config.py": "# Configuration-related logic\n\nCONFIG = {}",
            "utils.py": "# Shared utility functions\n\ndef example_util():\n    pass",

            "data": {
                "__init__.py": "",
                "books.py": "# Book-related data handling",
                "movies.py": "# Movie-related data handling",
                "processed": {}
            },

            "models": {
                "__init__.py": "",
                "recommender.py": "# Recommendation system logic",
                "sentiment_analysis.py": "# Sentiment analysis model",
                "embeddings": {}
            },

            "streamlit_components": {
                "__init__.py": "",
                "books_ui.py": "# Streamlit UI components for books",
                "movies_ui.py": "# Streamlit UI components for movies",
                "sentiment_ui.py": "# Streamlit UI components for sentiment analysis"
            },

            "logs": {
                "application.log": "# Runtime logs",
                "tensorboard": {}
            },

            "tests": {
                "test_books.py": "# Tests for book-related functionality",
                "test_movies.py": "# Tests for movie-related functionality",
                "test_sentiment.py": "# Tests for sentiment analysis"
            },

            "config": {
                "config.json": json.dumps({
                    "database_path": "app/data/",
                    "models_path": "app/models/",
                    "log_file": "app/logs/application.log"
                }, indent=4)
            }
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  
        else: 
            with open(path, "w") as file:
                file.write(content)

if __name__ == "__main__":
    base_path = os.getcwd()  
    create_structure(base_path, structure)
    print("Folder structure and files created successfully!")
