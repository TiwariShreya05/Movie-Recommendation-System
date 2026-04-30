import requests

API_KEY = "YOUR_TMDB_API_KEY"

def get_trailer_url(movie_id):
    """Fetch YouTube trailer URL using TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()  

    for v in data.get("results", []):
        if v["type"] == "Trailer" and v["site"] == "YouTube":
            return f"https://www.youtube.com/embed/{v['key']}?autoplay=1"

    return None

