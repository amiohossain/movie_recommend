def format_movie(movie):
    title = movie.get("title", "Unknown")
    year = movie.get("release_date", "")[:4]
    rating = movie.get("vote_average", "N/A")
    return f"{title} ({year}) - ⭐ {rating}"

def display_movies(movies):
    print("\n~ Movies:")
    for i, m in enumerate(movies, 1):
        print(f"~ {i}. {format_movie(m)}")
    print()
