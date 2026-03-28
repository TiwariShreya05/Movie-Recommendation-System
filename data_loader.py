import pickle
import pandas as pd
import streamlit as st

CACHE_TTL = 3600  # Cache data for 1 hour


@st.cache_data(ttl=CACHE_TTL)
def load_data():
    """
    Loads movie list and similarity matrix from pickle files.
    Returns:
        movies_df: DataFrame with movie details
        similarity_matrix: Precomputed similarity matrix (list of lists)
    """
    try:
        with open('movies.pkl', 'rb') as f:
            movies_dict = pickle.load(f)
        movies_df = pd.DataFrame(movies_dict)

        with open('similarity.pkl', 'rb') as f:
            similarity_matrix = pickle.load(f)

        return movies_df, similarity_matrix

    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        st.stop()
