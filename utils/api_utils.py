import streamlit as st
import requests

# Fetch the API key from Streamlit secrets
try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = None

BASE_URL = "https://api.themoviedb.org/3"

def get_trending_movies():
    """Fetches a list of trending movies from TMDb."""
    if not API_KEY:
        return None
    try:
        response = requests.get(f"{BASE_URL}/trending/movie/day?api_key={API_KEY}")
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException:
        return None

def get_movie_details(query):
    """Searches for a movie and returns its details."""
    if not API_KEY:
        return None
    try:
        response = requests.get(f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}")
        response.raise_for_status()
        results = response.json().get('results', [])
        return results[0] if results else None
    except requests.RequestException:
        return None

def get_movie_reviews(movie_id):
    """Fetches reviews for a specific movie by its ID."""
    if not API_KEY or not movie_id:
        return None
    try:
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/reviews?api_key={API_KEY}")
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException:
        return None

