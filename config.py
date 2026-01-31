import os
import sys

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
LANG = "en-US"

DATA_DIR = "data"
INTERACTIONS_FILE = f"{DATA_DIR}/interactions.csv"
GENRE_FILE = f"{DATA_DIR}/genre_weights.csv"
SEEN_FILE = f"{DATA_DIR}/seen_movies.csv"

if not TMDB_API_KEY:
    print("~ Error: TMDB_API_KEY environment variable not set.")
    sys.exit(1)
