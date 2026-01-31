import pandas as pd
import os
from config import DATA_DIR, INTERACTIONS_FILE, GENRE_FILE, SEEN_FILE

os.makedirs(DATA_DIR, exist_ok=True)

def load_seen_movies():
    if os.path.exists(SEEN_FILE):
        return set(pd.read_csv(SEEN_FILE)["movie_id"])
    return set()

def save_seen_movie(movie_id):
    df = pd.DataFrame([[movie_id]], columns=["movie_id"])
    df.to_csv(SEEN_FILE, mode="a", header=not os.path.exists(SEEN_FILE), index=False)

def log_interaction(movie, action):
    row = {
        "movie_id": movie["id"],
        "title": movie.get("title"),
        "rating": movie.get("vote_average"),
        "popularity": movie.get("popularity"),
        "action": action
    }
    df = pd.DataFrame([row])
    df.to_csv(INTERACTIONS_FILE, mode="a",
              header=not os.path.exists(INTERACTIONS_FILE),
              index=False)

def load_genre_weights():
    if os.path.exists(GENRE_FILE):
        df = pd.read_csv(GENRE_FILE)
        return dict(zip(df.genre_id, df.weight))
    return {}

def update_genre_weights(movie, delta=1.0):
    weights = load_genre_weights()
    for g in movie.get("genre_ids", []):
        weights[g] = weights.get(g, 0) + delta

    df = pd.DataFrame(
        [{"genre_id": k, "weight": v} for k, v in weights.items()]
    )
    df.to_csv(GENRE_FILE, index=False)
