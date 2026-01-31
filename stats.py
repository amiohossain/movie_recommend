import pandas as pd
from config import GENRE_FILE
from genres import load_genre_map


def get_genre_stats():
    try:
        df = pd.read_csv(GENRE_FILE)
    except FileNotFoundError:
        return []

    total = df["weight"].sum()
    if total == 0:
        return []

    genre_map = load_genre_map()

    df["genre_name"] = df["genre_id"].map(
        lambda g: genre_map.get(g, f"Unknown ({g})")
    )
    df["percentage"] = (df["weight"] / total) * 100

    df = df.sort_values("weight", ascending=False)
    return df.to_dict("records")


def display_genre_stats(stats):
    print("\n~ Your Genre Preference Statistics:")
    for row in stats:
        print(f"~ {row['genre_name']}: {row['percentage']:.2f}% preference")
    print()


def get_top_genres(n=2):
    try:
        df = pd.read_csv(GENRE_FILE)
    except FileNotFoundError:
        return []

    if df.empty:
        return []

    df = df.sort_values("weight", ascending=False)
    return df["genre_id"].head(n).tolist()
