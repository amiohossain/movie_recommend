import os
import pandas as pd
from api import tmdb_get

GENRE_CACHE = "data/genres.csv"


def load_genre_map():
    if os.path.exists(GENRE_CACHE):
        df = pd.read_csv(GENRE_CACHE)
        return dict(zip(df.id, df.name))

    data = tmdb_get("/genre/movie/list")
    if not data:
        return {}

    genres = data.get("genres", [])
    df = pd.DataFrame(genres)
    df.to_csv(GENRE_CACHE, index=False)

    return dict(zip(df["id"], df["name"]))
