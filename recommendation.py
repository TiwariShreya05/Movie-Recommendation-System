import requests
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

# ------------------------------
# TMDB CONFIG
# ------------------------------
TMDB_API_KEY = "522a3b9f8596353a8a28fbb4dc6a5071"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500/"
REQUEST_TIMEOUT = 5
NUM_RECOMMENDATIONS = 8


# ------------------------------
# FETCH POSTER
# ------------------------------
@st.cache_data(ttl=3600)
def fetch_movie_data(movie_id):
    url = f"{TMDB_MOVIE_URL}{movie_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=videos"

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        movie_data = response.json()

        poster_path = movie_data.get("poster_path")
        poster_url = TMDB_IMAGE_URL + poster_path if poster_path else None

        vote_avg = movie_data.get("vote_average", 0)

        # Extract trailer
        trailer_key = None
        videos = movie_data.get("videos", {}).get("results", [])
        for vid in videos:
            if vid.get("type") == "Trailer" and vid.get("site") == "YouTube":
                trailer_key = vid.get("key")
                break

        trailer_url = f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None

        return {
            "poster": poster_url,
            "rating": vote_avg,
            "trailer": trailer_url
        }

    except:
        return {"poster": None, "rating": 0, "trailer": None}


# ------------------------------
# RECOMMENDATION ENGINE
# ------------------------------
def get_recommendations(input_title, movies_df, similarity_matrix):
    try:
        movie_index = movies_df[movies_df["title"] == input_title].index[0]
    except IndexError:
        st.error("Movie not found!")
        return []

    scores = list(enumerate(similarity_matrix[movie_index]))
    sorted_scores = sorted(scores, reverse=True, key=lambda x: x[1])

    selected = sorted_scores[1:NUM_RECOMMENDATIONS + 1]

    recommended_movies = []

    with ThreadPoolExecutor(max_workers=NUM_RECOMMENDATIONS) as executor:
        futures = []
        for idx, _ in selected:
            movie_id = movies_df.iloc[idx].movie_id
            movie_title = movies_df.iloc[idx].title
            futures.append((movie_title, executor.submit(fetch_movie_data, movie_id)))

        for title, f in futures:
            data = f.result()
            recommended_movies.append({
                "title": title,
                "poster": data["poster"],
                "rating": data["rating"],
                "trailer": data["trailer"]
            })

    return recommended_movies


# ------------------------------
# STREAMLIT FRONTEND
# ------------------------------
def display_movie(movie):
    col = st.container()

    with col:
        st.markdown(f"### 🎬 {movie['title']}")

        if movie["poster"]:
            st.image(movie["poster"], width=250)
        else:
            st.write("❌ Poster Not Available")

        # Display star rating
        stars = "⭐" * int(movie["rating"] // 2)
        st.write(f"**Rating:** {movie['rating']}  ({stars})")

        # Trailer button
        if movie["trailer"]:
            st.markdown(f"[🎥 Watch Trailer]({movie['trailer']})")
        else:
            st.write("No Trailer Available")


def main_ui(movies_df, similarity_matrix):
    st.title("🎥 Movie Recommender System")

    movie_list = movies_df["title"].values
    selected_movie = st.selectbox("Select a Movie", movie_list)

    if st.button("Show Recommendations"):
        results = get_recommendations(selected_movie, movies_df, similarity_matrix)

        cols = st.columns(4)
        idx = 0
        for movie in results:
            with cols[idx % 4]:
                display_movie(movie)
            idx += 1
