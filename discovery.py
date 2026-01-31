from api import tmdb_get
from recommender import rank_movies
from storage import (
    load_seen_movies, save_seen_movie,
    log_interaction, load_genre_weights,
    update_genre_weights
)
from ui import display_movies, format_movie
from stats import get_genre_stats, display_genre_stats, get_top_genres


def get_initial_movies(seen_ids):
    data = tmdb_get("/movie/popular")
    if not data:
        return []

    return [m for m in data["results"] if m["id"] not in seen_ids][:5]


def get_recommendations_from_preferences(seen_ids):
    """
    🔥 CORE FIX:
    Generate candidate movies FROM preferred genres
    Falls back to popular movies if no preferences exist yet
    """
    top_genres = get_top_genres(n=2)

    # 🔥 FALLBACK: If no genre preferences yet, use popular movies
    if not top_genres:
        print("~ No genre preferences recorded yet. Showing popular movies...")
        return get_initial_movies(seen_ids)

    data = tmdb_get("/discover/movie", {
        "with_genres": ",".join(map(str, top_genres)),
        "sort_by": "vote_average.desc",
        "vote_count.gte": 300
    })

    if not data:
        return []

    genre_weights = load_genre_weights()
    return rank_movies(data["results"], genre_weights, seen_ids)


def discovery_loop():
    seen_ids = load_seen_movies()
    genre_weights = load_genre_weights()

    current_list = get_initial_movies(seen_ids)

    while True:
        display_movies(current_list)

        choice = input(
            "~ Choose a movie number to LIKE\n"
            "~ 's' skip | 'r' refresh | 'rec' recommend now | 'e' exit\n"
            "~ Your Answer: "
        ).strip().lower()

        # Exit
        if choice == "e":
            print("~ Exiting Movie Discovery.")
            break

        # 🔥 RECOMMEND NOW (FIXED)
        if choice == "rec":
            print("\n~ Generating recommendations based on your preferences...")

            stats = get_genre_stats()
            if not stats:
                print("~ Not enough preference data yet. Using popular recommendations...")
            else:
                display_genre_stats(stats)

            recommendations = get_recommendations_from_preferences(seen_ids)

            if not recommendations:
                print("~ No recommendations found.")
                continue

            print("~ Recommended Movies For You:")
            for i, m in enumerate(recommendations, 1):
                print(f"~ {i}. {format_movie(m)}")
            print()
            continue

        # Refresh
        if choice == "r":
            for m in current_list:
                save_seen_movie(m["id"])
                log_interaction(m, "refresh")
                seen_ids.add(m["id"])

            current_list = get_initial_movies(seen_ids)
            continue

        # Skip
        if choice == "s":
            for m in current_list:
                save_seen_movie(m["id"])
                log_interaction(m, "skip")
                seen_ids.add(m["id"])

            current_list = get_initial_movies(seen_ids)
            continue

        # Like
        if not choice.isdigit():
            print("~ Invalid input.")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(current_list):
            print("~ Selection out of range.")
            continue

        selected = current_list[idx]
        print(f"\n~ You liked: {format_movie(selected)}")

        update_genre_weights(selected, delta=1.0)
        log_interaction(selected, "like")
        save_seen_movie(selected["id"])
        seen_ids.add(selected["id"])

        # Next list pivots immediately
        data = tmdb_get(f"/movie/{selected['id']}/recommendations")
        current_list = [
            m for m in data["results"]
            if m["id"] not in seen_ids
        ][:5] if data else get_initial_movies(seen_ids)
        
        # 🔥 FALLBACK: If no recommendations found, get popular movies
        if not current_list:
            current_list = get_initial_movies(seen_ids)